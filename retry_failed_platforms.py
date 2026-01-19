#!/usr/bin/env python3
"""
重试失败平台的批量生成脚本
"""
import subprocess
import sys
import time
from datetime import datetime

# 失败平台列表
FAILED_PLATFORMS = [
    # 第1批失败
    ("https://framinghamheartstudy.org/", "弗雷明汉心脏研究 FHS"),
    ("https://www.cardia.dopm.uab.edu/", "年轻人冠状动脉风险发展研究 CARDIA"),
    ("https://openicpsr.org", "开放社会科学数据平台 openICPSR"),
    ("https://kidsfirstdrc.org/resources", "儿童癌症数据资源平台 KFDRes"),
    ("https://alzheimersdata.org/ad-workbench/", "阿尔茨海默病数据倡议仓库 ADI Repository"),
    
    # 第2批失败
    ("https://naccdata.org", "国家阿尔茨海默病协调中心 NACC"),
    ("https://www.icpsr.umich.edu/web/pages/NACDA/", "国家老龄化数据档案 NACDA"),
    ("https://bioportal.bioontology.org", "美国国家生物医学本体中心BioPortal"),
    
    # 第3批失败
    ("https://immunespace.org", "免疫数据平台 IS"),
    ("https://neuinfo.org/", "神经科学信息框架 NIF"),
    ("https://vdjserver.org/community", "VDJServer 社区数据门户 VDJServer CDP"),
]

def retry_platform(url, name, output_dir="./generated_spiders_retry", timeout=180, max_retries=3):
    """重试单个平台"""
    print(f"\n{'='*60}")
    print(f"正在重试: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}\n")
    
    cmd = [
        "python3",
        "spider_generator/spider_generator_cli_optimized.py",
        "--url", url,
        "--name", name,
        "--output-dir", output_dir,
        "--timeout", str(timeout),
        "--max-retries", str(max_retries),
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 30,
        )
        
        if result.returncode == 0:
            print(f"✅ {name} - 生成成功")
            return True
        else:
            print(f"❌ {name} - 生成失败")
            print(f"错误: {result.stderr[-500:]}")  # 只显示最后500字符
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️ {name} - 超时")
        return False
    except Exception as e:
        print(f"❌ {name} - 异常: {str(e)}")
        return False

def main():
    print("="*60)
    print("开始重试11个失败的平台")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = {
        "success": [],
        "failed": [],
    }
    
    for i, (url, name) in enumerate(FAILED_PLATFORMS, 1):
        print(f"\n[{i}/{len(FAILED_PLATFORMS)}] 处理: {name}")
        
        success = retry_platform(url, name)
        
        if success:
            results["success"].append(name)
        else:
            results["failed"].append(name)
        
        # 避免请求过快
        if i < len(FAILED_PLATFORMS):
            time.sleep(2)
    
    # 打印最终统计
    print("\n" + "="*60)
    print("重试完成！")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print(f"\n✅ 成功: {len(results['success'])}/{len(FAILED_PLATFORMS)}")
    print(f"❌ 失败: {len(results['failed'])}/{len(FAILED_PLATFORMS)}")
    
    if results["success"]:
        print("\n成功的平台:")
        for name in results["success"]:
            print(f"  ✓ {name}")
    
    if results["failed"]:
        print("\n仍然失败的平台:")
        for name in results["failed"]:
            print(f"  ✗ {name}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
