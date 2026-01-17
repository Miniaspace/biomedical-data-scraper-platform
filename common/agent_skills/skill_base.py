"""
Agent Skills 核心框架

基于业界标准的SKILL.md格式，为数据采集平台提供插件化的能力模块
"""

import os
import yaml
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from pathlib import Path


@dataclass
class SkillMetadata:
    """Skill元数据"""
    name: str
    version: str
    description: str
    author: str = "Unknown"
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    priority: int = 50  # 0-100, 数字越大优先级越高


class BaseSkill(ABC):
    """
    Skill基类
    
    所有Skills都应该继承这个基类并实现核心方法
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化Skill
        
        Args:
            config: Skill配置
        """
        self.config = config or {}
        self.logger = logging.getLogger(f"skill.{self.metadata.name}")
        self.enabled = self.config.get('enabled', True)
    
    @property
    @abstractmethod
    def metadata(self) -> SkillMetadata:
        """返回Skill的元数据"""
        pass
    
    @abstractmethod
    def can_handle(self, context: Dict[str, Any]) -> bool:
        """
        判断这个Skill是否能处理当前上下文
        
        Args:
            context: 上下文信息（如URL、HTML、响应等）
        
        Returns:
            True if this skill can handle the context
        """
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行Skill的核心逻辑
        
        Args:
            context: 输入上下文
        
        Returns:
            执行结果
        """
        pass
    
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        return True
    
    def on_success(self, result: Dict[str, Any]):
        """成功回调"""
        self.logger.info(f"Skill {self.metadata.name} executed successfully")
    
    def on_failure(self, error: Exception):
        """失败回调"""
        self.logger.error(f"Skill {self.metadata.name} failed: {error}")


class SkillRegistry:
    """
    Skill注册表
    
    管理所有可用的Skills
    """
    
    def __init__(self):
        self.skills: Dict[str, BaseSkill] = {}
        self.logger = logging.getLogger(__name__)
    
    def register(self, skill: BaseSkill):
        """注册一个Skill"""
        name = skill.metadata.name
        if name in self.skills:
            self.logger.warning(f"Skill {name} already registered, overwriting")
        self.skills[name] = skill
        self.logger.info(f"Registered skill: {name}")
    
    def unregister(self, name: str):
        """注销一个Skill"""
        if name in self.skills:
            del self.skills[name]
            self.logger.info(f"Unregistered skill: {name}")
    
    def get_skill(self, name: str) -> Optional[BaseSkill]:
        """获取指定名称的Skill"""
        return self.skills.get(name)
    
    def get_all_skills(self) -> List[BaseSkill]:
        """获取所有已注册的Skills"""
        return list(self.skills.values())
    
    def get_skills_by_tag(self, tag: str) -> List[BaseSkill]:
        """根据标签获取Skills"""
        return [
            skill for skill in self.skills.values()
            if tag in skill.metadata.tags
        ]
    
    def find_applicable_skills(self, context: Dict[str, Any]) -> List[BaseSkill]:
        """
        找到所有能处理当前上下文的Skills
        
        Args:
            context: 上下文信息
        
        Returns:
            按优先级排序的Skills列表
        """
        applicable = [
            skill for skill in self.skills.values()
            if skill.enabled and skill.can_handle(context)
        ]
        
        # 按优先级排序
        applicable.sort(key=lambda s: s.metadata.priority, reverse=True)
        
        return applicable


class SkillLoader:
    """
    Skill加载器
    
    从文件系统加载Skills
    """
    
    def __init__(self, skills_dir: str = "./.skills"):
        """
        初始化加载器
        
        Args:
            skills_dir: Skills目录路径
        """
        self.skills_dir = Path(skills_dir)
        self.logger = logging.getLogger(__name__)
    
    def load_all_skills(self, registry: SkillRegistry):
        """
        加载所有Skills
        
        Args:
            registry: Skill注册表
        """
        if not self.skills_dir.exists():
            self.logger.warning(f"Skills directory not found: {self.skills_dir}")
            return
        
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                self._load_skill_from_dir(skill_dir, registry)
    
    def _load_skill_from_dir(self, skill_dir: Path, registry: SkillRegistry):
        """从目录加载单个Skill"""
        skill_md = skill_dir / "SKILL.md"
        skill_py = skill_dir / "skill.py"
        
        if not skill_md.exists():
            self.logger.warning(f"SKILL.md not found in {skill_dir}")
            return
        
        if not skill_py.exists():
            self.logger.warning(f"skill.py not found in {skill_dir}")
            return
        
        try:
            # 动态导入skill.py
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                f"skill_{skill_dir.name}",
                skill_py
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 查找BaseSkill的子类
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BaseSkill) and 
                    attr is not BaseSkill):
                    # 实例化并注册
                    skill_instance = attr()
                    registry.register(skill_instance)
                    break
            
        except Exception as e:
            self.logger.error(f"Failed to load skill from {skill_dir}: {e}")


class SkillAgent:
    """
    Skill Agent
    
    智能编排和执行Skills
    """
    
    def __init__(self, registry: SkillRegistry):
        """
        初始化Agent
        
        Args:
            registry: Skill注册表
        """
        self.registry = registry
        self.logger = logging.getLogger(__name__)
    
    def execute_pipeline(
        self,
        context: Dict[str, Any],
        skill_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        执行Skill流水线
        
        Args:
            context: 初始上下文
            skill_names: 指定要执行的Skills（如果为None，则自动选择）
        
        Returns:
            最终结果
        """
        # 如果指定了Skills，使用指定的；否则自动选择
        if skill_names:
            skills = [
                self.registry.get_skill(name)
                for name in skill_names
                if self.registry.get_skill(name)
            ]
        else:
            skills = self.registry.find_applicable_skills(context)
        
        if not skills:
            self.logger.warning("No applicable skills found")
            return context
        
        self.logger.info(f"Executing {len(skills)} skills")
        
        # 依次执行每个Skill
        result = context.copy()
        for skill in skills:
            try:
                self.logger.info(f"Executing skill: {skill.metadata.name}")
                skill_result = skill.execute(result)
                
                # 合并结果到上下文
                result.update(skill_result)
                
                skill.on_success(skill_result)
                
            except Exception as e:
                self.logger.error(f"Skill {skill.metadata.name} failed: {e}")
                skill.on_failure(e)
                
                # 根据配置决定是否继续
                if not self.registry.get_skill(skill.metadata.name).config.get('continue_on_error', False):
                    raise
        
        return result
    
    def suggest_skills(self, context: Dict[str, Any]) -> List[str]:
        """
        根据上下文建议使用哪些Skills
        
        Args:
            context: 上下文信息
        
        Returns:
            建议的Skill名称列表
        """
        applicable_skills = self.registry.find_applicable_skills(context)
        return [skill.metadata.name for skill in applicable_skills]


# 全局注册表实例
_global_registry = SkillRegistry()


def get_global_registry() -> SkillRegistry:
    """获取全局Skill注册表"""
    return _global_registry
