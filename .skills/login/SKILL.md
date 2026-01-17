# Login Skill

## Description

通用登录处理Skill，自动识别和处理各种网站的登录流程。

## Capabilities

- 自动识别登录表单
- 支持用户名/密码、邮箱/密码等多种登录方式
- 提取和填充表单字段
- 保存登录后的会话和Cookies

## When to Use

当目标网站需要登录才能访问数据时，这个Skill会自动激活。

## Configuration

```yaml
enabled: true
continue_on_error: false
```

## Required Context

- `credentials`: 包含username和password的字典
- `html`: 页面HTML内容
- `url`: 当前页面URL

## Output

- `login_required`: 是否需要登录
- `login_form_data`: 填充好的表单数据
- `login_url`: 登录请求的URL
- `login_method`: 登录请求的HTTP方法

## Example

```python
from common.agent_skills.skill_base import get_global_registry, SkillAgent

# 获取全局注册表
registry = get_global_registry()

# 创建Agent
agent = SkillAgent(registry)

# 准备上下文
context = {
    'platform': 'example_platform',
    'url': 'https://example.com/login',
    'html': '<form>...</form>',
    'credentials': {
        'username': 'user@example.com',
        'password': 'password123'
    }
}

# 执行
result = agent.execute_pipeline(context, skill_names=['login'])
print(result['login_form_data'])
```

## Author

Biomedical Data Scraper Team

## Version

1.0.0

## Tags

- authentication
- login
- session
