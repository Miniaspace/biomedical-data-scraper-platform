#!/usr/bin/env python3
"""
Spider生成器CLI工具 - 优化版
自动分析网站并生成定制化的Scrapy Spider代码
增强了容错能力、并发处理和断点续传功能
"""

import asyncio
import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import traceback

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
    """Spider生成器命令行界面 - 优化版"""
    
    def __init__(self, max_retries: int = 3, timeout: int = 120):
        self.planner = AIStrategyPlanner()
        self.generator = CodeGenerator()
        self.max_retries = max_retries
        self.timeout = timeout
        
    async def generate_spider_with_retry(self,
                                        url: str,
                                        name: str,
                                        platform_type: Optional[str] = None,
                                        target_data: Optional[str] = None,
                                        output_dir: str = './generated_spiders') -> Dict[str, Any]:
        """
        带重试机制的Spider生成
        
        Args:
            url: 目标网站URL
            name: 平台名称
            platform_type: 平台类型
            target_data: 目标数据描述
            output_dir: 输出目录
            
        Returns:
            生成结果
        """
        for attempt in range(self.max_retries):
            try:
                if attempt > 0:
                    logger.info(f"第 {attempt + 1} 次尝试...")
                    await asyncio.sleep(5 * attempt)  # 指数退避
                
                result = await asyncio.wait_for(
                    self.generate_spider(url, name, platform_type, target_data, output_dir),
                    timeout=self.timeout
                )
                
                if result['success']:
                    return result
                    
            except asyncio.TimeoutError:
                logger.error(f"生成超时 (尝试 {attempt + 1}/{self.max_retries})")
                if attempt == self.max_retries - 1:
                    return {
                        'success': False,
                        'platform_name': name,
                        'url': url,
                        'files': {},
                        'errors': [f'超时: 超过 {self.timeout} 秒']
                    }
            except Exception as e:
                logger.error(f"生成失败 (尝试 {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return {
                        'success': False,
                        'platform_name': name,
                        'url': url,
                        'files': {},
                        'errors': [str(e), traceback.format_exc()]
                    }
        
        return {
            'success': False,
            'platform_name': name,
            'url': url,
            'files': {},
            'errors': ['达到最大重试次数']
        }
    
    async def generate_spider(self,
                             url: str,
                             name: str,
                             platform_type: Optional[str] = None,
                             target_data: Optional[str] = None,
                             output_dir: str = './generated_spiders') -> Dict[str, Any]:
        """
        生成Spider的完整流程
        """
        logger.info("=" * 60)
        logger.info(f"开始为 {name} 生成Spider")
        logger.info("=" * 60)
        
        result = {
            'success': False,
            'platform_name': name,
            'url': url,
            'files': {},
            'errors': [],
            'timestamp': datetime.now().isoformat()
        }
        
        analyzer = None
        
        try:
            # 步骤1: 网站分析
            logger.info("\n[步骤 1/4] 分析网站结构...")
            analyzer = WebsiteAnalyzer(url)
            analysis_result = await analyzer.analyze()
            
            if 'error' in analysis_result:
                result['errors'].append(f"网站分析失败: {analysis_result['error']}")
                logger.error(f"网站分析失败: {analysis_result['error']}")
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
            
            result['success'] = True
            result['strategy'] = strategy
            
            logger.info("\n" + "=" * 60)
            logger.info("✓ Spider生成完成！")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"生成过程中出错: {str(e)}", exc_info=True)
            result['errors'].append(str(e))
            result['errors'].append(traceback.format_exc())
        finally:
            # 清理资源
            if analyzer:
                try:
                    await analyzer.close()
                except:
                    pass
        
        return result
    
    async def batch_generate(self, 
                            excel_file: str, 
                            start_row: int = 1, 
                            end_row: Optional[int] = None,
                            output_dir: str = './generated_spiders',
                            resume: bool = True):
        """
        批量生成Spider - 支持断点续传
        
        Args:
            excel_file: Excel文件路径
            start_row: 起始行（1-based）
            end_row: 结束行（1-based，None表示到最后）
            output_dir: 输出目录
            resume: 是否从上次中断处继续
        """
        import pandas as pd
        
        logger.info(f"从Excel文件批量生成: {excel_file}")
        logger.info(f"输出目录: {output_dir}")
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 读取Excel
        df = pd.read_excel(excel_file)
        
        # 选择行范围
        if end_row:
            df = df.iloc[start_row-1:end_row]
        else:
            df = df.iloc[start_row-1:]
        
        logger.info(f"将生成 {len(df)} 个Spider (行 {start_row} 到 {end_row or len(df)})")
        
        # 加载已有结果（断点续传）
        progress_file = os.path.join(output_dir, 'batch_progress.json')
        results = []
        completed_names = set()
        
        if resume and os.path.exists(progress_file):
            try:
                with open(progress_file, 'r', encoding='utf-8') as f:
                    results = json.load(f)
                completed_names = {r['platform_name'] for r in results if r['success']}
                logger.info(f"从上次中断处继续，已完成 {len(completed_names)} 个")
            except:
                logger.warning("无法加载进度文件，从头开始")
                results = []
        
        # 处理每个平台
        success_count = 0
        failed_count = 0
        skipped_count = 0
        
        for idx, row in df.iterrows():
            # 提取平台信息
            platform_name = (row.get('平台名称') or row.get('name') or 
                           row.get('数据名称（中文+缩略名）') or row.get('数据名称（英文）'))
            platform_url = (row.get('网址') or row.get('url') or 
                          row.get('数据链接'))
            
            if not platform_name or not platform_url:
                logger.warning(f"跳过第 {idx+1} 行：缺少名称或URL")
                skipped_count += 1
                continue
            
            # 检查是否已完成
            if platform_name in completed_names:
                logger.info(f"跳过已完成: {platform_name}")
                skipped_count += 1
                continue
            
            logger.info(f"\n{'='*60}")
            logger.info(f"处理 [{idx+1-start_row+1}/{len(df)}]: {platform_name}")
            logger.info(f"URL: {platform_url}")
            logger.info(f"{'='*60}")
            
            # 生成Spider（带重试）
            result = await self.generate_spider_with_retry(
                url=platform_url,
                name=platform_name,
                output_dir=output_dir
            )
            
            results.append(result)
            
            if result['success']:
                success_count += 1
                completed_names.add(platform_name)
                logger.info(f"✓ 成功 ({success_count}/{len(df)})")
            else:
                failed_count += 1
                logger.error(f"✗ 失败 ({failed_count}/{len(df)})")
                logger.error(f"错误: {result['errors']}")
            
            # 实时保存进度
            try:
                with open(progress_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"保存进度失败: {e}")
            
            # 短暂延迟，避免请求过快
            await asyncio.sleep(2)
        
        # 生成最终报告
        logger.info("\n" + "="*60)
        logger.info("批量生成完成！")
        logger.info(f"成功: {success_count}")
        logger.info(f"失败: {failed_count}")
        logger.info(f"跳过: {skipped_count}")
        logger.info("="*60)
        
        self._generate_batch_report(results, output_dir)
        
        return results
    
    def _sanitize_name(self, name: str) -> str:
        """清理名称，用于文件名"""
        import re
        # 移除特殊字符
        name = re.sub(r'[^\w\s\-\u4e00-\u9fff]', '', name)
        # 替换空格和连字符为下划线
        name = re.sub(r'[-\s]+', '_', name)
        return name.lower()
    
    def _generate_batch_report(self, results: List[Dict], output_dir: str):
        """生成批量处理报告"""
        report = f"""# Spider批量生成报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
输出目录: {output_dir}

## 统计摘要

- **总数**: {len(results)}
- **成功**: {sum(1 for r in results if r['success'])} ✓
- **失败**: {sum(1 for r in results if not r['success'])} ✗
- **成功率**: {sum(1 for r in results if r['success']) / len(results) * 100:.1f}%

## 详细结果

| # | 平台名称 | URL | 状态 | 难度 | 方法 | 错误 |
|---|---------|-----|------|------|------|------|
"""
        
        for i, r in enumerate(results, 1):
            status = "✓" if r['success'] else "✗"
            difficulty = "⭐" * r.get('strategy', {}).get('difficulty', 0) if r['success'] else "N/A"
            method = r.get('strategy', {}).get('recommended_method', 'N/A') if r['success'] else "N/A"
            error = r['errors'][0][:50] + "..." if r['errors'] and not r['success'] else "-"
            
            report += f"| {i} | {r['platform_name']} | {r['url'][:40]}... | {status} | {difficulty} | {method} | {error} |\n"
        
        # 失败详情
        failed = [r for r in results if not r['success']]
        if failed:
            report += "\n## 失败详情\n\n"
            for r in failed:
                report += f"### {r['platform_name']}\n\n"
                report += f"- **URL**: {r['url']}\n"
                report += f"- **错误**:\n"
                for err in r['errors']:
                    report += f"  - {err}\n"
                report += "\n"
        
        # 成功统计
        successful = [r for r in results if r['success']]
        if successful:
            report += "\n## 成功统计\n\n"
            
            # 按难度分组
            by_difficulty = {}
            for r in successful:
                diff = r.get('strategy', {}).get('difficulty', 0)
                by_difficulty[diff] = by_difficulty.get(diff, 0) + 1
            
            report += "### 按难度分布\n\n"
            for diff in sorted(by_difficulty.keys()):
                report += f"- {'⭐' * diff} ({diff}星): {by_difficulty[diff]} 个\n"
            
            # 按方法分组
            by_method = {}
            for r in successful:
                method = r.get('strategy', {}).get('recommended_method', 'unknown')
                by_method[method] = by_method.get(method, 0) + 1
            
            report += "\n### 按方法分布\n\n"
            for method, count in sorted(by_method.items(), key=lambda x: x[1], reverse=True):
                report += f"- **{method}**: {count} 个\n"
        
        # 保存报告
        report_file = os.path.join(output_dir, 'BATCH_REPORT.md')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"\n批量报告已生成: {report_file}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='智能Spider生成器 - 自动分析网站并生成Scrapy采集器代码（优化版）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成单个Spider
  python spider_generator_cli_optimized.py --url "https://biolincc.nhlbi.nih.gov" --name "BioLINCC"
  
  # 批量生成（支持断点续传）
  python spider_generator_cli_optimized.py --batch-file "需求清单.xlsx" --start-row 1 --end-row 25
  
  # 从中断处继续
  python spider_generator_cli_optimized.py --batch-file "需求清单.xlsx" --start-row 1 --end-row 75 --resume
        """
    )
    
    # 单个生成模式
    parser.add_argument('--url', help='目标网站URL')
    parser.add_argument('--name', help='平台名称')
    parser.add_argument('--type', help='平台类型（可选）')
    parser.add_argument('--target-data', help='目标数据描述（可选）')
    parser.add_argument('--output-dir', default='./generated_spiders', help='输出目录')
    
    # 批量生成模式
    parser.add_argument('--batch-file', help='Excel文件路径（批量模式）')
    parser.add_argument('--start-row', type=int, default=1, help='起始行号（默认1）')
    parser.add_argument('--end-row', type=int, help='结束行号（默认到最后）')
    parser.add_argument('--resume', action='store_true', help='从上次中断处继续')
    parser.add_argument('--no-resume', dest='resume', action='store_false', help='不使用断点续传，从头开始')
    parser.set_defaults(resume=True)
    
    # 性能参数
    parser.add_argument('--max-retries', type=int, default=3, help='最大重试次数（默认3）')
    parser.add_argument('--timeout', type=int, default=120, help='单个Spider生成超时时间（秒，默认120）')
    
    args = parser.parse_args()
    
    cli = SpiderGeneratorCLI(max_retries=args.max_retries, timeout=args.timeout)
    
    if args.batch_file:
        # 批量模式
        results = asyncio.run(cli.batch_generate(
            args.batch_file,
            args.start_row,
            args.end_row,
            args.output_dir,
            args.resume
        ))
        
        success_count = sum(1 for r in results if r['success'])
        print(f"\n批量生成完成: {success_count}/{len(results)} 成功")
        
        sys.exit(0 if success_count == len(results) else 1)
        
    elif args.url and args.name:
        # 单个模式
        result = asyncio.run(cli.generate_spider_with_retry(
            url=args.url,
            name=args.name,
            platform_type=args.type,
            target_data=args.target_data,
            output_dir=args.output_dir
        ))
        
        if result['success']:
            print("\n✓ Spider生成成功！")
            print(f"\nSpider文件: {result['files']['spider']}")
            print(f"README: {result['files']['readme']}")
            sys.exit(0)
        else:
            print("\n✗ Spider生成失败")
            for error in result['errors']:
                print(f"  错误: {error}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
