"""
LoginSkill - 通用登录处理Skill
"""

import re
from typing import Dict, Any
from common.agent_skills.skill_base import BaseSkill, SkillMetadata


class LoginSkill(BaseSkill):
    """
    通用登录处理Skill
    
    功能:
    - 自动识别登录表单
    - 填充用户名和密码
    - 处理常见的登录流程
    - 保存登录后的会话
    """
    
    @property
    def metadata(self) -> SkillMetadata:
        return SkillMetadata(
            name="login",
            version="1.0.0",
            description="通用登录处理，支持表单登录、OAuth等多种方式",
            author="Biomedical Data Scraper Team",
            tags=["authentication", "login", "session"],
            priority=90  # 高优先级，因为登录通常是第一步
        )
    
    def can_handle(self, context: Dict[str, Any]) -> bool:
        """
        判断是否需要登录
        
        检查:
        1. 是否提供了凭证
        2. 页面是否包含登录表单
        3. 是否已经登录
        """
        # 检查是否提供了凭证
        credentials = context.get('credentials')
        if not credentials:
            return False
        
        # 检查是否已经有有效会话
        if context.get('session_valid'):
            return False
        
        # 检查页面是否包含登录表单
        html = context.get('html', '')
        if self._has_login_form(html):
            return True
        
        # 检查URL是否是登录页面
        url = context.get('url', '')
        if re.search(r'/(login|signin|auth)', url, re.I):
            return True
        
        return False
    
    def _has_login_form(self, html: str) -> bool:
        """检查HTML是否包含登录表单"""
        # 简单的启发式检测
        login_indicators = [
            r'<input[^>]*type=["\']password["\']',
            r'<input[^>]*name=["\']password["\']',
            r'<input[^>]*name=["\']username["\']',
            r'<input[^>]*name=["\']email["\']',
            r'<form[^>]*login',
        ]
        
        for pattern in login_indicators:
            if re.search(pattern, html, re.I):
                return True
        
        return False
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行登录
        
        Args:
            context: 包含credentials, html, response等信息
        
        Returns:
            包含session, cookies等登录结果
        """
        credentials = context['credentials']
        platform = context.get('platform', 'unknown')
        
        self.logger.info(f"Attempting login for platform: {platform}")
        
        # 提取表单字段
        html = context.get('html', '')
        form_fields = self._extract_form_fields(html)
        
        # 填充凭证
        form_data = self._fill_credentials(form_fields, credentials)
        
        # 返回登录请求的数据
        return {
            'login_required': True,
            'login_form_data': form_data,
            'login_url': context.get('url'),
            'login_method': 'POST'
        }
    
    def _extract_form_fields(self, html: str) -> Dict[str, str]:
        """从HTML中提取表单字段"""
        fields = {}
        
        # 提取所有input字段
        input_pattern = r'<input[^>]*name=["\']([^"\']+)["\'][^>]*>'
        for match in re.finditer(input_pattern, html, re.I):
            field_name = match.group(1)
            
            # 提取value属性
            value_match = re.search(r'value=["\']([^"\']*)["\']', match.group(0), re.I)
            value = value_match.group(1) if value_match else ''
            
            fields[field_name] = value
        
        return fields
    
    def _fill_credentials(
        self,
        form_fields: Dict[str, str],
        credentials: Dict[str, str]
    ) -> Dict[str, str]:
        """填充凭证到表单字段"""
        filled = form_fields.copy()
        
        # 常见的用户名字段名
        username_fields = ['username', 'user', 'email', 'login', 'account']
        # 常见的密码字段名
        password_fields = ['password', 'pass', 'pwd']
        
        # 填充用户名
        for field in username_fields:
            if field in filled:
                filled[field] = credentials.get('username', '')
                break
        
        # 填充密码
        for field in password_fields:
            if field in filled:
                filled[field] = credentials.get('password', '')
                break
        
        return filled
