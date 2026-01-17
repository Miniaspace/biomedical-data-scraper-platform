# Pagination Skill

## Description

智能翻页Skill，自动识别并生成翻页请求，支持多种翻页模式。

## Capabilities

- 自动识别"下一页"链接或按钮
- 支持链接翻页、参数翻页、offset翻页等多种模式
- 智能判断是否已到最后一页
- 生成标准化的翻页请求

## When to Use

当需要遍历多页数据时，这个Skill会自动激活并生成翻页请求。

## Pagination Strategies

1. **Link-based**: 查找HTML中的"下一页"链接
2. **Page parameter**: 增加URL中的page参数（如`?page=2`）
3. **Offset parameter**: 增加URL中的offset参数（如`?offset=20`）

## Configuration

```yaml
enabled: true
continue_on_error: true
```

## Required Context

- `html`: 页面HTML内容
- `url`: 当前页面URL
- `page_size` (optional): 每页数量，默认20

## Output

- `has_next_page`: 是否有下一页
- `next_page_url`: 下一页的URL
- `is_last_page`: 是否是最后一页
- `pagination_method`: 使用的翻页方法

## Example

```python
from common.agent_skills.skill_base import get_global_registry, SkillAgent

registry = get_global_registry()
agent = SkillAgent(registry)

context = {
    'url': 'https://example.com/data?page=1',
    'html': '<html>...<a href="?page=2">Next</a>...</html>',
    'page_size': 20
}

result = agent.execute_pipeline(context, skill_names=['pagination'])

if result['has_next_page']:
    print(f"Next page: {result['next_page_url']}")
```

## Author

Biomedical Data Scraper Team

## Version

1.0.0

## Tags

- pagination
- navigation
- crawling
