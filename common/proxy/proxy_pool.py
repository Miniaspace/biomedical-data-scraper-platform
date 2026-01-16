"""
代理IP池管理模块
支持多种代理源和智能轮换策略
"""

import random
import time
import logging
from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests


@dataclass
class ProxyInfo:
    """代理信息"""
    url: str  # 格式: http://user:pass@host:port
    protocol: str = "http"  # http, https, socks5
    success_count: int = 0
    fail_count: int = 0
    last_used: Optional[datetime] = None
    last_success: Optional[datetime] = None
    response_time: float = 0.0  # 平均响应时间(秒)
    is_banned: bool = False
    
    @property
    def success_rate(self) -> float:
        """成功率"""
        total = self.success_count + self.fail_count
        return self.success_count / total if total > 0 else 0.0
    
    @property
    def score(self) -> float:
        """代理评分 (0-100)"""
        # 综合考虑成功率和响应时间
        success_score = self.success_rate * 70
        speed_score = max(0, 30 - self.response_time * 10)
        return success_score + speed_score


class ProxyPool:
    """
    代理池管理器
    
    功能:
    1. 从多个源加载代理
    2. 智能轮换和选择
    3. 健康检查和自动移除失效代理
    4. 统计和监控
    """
    
    def __init__(
        self,
        proxies: Optional[List[str]] = None,
        rotation_strategy: str = "round_robin",  # round_robin, random, best_performance
        max_fail_count: int = 5,
        ban_duration: int = 300,  # 封禁后冷却时间(秒)
        health_check_url: str = "http://httpbin.org/ip"
    ):
        """
        初始化代理池
        
        Args:
            proxies: 代理列表
            rotation_strategy: 轮换策略
            max_fail_count: 最大失败次数
            ban_duration: 封禁冷却时间
            health_check_url: 健康检查URL
        """
        self.logger = logging.getLogger(__name__)
        self.rotation_strategy = rotation_strategy
        self.max_fail_count = max_fail_count
        self.ban_duration = ban_duration
        self.health_check_url = health_check_url
        
        # 初始化代理池
        self.proxies: List[ProxyInfo] = []
        if proxies:
            for proxy_url in proxies:
                self.add_proxy(proxy_url)
        
        self.current_index = 0
        self.logger.info(f"代理池初始化完成: {len(self.proxies)} 个代理")
    
    def add_proxy(self, proxy_url: str, protocol: str = "http"):
        """添加代理"""
        proxy_info = ProxyInfo(url=proxy_url, protocol=protocol)
        self.proxies.append(proxy_info)
        self.logger.debug(f"添加代理: {proxy_url}")
    
    def get_proxy(self) -> Optional[Dict[str, str]]:
        """
        获取一个可用代理
        
        Returns:
            代理字典 {"http": "...", "https": "..."}
        """
        if not self.proxies:
            self.logger.warning("代理池为空")
            return None
        
        # 过滤可用代理
        available_proxies = [
            p for p in self.proxies
            if not p.is_banned or (
                p.last_used and 
                datetime.now() - p.last_used > timedelta(seconds=self.ban_duration)
            )
        ]
        
        if not available_proxies:
            self.logger.warning("没有可用代理")
            return None
        
        # 根据策略选择代理
        if self.rotation_strategy == "round_robin":
            proxy = self._get_round_robin(available_proxies)
        elif self.rotation_strategy == "random":
            proxy = random.choice(available_proxies)
        elif self.rotation_strategy == "best_performance":
            proxy = max(available_proxies, key=lambda p: p.score)
        else:
            proxy = available_proxies[0]
        
        # 更新使用时间
        proxy.last_used = datetime.now()
        
        # 返回Scrapy格式的代理
        return {
            "http": proxy.url,
            "https": proxy.url
        }
    
    def _get_round_robin(self, proxies: List[ProxyInfo]) -> ProxyInfo:
        """轮询策略"""
        proxy = proxies[self.current_index % len(proxies)]
        self.current_index += 1
        return proxy
    
    def mark_success(self, proxy_url: str, response_time: float = 0.0):
        """标记代理成功"""
        proxy = self._find_proxy(proxy_url)
        if proxy:
            proxy.success_count += 1
            proxy.last_success = datetime.now()
            proxy.is_banned = False
            
            # 更新平均响应时间
            if proxy.response_time == 0:
                proxy.response_time = response_time
            else:
                proxy.response_time = (proxy.response_time + response_time) / 2
            
            self.logger.debug(f"代理成功: {proxy_url}, 成功率: {proxy.success_rate:.2%}")
    
    def mark_failure(self, proxy_url: str, reason: str = ""):
        """标记代理失败"""
        proxy = self._find_proxy(proxy_url)
        if proxy:
            proxy.fail_count += 1
            
            # 判断是否需要封禁
            if proxy.fail_count >= self.max_fail_count:
                proxy.is_banned = True
                self.logger.warning(f"代理被封禁: {proxy_url}, 原因: {reason}")
            else:
                self.logger.debug(f"代理失败: {proxy_url}, 失败次数: {proxy.fail_count}")
    
    def _find_proxy(self, proxy_url: str) -> Optional[ProxyInfo]:
        """查找代理"""
        for proxy in self.proxies:
            if proxy.url == proxy_url:
                return proxy
        return None
    
    def health_check(self) -> Dict[str, int]:
        """
        健康检查
        
        Returns:
            统计信息
        """
        self.logger.info("开始代理健康检查...")
        
        healthy = 0
        unhealthy = 0
        
        for proxy in self.proxies:
            try:
                start_time = time.time()
                response = requests.get(
                    self.health_check_url,
                    proxies={"http": proxy.url, "https": proxy.url},
                    timeout=10
                )
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    self.mark_success(proxy.url, response_time)
                    healthy += 1
                else:
                    self.mark_failure(proxy.url, f"状态码: {response.status_code}")
                    unhealthy += 1
                    
            except Exception as e:
                self.mark_failure(proxy.url, str(e))
                unhealthy += 1
        
        stats = {
            "total": len(self.proxies),
            "healthy": healthy,
            "unhealthy": unhealthy,
            "banned": sum(1 for p in self.proxies if p.is_banned)
        }
        
        self.logger.info(f"健康检查完成: {stats}")
        return stats
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_proxies": len(self.proxies),
            "available_proxies": sum(1 for p in self.proxies if not p.is_banned),
            "banned_proxies": sum(1 for p in self.proxies if p.is_banned),
            "avg_success_rate": sum(p.success_rate for p in self.proxies) / len(self.proxies) if self.proxies else 0,
            "avg_response_time": sum(p.response_time for p in self.proxies) / len(self.proxies) if self.proxies else 0,
        }
    
    def load_from_file(self, filepath: str):
        """从文件加载代理列表"""
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    proxy_url = line.strip()
                    if proxy_url and not proxy_url.startswith('#'):
                        self.add_proxy(proxy_url)
            self.logger.info(f"从文件加载了 {len(self.proxies)} 个代理")
        except Exception as e:
            self.logger.error(f"加载代理文件失败: {e}")
    
    def load_from_api(self, api_url: str, parser_func=None):
        """
        从API加载代理列表
        
        Args:
            api_url: API地址
            parser_func: 解析函数,接收响应JSON,返回代理URL列表
        """
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            
            if parser_func:
                proxy_urls = parser_func(response.json())
            else:
                # 默认解析器
                data = response.json()
                if isinstance(data, list):
                    proxy_urls = data
                elif isinstance(data, dict) and 'proxies' in data:
                    proxy_urls = data['proxies']
                else:
                    raise ValueError("无法解析API响应")
            
            for proxy_url in proxy_urls:
                self.add_proxy(proxy_url)
            
            self.logger.info(f"从API加载了 {len(proxy_urls)} 个代理")
            
        except Exception as e:
            self.logger.error(f"从API加载代理失败: {e}")


class ScrapyProxyMiddleware:
    """
    Scrapy代理中间件
    自动为每个请求分配代理
    """
    
    def __init__(self, proxy_pool: ProxyPool):
        self.proxy_pool = proxy_pool
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        # 从settings加载代理配置
        proxy_list = crawler.settings.getlist('PROXY_LIST', [])
        proxy_file = crawler.settings.get('PROXY_FILE')
        proxy_api = crawler.settings.get('PROXY_API')
        rotation_strategy = crawler.settings.get('PROXY_ROTATION_STRATEGY', 'round_robin')
        
        # 初始化代理池
        proxy_pool = ProxyPool(
            proxies=proxy_list,
            rotation_strategy=rotation_strategy
        )
        
        # 从文件或API加载
        if proxy_file:
            proxy_pool.load_from_file(proxy_file)
        if proxy_api:
            proxy_pool.load_from_api(proxy_api)
        
        return cls(proxy_pool)
    
    def process_request(self, request, spider):
        """为请求分配代理"""
        # 检查是否禁用代理
        if request.meta.get('dont_use_proxy'):
            return
        
        # 获取代理
        proxy = self.proxy_pool.get_proxy()
        if proxy:
            request.meta['proxy'] = proxy['http']
            self.logger.debug(f"使用代理: {proxy['http']}")
    
    def process_response(self, request, response, spider):
        """处理响应"""
        proxy_url = request.meta.get('proxy')
        
        if proxy_url and response.status == 200:
            # 标记成功
            self.proxy_pool.mark_success(proxy_url)
        
        return response
    
    def process_exception(self, request, exception, spider):
        """处理异常"""
        proxy_url = request.meta.get('proxy')
        
        if proxy_url:
            # 标记失败
            self.proxy_pool.mark_failure(proxy_url, str(exception))
            
            # 重试请求(使用新代理)
            request.meta['proxy'] = None
            return request
