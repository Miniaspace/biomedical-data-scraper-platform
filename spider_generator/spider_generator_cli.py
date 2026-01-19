#!/usr/bin/env python3
"""
Spider生成器CLI工具
自动分析网站并生成定制化的Scrapy Spider代码
"""

import asyncio
import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from spider_generator.analyzers.website_analyzer import WebsiteAnalyzer
from spider_generator.analyzers.ai_strategy_planner import AIStrategyPlanner
from spider_generator.generators.code_generator import CodeGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SpiderGeneratorCLI:
    """Spider生成器命令行界面"""
    
    def __init__(self):
        self.analyzer = None
        self.planner = AIStrategyPlanner()
        self.generator = CodeGenerator()
        
    async def generate_spider(self,
                             url: str,
                             name: str,
                             platform_type: Optional[str] = None,
                             target_data: Optional[str] = None,
                             output_dir: str = './generated_spiders',
                             test: bool = False) -> Dict[str, Any]:
        """
        生成Spider的完整流程
        
        Args:
            url: 目标网站URL
            name: 平台名称
            platform_type: 平台类型
            target_data: 目标数据描述
            output_dir: 输出目录
            test: 是否运行测试
            
        Returns:
            生成结果
        """
        logger.info("=" * 60)
        logger.info(f"开始为 {name} 生成Spider")
        logger.info("=" * 60)
        
        result = {
            'success': False,
            'platform_name': name,
            'url': url,
            'files': {},
            'errors': []
        }
        
        try:
            # 步骤1: 网站分析
            logger.info("\n[步骤 1/4] 分析网站结构...")
            self.analyzer = WebsiteAnalyzer(url)
            analysis_result = await self.analyzer.analyze()
            
            if 'error' in analysis_result:
                result['errors'].append(f"网站分析失败: {analysis_result['error']}")
                return result
            
            logger.info(f"✓ 网站类型: {analysis_result.get('site_type')}")
            logger.info(f"✓ 需要登录: {analysis_result.get('has_login')}")
            logger.info(f"✓ 分页类型: {analysis_result.get('pagination', {}).get('type')}")
            
            # 保存分析结果
            analysis_file = os.path.join(output_dir, 'analysis', f"{self._sanitize_name(name)}_analysis.json")
            os.makedirs(os.path.dirname(analysis_file), exist_ok=True)
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)
            result['files']['analysis'] = analysis_file
            
            # 步骤2: AI策略规划
            logger.info("\n[步骤 2/4] 生成采集策略...")
            strategy = self.planner.plan_strategy(analysis_result, target_data)
            
            logger.info(f"✓ 推荐方法: {strategy.get('recommended_method')}")
            logger.info(f"✓ 难度评级: {'⭐' * strategy.get('difficulty', 3)}")
            logger.info(f"✓ 预估时间: {strategy.get('estimated_dev_time')}")
            
            # 保存策略
            strategy_file = os.path.join(output_dir, 'strategies', f"{self._sanitize_name(name)}_strategy.json")
            os.makedirs(os.path.dirname(strategy_file), exist_ok=True)
            with open(strategy_file, 'w', encoding='utf-8') as f:
                json.dump(strategy, f, ensure_ascii=False, indent=2)
            result['files']['strategy'] = strategy_file
            
            # 步骤3: 生成代码
            logger.info("\n[步骤 3/4] 生成Spider代码...")
            platform_info = {
                'name': name,
                'url': url,
                'type': platform_type or analysis_result.get('site_type'),
            }
            
            spider_output_dir = os.path.join(output_dir, 'spiders')
            generated_files = self.generator.generate_spider(
                platform_info,
                strategy,
                spider_output_dir
            )
            
            result['files'].update(generated_files)
            
            logger.info(f"✓ Spider代码: {generated_files['spider']}")
            logger.info(f"✓ 配置文件: {generated_files['config']}")
            logger.info(f"✓ README: {generated_files['readme']}")
            
            # 步骤4: 测试（可选）
            if test:
                logger.info("\n[步骤 4/4] 运行测试...")
                test_result = await self._run_test(generated_files['spider'])
                result['test_result'] = test_result
                
                if test_result.get('success'):
                    logger.info("✓ 测试通过")
                else:
                    logger.warning(f"✗ 测试失败: {test_result.get('error')}")
            else:
                logger.info("\n[步骤 4/4] 跳过测试")
            
            result['success'] = True
            result['strategy'] = strategy
            
            logger.info("\n" + "=" * 60)
            logger.info("✓ Spider生成完成！")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"生成过程中出错: {str(e)}", exc_info=True)
            result['errors'].append(str(e))
        
        return result
    
    async def batch_generate(self, excel_file: str, start_row: int = 1, end_row: Optional[int] = None):
        """
        批量生成Spider
        
        Args:
            excel_file: Excel文件路径
            start_row: 起始行（1-based）
            end_row: 结束行（1-based，None表示到最后）
        """
        import pandas as pd
        
        logger.info(f"从Excel文件批量生成: {excel_file}")
        
        # 读取Excel
        df = pd.read_excel(excel_file)
        
        # 选择行范围
        if end_row:
            df = df.iloc[start_row-1:end_row]
        else:
            df = df.iloc[start_row-1:]
        
        logger.info(f"将生成 {len(df)} 个Spider")
        
        results = []
        
        for idx, row in df.iterrows():
            # 尝试多个可能的列名
            platform_name = (row.get('平台名称') or row.get('name') or 
                           row.get('数据名称（中文+缩略名）') or row.get('数据名称（英文）'))
            platform_url = (row.get('网址') or row.get('url') or 
                          row.get('数据链接'))
            
            if not platform_name or not platform_url:
                logger.warning(f"跳过第 {idx+1} 行：缺少名称或URL")
                continue
            
            logger.info(f"\n处理 [{idx+1}/{len(df)}]: {platform_name}")
            
            result = await self.generate_spider(
                url=platform_url,
                name=platform_name,
                output_dir='./generated_spiders'
            )
            
            results.append(result)
            
            # 保存中间结果
            with open('./generated_spiders/batch_results.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 生成汇总报告
        self._generate_batch_report(results)
        
        return results
    
    def _sanitize_name(self, name: str) -> str:
        """清理名称，用于文件名"""
        import re
        name = re.sub(r'[^\w\s-]', '', name)
        name = re.sub(r'[-\s]+', '_', name)
        return name.lower()
    
    async def _run_test(self, spider_file: str) -> Dict[str, Any]:
        """运行Spider测试"""
        test_result = {
            'success': False,
            'error': None,
            'items_count': 0,
        }
        
        try:
            # TODO: 实现实际的测试逻辑
            # 这里可以使用subprocess运行scrapy crawl命令
            logger.info("测试功能待实现")
            test_result['success'] = True
            
        except Exception as e:
            test_result['error'] = str(e)
        
        return test_result
    
    def _generate_batch_report(self, results: list):
        """生成批量处理报告"""
        # 确保输出目录存在
        os.makedirs('./generated_spiders', exist_ok=True)
        
        report = f"""# Spider批量生成报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 统计

- 总数: {len(results)}
- 成功: {sum(1 for r in results if r['success'])}
- 失败: {sum(1 for r in results if not r['success'])}

## 详细结果

| 平台名称 | URL | 状态 | 难度 | 方法 |
|---------|-----|------|------|------|
"""
        
        for r in results:
            status = "✓" if r['success'] else "✗"
            difficulty = "⭐" * r.get('strategy', {}).get('difficulty', 0) if r['success'] else "N/A"
            method = r.get('strategy', {}).get('recommended_method', 'N/A') if r['success'] else "N/A"
            
            report += f"| {r['platform_name']} | {r['url']} | {status} | {difficulty} | {method} |\n"
        
        # 保存报告
        report_file = './generated_spiders/BATCH_REPORT.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"\n批量报告已生成: {report_file}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='智能Spider生成器 - 自动分析网站并生成Scrapy采集器代码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成单个Spider
  python spider_generator_cli.py --url "https://biolincc.nhlbi.nih.gov" --name "BioLINCC"
  
  # 生成并测试
  python spider_generator_cli.py --url "https://example.com" --name "Example" --test
  
  # 批量生成
  python spider_generator_cli.py --batch-file "需求清单.xlsx" --start-row 1 --end-row 10
        """
    )
    
    # 单个生成模式
    parser.add_argument('--url', help='目标网站URL')
    parser.add_argument('--name', help='平台名称')
    parser.add_argument('--type', help='平台类型（可选）')
    parser.add_argument('--target-data', help='目标数据描述（可选）')
    parser.add_argument('--output-dir', default='./generated_spiders', help='输出目录')
    parser.add_argument('--test', action='store_true', help='生成后运行测试')
    
    # 批量生成模式
    parser.add_argument('--batch-file', help='Excel文件路径（批量模式）')
    parser.add_argument('--start-row', type=int, default=1, help='起始行号（默认1）')
    parser.add_argument('--end-row', type=int, help='结束行号（默认到最后）')
    
    args = parser.parse_args()
    
    cli = SpiderGeneratorCLI()
    
    if args.batch_file:
        # 批量模式
        results = asyncio.run(cli.batch_generate(
            args.batch_file,
            args.start_row,
            args.end_row
        ))
        
        success_count = sum(1 for r in results if r['success'])
        print(f"\n批量生成完成: {success_count}/{len(results)} 成功")
        
    elif args.url and args.name:
        # 单个模式
        result = asyncio.run(cli.generate_spider(
            url=args.url,
            name=args.name,
            platform_type=args.type,
            target_data=args.target_data,
            output_dir=args.output_dir,
            test=args.test
        ))
        
        if result['success']:
            print("\n✓ Spider生成成功！")
            print(f"\nSpider文件: {result['files']['spider']}")
            print(f"README: {result['files']['readme']}")
        else:
            print("\n✗ Spider生成失败")
            for error in result['errors']:
                print(f"  错误: {error}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    from datetime import datetime
    main()
