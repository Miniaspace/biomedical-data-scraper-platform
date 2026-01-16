# 深度数据提取指南

**版本**: 2.0
**日期**: 2026年1月16日

## 1. 框架能力升级概述

为了满足您对完整数据采集的需求，我们对框架进行了重大升级，现在完全支持：

- **文件下载**: 自动下载PDF、Word、Excel等所有类型的文件。
- **标准化文件组织**: 按照您要求的目录结构（`main_file`, `SI_file`, `PR_file`）存储文件。
- **深度数据提取**: 支持提取评论、同行评审及各自的附件。
- **文件完整性校验**: 自动计算每个下载文件的SHA256哈希值。

## 2. 核心增强模块

### `BiomedicalFilesPipeline`

这是我们全新的文件下载管道，它会自动处理您在`item`中提交的所有文件URL。

**如何使用**: 
1.  在您的Spider中启用它。
2.  在`item`中填充以下字段：
    - `pdf_url`: 主PDF文件的URL。
    - `supplementary_files`: 补充文件列表。
    - `peer_review_files`: 同行评审文件列表。
    - `comments`: 评论列表（可以包含附件）。

### `CommentExtractor`

这是一个通用的评论提取工具，可以轻松地从页面中提取评论和同行评审。

**如何使用**:
```python
from common.extractors import CommentExtractor

# 在您的parse方法中
extractor = CommentExtractor(response)
comments = extractor.extract_comments(
    comment_selector=\'div.comment-item\',
    author_selector=\'span.author\',
    # ... 其他选择器
)
item[\'comments\'] = comments
```

## 3. 如何实现一个完整的采集器

我们为您创建了一个名为 `complete_example_spider.py` 的全新模板，它展示了如何利用新功能来提取所有类型的数据。这是您未来开发新采集器的**最佳实践范例**。

### 关键步骤

#### 步骤1: 启用文件下载

在您的Spider中，确保`ITEM_PIPELINES`包含了`BiomedicalFilesPipeline`：

```python
class MySpider(BaseSpider):
    custom_settings = {
        **BaseSpider.custom_settings,
        \'ITEM_PIPELINES
: {
            \'common.pipeline.file_pipeline.BiomedicalFilesPipeline
: 1,
            # ...
        },
        \'FILES_STORE
: \'data/files\',
    }
```

#### 步骤2: 在`parse_detail_page`中填充所有字段

在您的解析方法中，您需要做的就是找到正确的数据并填充到`item`中。剩下的工作将由Pipeline自动完成。

```python
def parse_detail_page(self, response):
    item = self.extract_common_metadata(response)
    
    # 提取元数据
    item[\'title\'] = response.css(\'h1::text
).get()
    
    # 提取主PDF
    item[\'pdf_url\'] = response.css(\'a.pdf::attr(href)
).get()
    
    # 提取补充文件
    supplementary_files = []
    for file_elem in response.css(\'div.si-files li
):
        supplementary_files.append({
            \'url
: file_elem.css(\'a::attr(href)
).get(),
            \'filename
: file_elem.css(\'span.name::text
).get(),
        })
    item[\'supplementary_files\'] = supplementary_files
    
    # 提取评论
    extractor = CommentExtractor(response)
    item[\'comments\'] = extractor.extract_comments(...) 
    
    yield item
```

#### 步骤3: Pipeline自动处理

当您`yield item`后，`BiomedicalFilesPipeline`会自动：
1.  **解析**`item`中的所有URL字段。
2.  **下载**所有文件。
3.  **保存**到正确的目录结构中（例如 `SI_file/track_id_123/sup_1.pdf`）。
4.  **计算**每个文件的SHA256哈希值。
5.  将下载结果（路径、哈希值等）**更新**回`item`中。

最终，输出的JSONL文件将包含完整的元数据和所有相关文件的本地路径及校验信息。

## 4. 总结

通过这次框架升级，我们为您提供了一个极其强大的数据采集系统。您现在只需要专注于编写针对特定平台的**解析逻辑**，而所有复杂的文件下载、组织和管理工作都将由框架**自动完成**。

请参考 `complete_example_spider.py` 作为您未来开发所有采集器的标准模板。
