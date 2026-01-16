# 快速开始指南 - 本地运行版本

本指南帮助您在**不使用Docker**的情况下，快速在本地运行数据采集平台。

## 前置要求

- Python 3.8 或更高版本
- pip 包管理器

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/Miniaspace/biomedical-data-scraper-platform.git
cd biomedical-data-scraper-platform
```

### 2. 安装依赖

```bash
# 安装本地运行所需的依赖
pip install -r requirements-local.txt
```

### 3. 配置凭证（可选）

如果要采集需要认证的平台（如BioPortal），需要配置凭证：

```bash
# 复制凭证模板
cp config/credentials.yaml.example config/credentials.yaml

# 编辑凭证文件，填入您的API密钥
nano config/credentials.yaml
```

## 运行采集器

### 查看可用平台

```bash
python run_local.py --list
```

输出示例：
```
=== Available Platforms ===

Platform             Name                           Status     Auth      
----------------------------------------------------------------------
biolincc             BioLINCC                       Enabled    Yes       
openicpsr            OpenICPSR                      Enabled    Yes       
bioportal            BioPortal                      Enabled    Yes       
kidsfirst            Kids First Data Resource       Enabled    No        
nsrr                 NSRR                           Disabled   No        
```

### 运行单个平台

```bash
# 运行Kids First采集器（不需要认证）
python run_local.py --platform kidsfirst

# 运行BioPortal采集器（需要API key）
python run_local.py --platform bioportal
```

### 运行所有启用的平台

```bash
python run_local.py --platform all
```

### 启用详细日志

```bash
python run_local.py --platform kidsfirst --verbose
```

## 查看采集结果

采集的数据会保存在 `data/raw/` 目录下，按平台分类：

```bash
# 查看采集的数据
ls -lh data/raw/kidsfirst/
ls -lh data/raw/bioportal/

# 查看JSONL文件内容
cat data/raw/kidsfirst/*.jsonl | head -20
```

数据格式：
- **JSONL格式**: 每行一个JSON对象，便于流式处理
- **CSV格式**: 可以用Excel或其他工具打开（如果配置了CSV输出）

## 平台说明

### 1. Kids First Data Resource
- **URL**: https://kidsfirstdrc.org
- **认证**: 不需要
- **数据类型**: 儿童癌症和结构性出生缺陷研究
- **运行命令**: `python run_local.py --platform kidsfirst`

### 2. BioPortal
- **URL**: https://bioportal.bioontology.org
- **认证**: 需要API Key
- **获取API Key**: https://bioportal.bioontology.org/account
- **数据类型**: 生物医学本体
- **运行命令**: 
  ```bash
  # 方法1: 通过命令行参数
  python run_local.py --platform bioportal --api_key YOUR_KEY
  
  # 方法2: 通过环境变量
  export BIOPORTAL_API_KEY="YOUR_KEY"
  python run_local.py --platform bioportal
  
  # 方法3: 在credentials.yaml中配置
  python run_local.py --platform bioportal
  ```

### 3. OpenICPSR
- **URL**: https://openicpsr.org
- **认证**: 部分数据需要
- **数据类型**: 社会科学研究数据
- **运行命令**: `python run_local.py --platform openicpsr`

### 4. NSRR (National Sleep Research Resource)
- **URL**: https://sleepdata.org
- **认证**: 不需要
- **状态**: 网站当前可能不可用（502错误）
- **数据类型**: 睡眠研究数据
- **运行命令**: `python run_local.py --platform nsrr`

## 常见问题

### Q: 如何添加新的平台？

A: 使用辅助脚本：

```bash
python scripts/add_platform.py new_platform_name
```

然后编辑生成的spider文件，实现解析逻辑。

### Q: 采集速度太慢怎么办？

A: 可以调整并发设置。编辑对应spider的`custom_settings`：

```python
custom_settings = {
    'CONCURRENT_REQUESTS': 16,  # 增加并发请求数
    'DOWNLOAD_DELAY': 1,        # 减少延迟（注意遵守网站规则）
}
```

### Q: 如何只采集部分数据？

A: 可以修改spider的`start_urls`或添加过滤逻辑。例如：

```python
def parse_list_page(self, response):
    # 只处理前10个链接
    for link in response.css('a.dataset::attr(href)').getall()[:10]:
        yield scrapy.Request(...)
```

### Q: 遇到错误怎么办？

A: 查看日志文件，或使用`--verbose`参数获取详细信息：

```bash
python run_local.py --platform kidsfirst --verbose 2>&1 | tee scraping.log
```

## 下一步

- 查看 [添加新平台指南](docs/adding_new_platform.md) 了解如何扩展平台
- 查看 [架构文档](docs/architecture.md) 了解系统设计
- 查看 [部署指南](docs/deployment.md) 了解生产环境部署

## 技术支持

如有问题，请在GitHub仓库提交Issue：
https://github.com/Miniaspace/biomedical-data-scraper-platform/issues
