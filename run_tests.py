#!/usr/bin/env python3
"""
AutoCheckBJMF 增强版测试运行器
"""
import os
import sys
import unittest
import argparse
import time
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def discover_tests(test_dir='tests', pattern='test_*.py'):
    """发现测试用例"""
    loader = unittest.TestLoader()
    start_dir = os.path.join(project_root, test_dir)
    
    if not os.path.exists(start_dir):
        print(f"❌ 测试目录不存在: {start_dir}")
        return None
    
    suite = loader.discover(start_dir, pattern=pattern)
    return suite

def run_tests(suite, verbosity=2):
    """运行测试"""
    runner = unittest.TextTestRunner(
        verbosity=verbosity,
        stream=sys.stdout,
        buffer=True
    )
    
    print("🚀 开始运行测试...")
    print("=" * 70)
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    print("=" * 70)
    print(f"⏱️ 测试运行时间: {end_time - start_time:.2f} 秒")
    
    return result

def print_test_summary(result):
    """打印测试摘要"""
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    
    print("\n📊 测试摘要:")
    print(f"   总测试数: {total_tests}")
    print(f"   成功: {total_tests - failures - errors}")
    print(f"   失败: {failures}")
    print(f"   错误: {errors}")
    print(f"   跳过: {skipped}")
    
    if result.wasSuccessful():
        print("\n🎉 所有测试通过！")
        return True
    else:
        print("\n❌ 测试失败！")
        
        if failures:
            print(f"\n💥 失败的测试 ({failures}):")
            for i, (test, traceback) in enumerate(result.failures, 1):
                print(f"  {i}. {test}")
                print(f"     {traceback.split('AssertionError:')[-1].strip()}")
        
        if errors:
            print(f"\n🚨 错误的测试 ({errors}):")
            for i, (test, traceback) in enumerate(result.errors, 1):
                print(f"  {i}. {test}")
                error_line = traceback.split('\n')[-2] if '\n' in traceback else traceback
                print(f"     {error_line.strip()}")
        
        return False

def check_dependencies():
    """检查测试依赖"""
    print("🔍 检查测试依赖...")
    
    required_modules = [
        'unittest',
        'tempfile',
        'json',
        'os',
        'sys'
    ]
    
    optional_modules = [
        'requests',
        'beautifulsoup4',
        'cryptography',
        'selenium'
    ]
    
    missing_required = []
    missing_optional = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_required.append(module)
    
    for module in optional_modules:
        try:
            __import__(module.replace('-', '_'))
        except ImportError:
            missing_optional.append(module)
    
    if missing_required:
        print(f"❌ 缺少必需模块: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        print(f"⚠️ 缺少可选模块: {', '.join(missing_optional)}")
        print("   某些测试可能会跳过")
    
    print("✅ 依赖检查完成")
    return True

def run_specific_test(test_name):
    """运行特定测试"""
    try:
        # 尝试导入并运行特定测试
        if '.' in test_name:
            module_name, class_name = test_name.rsplit('.', 1)
        else:
            module_name = test_name
            class_name = None
        
        # 导入测试模块
        test_module = __import__(f'tests.{module_name}', fromlist=[module_name])
        
        if class_name:
            # 运行特定测试类
            test_class = getattr(test_module, class_name)
            suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        else:
            # 运行整个模块
            suite = unittest.TestLoader().loadTestsFromModule(test_module)
        
        return run_tests(suite)
    
    except ImportError as e:
        print(f"❌ 无法导入测试模块: {e}")
        return None
    except AttributeError as e:
        print(f"❌ 无法找到测试类: {e}")
        return None

def generate_coverage_report():
    """生成覆盖率报告"""
    try:
        import coverage
        
        print("📈 生成覆盖率报告...")
        
        cov = coverage.Coverage()
        cov.start()
        
        # 运行测试
        suite = discover_tests()
        if suite:
            runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
            runner.run(suite)
        
        cov.stop()
        cov.save()
        
        # 生成报告
        print("\n📊 覆盖率报告:")
        cov.report()
        
        # 生成HTML报告
        html_dir = os.path.join(project_root, 'htmlcov')
        cov.html_report(directory=html_dir)
        print(f"📄 HTML报告已生成: {html_dir}/index.html")
        
    except ImportError:
        print("⚠️ 未安装coverage模块，跳过覆盖率报告")
        print("   安装命令: pip install coverage")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AutoCheckBJMF 增强版测试运行器')
    parser.add_argument(
        '--test', '-t',
        help='运行特定测试 (例如: test_main_enhanced.TestEnhancedAutoCheckBJMF)'
    )
    parser.add_argument(
        '--pattern', '-p',
        default='test_*.py',
        help='测试文件匹配模式 (默认: test_*.py)'
    )
    parser.add_argument(
        '--verbosity', '-v',
        type=int,
        default=2,
        choices=[0, 1, 2],
        help='输出详细程度 (0=静默, 1=正常, 2=详细)'
    )
    parser.add_argument(
        '--coverage', '-c',
        action='store_true',
        help='生成覆盖率报告'
    )
    parser.add_argument(
        '--check-deps',
        action='store_true',
        help='仅检查依赖，不运行测试'
    )
    
    args = parser.parse_args()
    
    print("🧪 AutoCheckBJMF 增强版测试运行器")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    if args.check_deps:
        print("✅ 依赖检查完成，退出")
        return
    
    # 运行测试
    if args.test:
        # 运行特定测试
        result = run_specific_test(args.test)
    else:
        # 发现并运行所有测试
        suite = discover_tests(pattern=args.pattern)
        if not suite:
            sys.exit(1)
        
        result = run_tests(suite, args.verbosity)
    
    if result is None:
        sys.exit(1)
    
    # 打印摘要
    success = print_test_summary(result)
    
    # 生成覆盖率报告
    if args.coverage:
        generate_coverage_report()
    
    # 退出码
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试运行器发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
