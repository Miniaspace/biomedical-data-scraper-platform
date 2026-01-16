# 网站分析笔记

## BioPortal (https://bioportal.bioontology.org)

### 网站概况
- **类型**: 生物医学本体数据库
- **数据量**: 1,246个本体，17,575,783个类，36,286个属性
- **访问方式**: 公开访问，有REST API

### 数据结构
- 本体列表页: 可通过"Browse ontologies"访问
- 每个本体有详细页面
- 提供REST API进行程序化访问

### 采集策略
1. 使用REST API获取本体列表
2. 对每个本体获取详细信息
3. 提取元数据、类、属性等信息

### API文档
- 主要API endpoint: https://data.bioontology.org/
- 需要API Key进行认证

---

## National Sleep Research Resource (https://sleepdata.org)

### 网站概况
- **类型**: 睡眠研究数据平台
- **状态**: 网站当前返回502错误，可能暂时不可用

### 备注
- 需要等待网站恢复后再进行分析
- 可以先实现基础框架，后续补充具体解析逻辑

---

## Kids First Data Resource (https://kidsfirstdrc.org)

### 待分析
- 需要访问网站了解数据结构

---

## OpenICPSR (https://openicpsr.org)

### 状态
- 已实现基础spider
- 需要进一步测试和完善
