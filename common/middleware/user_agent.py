"""
User-Agent轮换和浏览器指纹伪装
"""

import random
import logging
from typing import List


# 真实的User-Agent库 (来自真实浏览器)
USER_AGENTS = [
    # Chrome on Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    
    # Chrome on Mac
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    
    # Firefox on Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    
    # Firefox on Mac
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    
    # Safari on Mac
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    
    # Edge on Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    
    # Chrome on Linux
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]


class UserAgentRotator:
    """
    User-Agent轮换器
    """
    
    def __init__(
        self,
        user_agents: List[str] = None,
        strategy: str = "random"  # random, round_robin
    ):
        """
        初始化User-Agent轮换器
        
        Args:
            user_agents: User-Agent列表
            strategy: 轮换策略
        """
        self.user_agents = user_agents or USER_AGENTS
        self.strategy = strategy
        self.current_index = 0
        self.logger = logging.getLogger(__name__)
    
    def get_user_agent(self) -> str:
        """获取一个User-Agent"""
        if self.strategy == "random":
            return random.choice(self.user_agents)
        elif self.strategy == "round_robin":
            ua = self.user_agents[self.current_index % len(self.user_agents)]
            self.current_index += 1
            return ua
        else:
            return self.user_agents[0]


class BrowserFingerprintManager:
    """
    浏览器指纹管理器
    
    生成一致的浏览器指纹,避免被检测
    """
    
    # 常见的Accept头
    ACCEPT_HEADERS = {
        'html': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'json': 'application/json, text/plain, */*',
        'image': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    }
    
    # 常见的Accept-Language
    ACCEPT_LANGUAGES = [
        'en-US,en;q=0.9',
        'zh-CN,zh;q=0.9,en;q=0.8',
        'en-GB,en;q=0.9',
    ]
    
    # 常见的Accept-Encoding
    ACCEPT_ENCODING = 'gzip, deflate, br'
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_headers(
        self,
        user_agent: str,
        referer: str = None,
        accept_type: str = 'html'
    ) -> dict:
        """
        生成完整的请求头
        
        Args:
            user_agent: User-Agent
            referer: Referer
            accept_type: 接受的内容类型
        
        Returns:
            请求头字典
        """
        headers = {
            'User-Agent': user_agent,
            'Accept': self.ACCEPT_HEADERS.get(accept_type, self.ACCEPT_HEADERS['html']),
            'Accept-Language': random.choice(self.ACCEPT_LANGUAGES),
            'Accept-Encoding': self.ACCEPT_ENCODING,
            'DNT': '1',  # Do Not Track
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        if referer:
            headers['Referer'] = referer
        
        # 根据User-Agent添加特定头
        if 'Chrome' in user_agent:
            headers['sec-ch-ua'] = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
            headers['sec-ch-ua-mobile'] = '?0'
            headers['sec-ch-ua-platform'] = '"Windows"' if 'Windows' in user_agent else '"macOS"'
            headers['Sec-Fetch-Site'] = 'none'
            headers['Sec-Fetch-Mode'] = 'navigate'
            headers['Sec-Fetch-User'] = '?1'
            headers['Sec-Fetch-Dest'] = 'document'
        
        return headers


class ScrapyUserAgentMiddleware:
    """Scrapy User-Agent中间件"""
    
    def __init__(
        self,
        user_agent_rotator: UserAgentRotator,
        fingerprint_manager: BrowserFingerprintManager
    ):
        self.ua_rotator = user_agent_rotator
        self.fp_manager = fingerprint_manager
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        # 从settings加载配置
        user_agents = crawler.settings.getlist('USER_AGENT_LIST', None)
        strategy = crawler.settings.get('USER_AGENT_STRATEGY', 'random')
        
        ua_rotator = UserAgentRotator(
            user_agents=user_agents,
            strategy=strategy
        )
        
        fp_manager = BrowserFingerprintManager()
        
        return cls(ua_rotator, fp_manager)
    
    def process_request(self, request, spider):
        """为请求设置User-Agent和其他头"""
        # 获取User-Agent
        user_agent = self.ua_rotator.get_user_agent()
        
        # 生成完整的请求头
        headers = self.fp_manager.get_headers(
            user_agent=user_agent,
            referer=request.headers.get('Referer')
        )
        
        # 更新请求头
        for key, value in headers.items():
            request.headers[key] = value
        
        self.logger.debug(f"使用User-Agent: {user_agent[:50]}...")


# 创建__init__.py
def create_init_files():
    """创建必要的__init__.py文件"""
    import os
    
    dirs = [
        '/home/ubuntu/biomedical-data-scraper-platform/common/proxy',
        '/home/ubuntu/biomedical-data-scraper-platform/common/middleware',
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        init_file = os.path.join(dir_path, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Auto-generated\n')


if __name__ == '__main__':
    create_init_files()
