"""
请求频率控制和会话管理中间件
"""

import time
import random
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import pickle
import os


class SmartRateLimiter:
    """
    智能频率限制器
    
    功能:
    1. 基于域名的独立限流
    2. 动态调整延迟(根据响应时间和错误率)
    3. 随机延迟模拟人类行为
    """
    
    def __init__(
        self,
        min_delay: float = 1.0,
        max_delay: float = 5.0,
        randomize: bool = True,
        adaptive: bool = True
    ):
        """
        初始化限流器
        
        Args:
            min_delay: 最小延迟(秒)
            max_delay: 最大延迟(秒)
            randomize: 是否随机化延迟
            adaptive: 是否自适应调整
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.randomize = randomize
        self.adaptive = adaptive
        
        # 记录每个域名的最后请求时间
        self.last_request_time: Dict[str, float] = {}
        
        # 记录每个域名的统计信息
        self.domain_stats: Dict[str, Dict] = defaultdict(lambda: {
            'total_requests': 0,
            'success_requests': 0,
            'failed_requests': 0,
            'avg_response_time': 0.0,
            'current_delay': min_delay
        })
        
        self.logger = logging.getLogger(__name__)
    
    def wait_if_needed(self, domain: str):
        """如果需要,等待一段时间"""
        now = time.time()
        last_time = self.last_request_time.get(domain, 0)
        
        # 计算需要等待的时间
        stats = self.domain_stats[domain]
        delay = stats['current_delay']
        
        if self.randomize:
            # 添加随机性 (±30%)
            delay = delay * random.uniform(0.7, 1.3)
        
        elapsed = now - last_time
        wait_time = max(0, delay - elapsed)
        
        if wait_time > 0:
            self.logger.debug(f"等待 {wait_time:.2f}秒 (域名: {domain})")
            time.sleep(wait_time)
        
        # 更新最后请求时间
        self.last_request_time[domain] = time.time()
    
    def record_success(self, domain: str, response_time: float):
        """记录成功请求"""
        stats = self.domain_stats[domain]
        stats['total_requests'] += 1
        stats['success_requests'] += 1
        
        # 更新平均响应时间
        if stats['avg_response_time'] == 0:
            stats['avg_response_time'] = response_time
        else:
            stats['avg_response_time'] = (stats['avg_response_time'] + response_time) / 2
        
        # 自适应调整延迟
        if self.adaptive:
            self._adjust_delay(domain)
    
    def record_failure(self, domain: str):
        """记录失败请求"""
        stats = self.domain_stats[domain]
        stats['total_requests'] += 1
        stats['failed_requests'] += 1
        
        # 自适应调整延迟
        if self.adaptive:
            self._adjust_delay(domain)
    
    def _adjust_delay(self, domain: str):
        """自适应调整延迟"""
        stats = self.domain_stats[domain]
        
        # 计算错误率
        error_rate = stats['failed_requests'] / stats['total_requests'] if stats['total_requests'] > 0 else 0
        
        current_delay = stats['current_delay']
        
        # 如果错误率高,增加延迟
        if error_rate > 0.2:  # 错误率超过20%
            new_delay = min(current_delay * 1.5, self.max_delay)
            self.logger.warning(f"错误率过高({error_rate:.1%}), 增加延迟: {current_delay:.2f}s -> {new_delay:.2f}s")
            stats['current_delay'] = new_delay
        
        # 如果错误率低且响应快,减少延迟
        elif error_rate < 0.05 and stats['avg_response_time'] < 1.0:
            new_delay = max(current_delay * 0.9, self.min_delay)
            if new_delay < current_delay:
                self.logger.info(f"性能良好, 减少延迟: {current_delay:.2f}s -> {new_delay:.2f}s")
                stats['current_delay'] = new_delay


class SessionManager:
    """
    会话管理器
    
    功能:
    1. Cookie持久化
    2. 会话复用
    3. 登录状态管理
    4. 多账号轮换
    """
    
    def __init__(
        self,
        session_dir: str = "./data/sessions",
        session_timeout: int = 3600  # 会话超时时间(秒)
    ):
        """
        初始化会话管理器
        
        Args:
            session_dir: 会话存储目录
            session_timeout: 会话超时时间
        """
        self.session_dir = session_dir
        self.session_timeout = session_timeout
        self.logger = logging.getLogger(__name__)
        
        # 创建会话目录
        os.makedirs(session_dir, exist_ok=True)
        
        # 内存中的会话缓存
        self.sessions: Dict[str, Dict] = {}
    
    def get_session(self, platform: str, account_id: Optional[str] = None) -> Optional[Dict]:
        """
        获取会话
        
        Args:
            platform: 平台名称
            account_id: 账号ID(可选)
        
        Returns:
            会话数据(包含cookies等)
        """
        session_key = f"{platform}_{account_id}" if account_id else platform
        
        # 先从内存缓存查找
        if session_key in self.sessions:
            session = self.sessions[session_key]
            
            # 检查是否过期
            if self._is_session_valid(session):
                self.logger.debug(f"使用缓存会话: {session_key}")
                return session
            else:
                self.logger.info(f"会话已过期: {session_key}")
                del self.sessions[session_key]
        
        # 从文件加载
        session = self._load_session_from_file(session_key)
        if session and self._is_session_valid(session):
            self.sessions[session_key] = session
            self.logger.info(f"从文件加载会话: {session_key}")
            return session
        
        self.logger.info(f"没有有效会话: {session_key}")
        return None
    
    def save_session(
        self,
        platform: str,
        cookies: Dict,
        account_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        保存会话
        
        Args:
            platform: 平台名称
            cookies: Cookie字典
            account_id: 账号ID
            metadata: 额外的元数据
        """
        session_key = f"{platform}_{account_id}" if account_id else platform
        
        session = {
            'platform': platform,
            'account_id': account_id,
            'cookies': cookies,
            'created_at': datetime.now().isoformat(),
            'last_used': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        # 保存到内存
        self.sessions[session_key] = session
        
        # 保存到文件
        self._save_session_to_file(session_key, session)
        
        self.logger.info(f"保存会话: {session_key}")
    
    def _is_session_valid(self, session: Dict) -> bool:
        """检查会话是否有效"""
        try:
            last_used = datetime.fromisoformat(session['last_used'])
            age = (datetime.now() - last_used).total_seconds()
            return age < self.session_timeout
        except:
            return False
    
    def _get_session_filepath(self, session_key: str) -> str:
        """获取会话文件路径"""
        return os.path.join(self.session_dir, f"{session_key}.pkl")
    
    def _load_session_from_file(self, session_key: str) -> Optional[Dict]:
        """从文件加载会话"""
        filepath = self._get_session_filepath(session_key)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            self.logger.error(f"加载会话文件失败: {e}")
            return None
    
    def _save_session_to_file(self, session_key: str, session: Dict):
        """保存会话到文件"""
        filepath = self._get_session_filepath(session_key)
        
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(session, f)
        except Exception as e:
            self.logger.error(f"保存会话文件失败: {e}")
    
    def clear_session(self, platform: str, account_id: Optional[str] = None):
        """清除会话"""
        session_key = f"{platform}_{account_id}" if account_id else platform
        
        # 从内存删除
        if session_key in self.sessions:
            del self.sessions[session_key]
        
        # 删除文件
        filepath = self._get_session_filepath(session_key)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        self.logger.info(f"清除会话: {session_key}")


class ScrapyRateLimitMiddleware:
    """Scrapy频率限制中间件"""
    
    def __init__(self, rate_limiter: SmartRateLimiter):
        self.rate_limiter = rate_limiter
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        min_delay = crawler.settings.getfloat('DOWNLOAD_DELAY', 1.0)
        max_delay = crawler.settings.getfloat('MAX_DOWNLOAD_DELAY', 5.0)
        randomize = crawler.settings.getbool('RANDOMIZE_DOWNLOAD_DELAY', True)
        adaptive = crawler.settings.getbool('ADAPTIVE_DOWNLOAD_DELAY', True)
        
        rate_limiter = SmartRateLimiter(
            min_delay=min_delay,
            max_delay=max_delay,
            randomize=randomize,
            adaptive=adaptive
        )
        
        return cls(rate_limiter)
    
    def process_request(self, request, spider):
        """处理请求前等待"""
        domain = request.url.split('/')[2]  # 提取域名
        self.rate_limiter.wait_if_needed(domain)
    
    def process_response(self, request, response, spider):
        """记录响应"""
        domain = request.url.split('/')[2]
        response_time = request.meta.get('download_latency', 0)
        
        if response.status == 200:
            self.rate_limiter.record_success(domain, response_time)
        else:
            self.rate_limiter.record_failure(domain)
        
        return response
    
    def process_exception(self, request, exception, spider):
        """记录异常"""
        domain = request.url.split('/')[2]
        self.rate_limiter.record_failure(domain)


class ScrapySessionMiddleware:
    """Scrapy会话管理中间件"""
    
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        session_dir = crawler.settings.get('SESSION_DIR', './data/sessions')
        session_timeout = crawler.settings.getint('SESSION_TIMEOUT', 3600)
        
        session_manager = SessionManager(
            session_dir=session_dir,
            session_timeout=session_timeout
        )
        
        return cls(session_manager)
    
    def process_request(self, request, spider):
        """为请求添加会话cookies"""
        platform = spider.name
        
        # 获取会话
        session = self.session_manager.get_session(platform)
        
        if session:
            # 添加cookies到请求
            cookies = session.get('cookies', {})
            request.cookies.update(cookies)
            self.logger.debug(f"使用会话cookies: {platform}")
    
    def process_response(self, request, response, spider):
        """保存响应中的cookies"""
        platform = spider.name
        
        # 提取cookies
        cookies = {}
        for cookie in response.headers.getlist('Set-Cookie'):
            # 简单解析(实际应该用更健壮的方法)
            parts = cookie.decode().split(';')[0].split('=', 1)
            if len(parts) == 2:
                cookies[parts[0]] = parts[1]
        
        if cookies:
            # 保存会话
            self.session_manager.save_session(platform, cookies)
        
        return response
