"""
AI辅助数据提取模块
支持本地LLM(Ollama)和商用API(OpenAI)双模式
"""

import os
import logging
from typing import Optional, Dict, Any, Type, List
from pydantic import BaseModel
from openai import OpenAI


class LLMExtractor:
    """
    LLM驱动的智能数据提取器
    
    支持两种模式:
    1. 本地模式: 使用Ollama部署的本地模型
    2. 商用模式: 使用OpenAI/Anthropic等商用API
    """
    
    def __init__(
        self,
        mode: str = "local",  # "local" or "commercial"
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        temperature: float = 0.1,
        max_retries: int = 3
    ):
        """
        初始化LLM提取器
        
        Args:
            mode: 运行模式 ("local" 使用Ollama, "commercial" 使用商用API)
            model: 模型名称 (local: "llama3.1:8b", commercial: "gpt-4o-mini")
            api_key: API密钥 (仅商用模式需要)
            api_base: API基础URL
            temperature: 生成温度 (越低越确定)
            max_retries: 最大重试次数
        """
        self.mode = mode
        self.temperature = temperature
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)
        
        # 设置默认模型
        if model is None:
            self.model = "llama3.1:8b" if mode == "local" else "gpt-4o-mini"
        else:
            self.model = model
        
        # 设置API配置
        if mode == "local":
            self.api_base = api_base or "http://localhost:11434/v1"
            self.api_key = "ollama"  # Ollama不需要真实API key
        else:
            self.api_base = api_base or "https://api.openai.com/v1"
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            
            if not self.api_key:
                raise ValueError("商用模式需要提供OPENAI_API_KEY环境变量或api_key参数")
        
        # 初始化OpenAI客户端 (兼容Ollama)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )
        
        self.logger.info(f"LLM提取器初始化: mode={mode}, model={self.model}, api_base={self.api_base}")
    
    def extract(
        self,
        text: str,
        schema: Type[BaseModel],
        instruction: Optional[str] = None
    ) -> Optional[BaseModel]:
        """
        从文本中提取结构化数据
        
        Args:
            text: 要提取的文本内容
            schema: Pydantic模型类,定义提取的数据结构
            instruction: 额外的提取指令
        
        Returns:
            提取的结构化数据实例,失败返回None
        """
        # 构建提示词
        schema_description = self._build_schema_description(schema)
        
        system_prompt = f"""你是一个专业的数据提取助手。
请从用户提供的文本中提取信息,并严格按照以下JSON Schema格式返回:

{schema_description}

要求:
1. 只返回JSON格式的数据,不要包含任何其他文字
2. 如果某个字段在文本中找不到,使用null
3. 确保所有字段类型正确
4. 日期使用ISO 8601格式
"""
        
        if instruction:
            system_prompt += f"\n\n额外说明: {instruction}"
        
        user_prompt = f"请从以下文本中提取数据:\n\n{text}"
        
        # 调用LLM
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temperature,
                    response_format={"type": "json_object"} if self.mode == "commercial" else None
                )
                
                # 解析响应
                content = response.choices[0].message.content
                
                # 清理可能的markdown代码块标记
                content = content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                
                # 验证并返回
                result = schema.model_validate_json(content)
                self.logger.info(f"成功提取数据 (attempt {attempt + 1})")
                return result
                
            except Exception as e:
                self.logger.warning(f"提取失败 (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt == self.max_retries - 1:
                    self.logger.error(f"达到最大重试次数,提取失败")
                    return None
        
        return None
    
    def extract_list(
        self,
        text: str,
        item_schema: Type[BaseModel],
        instruction: Optional[str] = None
    ) -> List[BaseModel]:
        """
        从文本中提取多个结构化数据项
        
        Args:
            text: 要提取的文本内容
            item_schema: 单个数据项的Pydantic模型类
            instruction: 额外的提取指令
        
        Returns:
            提取的数据项列表
        """
        # 创建一个包装模型
        class ListWrapper(BaseModel):
            items: List[item_schema]  # type: ignore
        
        result = self.extract(text, ListWrapper, instruction)
        
        if result:
            return result.items
        else:
            return []
    
    def _build_schema_description(self, schema: Type[BaseModel]) -> str:
        """构建Schema的描述文本"""
        schema_dict = schema.model_json_schema()
        
        description = f"模型名称: {schema.__name__}\n"
        
        if "description" in schema_dict:
            description += f"描述: {schema_dict['description']}\n"
        
        description += "\n字段:\n"
        
        properties = schema_dict.get("properties", {})
        required = schema_dict.get("required", [])
        
        for field_name, field_info in properties.items():
            field_type = field_info.get("type", "unknown")
            field_desc = field_info.get("description", "无描述")
            is_required = "必填" if field_name in required else "可选"
            
            description += f"  - {field_name} ({field_type}, {is_required}): {field_desc}\n"
            
            # 添加示例
            if "examples" in field_info:
                description += f"    示例: {field_info['examples']}\n"
        
        return description
    
    def validate_quality(self, text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用LLM验证提取数据的质量
        
        Args:
            text: 原始文本
            data: 提取的数据
        
        Returns:
            包含质量评分和问题的字典
        """
        prompt = f"""请评估以下数据提取的质量:

原始文本:
{text[:1000]}...

提取的数据:
{data}

请从以下维度评分(0-10):
1. 完整性: 是否提取了所有重要信息
2. 准确性: 提取的信息是否准确
3. 格式正确性: 数据格式是否符合要求

返回JSON格式:
{{
  "completeness_score": 分数,
  "accuracy_score": 分数,
  "format_score": 分数,
  "overall_score": 总分,
  "issues": ["问题1", "问题2"],
  "suggestions": ["建议1", "建议2"]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            self.logger.error(f"质量验证失败: {e}")
            return {
                "overall_score": 0,
                "issues": [str(e)]
            }


class HybridLLMExtractor(LLMExtractor):
    """
    混合模式提取器
    优先使用本地LLM,失败时自动fallback到商用API
    """
    
    def __init__(
        self,
        local_model: str = "llama3.1:8b",
        commercial_model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        quality_threshold: float = 7.0
    ):
        """
        初始化混合提取器
        
        Args:
            local_model: 本地模型名称
            commercial_model: 商用模型名称
            api_key: 商用API密钥
            quality_threshold: 质量阈值,低于此值则使用商用API重新提取
        """
        # 初始化本地提取器
        super().__init__(mode="local", model=local_model)
        
        # 初始化商用提取器
        self.commercial_extractor = LLMExtractor(
            mode="commercial",
            model=commercial_model,
            api_key=api_key
        )
        
        self.quality_threshold = quality_threshold
        self.logger.info(f"混合提取器初始化: local={local_model}, commercial={commercial_model}")
    
    def extract(
        self,
        text: str,
        schema: Type[BaseModel],
        instruction: Optional[str] = None,
        force_commercial: bool = False
    ) -> Optional[BaseModel]:
        """
        智能提取,自动选择最佳模式
        
        Args:
            text: 要提取的文本
            schema: 数据模型
            instruction: 额外指令
            force_commercial: 是否强制使用商用API
        
        Returns:
            提取的数据
        """
        if force_commercial:
            self.logger.info("强制使用商用API")
            return self.commercial_extractor.extract(text, schema, instruction)
        
        # 先尝试本地模型
        self.logger.info("尝试使用本地模型提取")
        result = super().extract(text, schema, instruction)
        
        if result is None:
            self.logger.warning("本地模型提取失败,切换到商用API")
            return self.commercial_extractor.extract(text, schema, instruction)
        
        # 验证质量
        quality = self.validate_quality(text, result.model_dump())
        overall_score = quality.get("overall_score", 0)
        
        if overall_score < self.quality_threshold:
            self.logger.warning(f"本地模型质量不达标({overall_score:.1f} < {self.quality_threshold}),切换到商用API")
            return self.commercial_extractor.extract(text, schema, instruction)
        
        self.logger.info(f"本地模型提取成功,质量评分: {overall_score:.1f}")
        return result
