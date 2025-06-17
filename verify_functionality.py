#!/usr/bin/env python3
"""
AutoCheckBJMF 增强版功能验证脚本
验证所有核心功能是否正常工作
"""
import os
import sys
import json
import time
import tempfile
import unittest
from unittest.mock import Mock, patch
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class FunctionalityVerifier:
    """功能验证器"""
    
    def __init__(self):
        self.results = {}
        self.temp_dir = tempfile.mkdtemp()
        print("🔍 AutoCheckBJMF 增强版功能验证")
        print("=" * 50)
    
    def verify_module_imports(self):
        """验证模块导入"""
        print("📦 验证模块导入...")
        
        modules_to_test = [
            ('main_enhanced', 'EnhancedAutoCheckBJMF'),
            ('modules.secure_storage', 'SecureStorage'),
            ('modules.location_manager', 'LocationManager'),
            ('modules.browser_cookie_extractor', 'BrowserCookieExtractor'),
            ('modules.auto_login', 'AutoLogin'),
            ('modules.class_detector', 'ClassDetector'),
            ('modules.gui_config', 'ConfigWizard')
        ]
        
        import_results = {}
        
        for module_name, class_name in modules_to_test:
            try:
                module = __import__(module_name, fromlist=[class_name])
                cls = getattr(module, class_name)
                import_results[f"{module_name}.{class_name}"] = "✅ 成功"
                print(f"  ✅ {module_name}.{class_name}")
            except ImportError as e:
                import_results[f"{module_name}.{class_name}"] = f"❌ 导入失败: {e}"
                print(f"  ❌ {module_name}.{class_name} - 导入失败: {e}")
            except AttributeError as e:
                import_results[f"{module_name}.{class_name}"] = f"❌ 类不存在: {e}"
                print(f"  ❌ {module_name}.{class_name} - 类不存在: {e}")
            except Exception as e:
                import_results[f"{module_name}.{class_name}"] = f"❌ 未知错误: {e}"
                print(f"  ❌ {module_name}.{class_name} - 未知错误: {e}")
        
        self.results['module_imports'] = import_results
        return all("成功" in result for result in import_results.values())
    
    def verify_secure_storage(self):
        """验证安全存储功能"""
        print("\n🔒 验证安全存储功能...")
        
        try:
            from modules.secure_storage import SecureStorage
            
            # 创建临时存储
            storage = SecureStorage("TestApp")
            storage.storage_path = self.temp_dir
            storage.key_file = os.path.join(self.temp_dir, "test.key")
            storage.data_file = os.path.join(self.temp_dir, "test_data.enc")
            storage.cipher = storage._get_or_create_cipher()
            
            # 测试数据保存和加载
            test_data = {
                'test_key': 'test_value',
                'chinese': '中文测试',
                'number': 123,
                'list': [1, 2, 3]
            }
            
            # 保存数据
            save_result = storage.save_data(test_data)
            if not save_result:
                print("  ❌ 数据保存失败")
                self.results['secure_storage'] = "❌ 数据保存失败"
                return False
            
            # 加载数据
            loaded_data = storage.load_data()
            if not loaded_data:
                print("  ❌ 数据加载失败")
                self.results['secure_storage'] = "❌ 数据加载失败"
                return False
            
            # 验证数据完整性
            if loaded_data['test_key'] != test_data['test_key']:
                print("  ❌ 数据完整性验证失败")
                self.results['secure_storage'] = "❌ 数据完整性验证失败"
                return False
            
            # 测试Unicode支持
            if loaded_data['chinese'] != test_data['chinese']:
                print("  ❌ Unicode支持验证失败")
                self.results['secure_storage'] = "❌ Unicode支持验证失败"
                return False
            
            print("  ✅ 安全存储功能正常")
            self.results['secure_storage'] = "✅ 功能正常"
            return True
            
        except Exception as e:
            print(f"  ❌ 安全存储验证失败: {e}")
            self.results['secure_storage'] = f"❌ 验证失败: {e}"
            return False
    
    def verify_location_manager(self):
        """验证位置管理功能"""
        print("\n📍 验证位置管理功能...")
        
        try:
            from modules.location_manager import LocationManager
            
            manager = LocationManager()
            
            # 测试IP定位（Mock网络请求）
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'status': 'success',
                    'lat': 39.904697,
                    'lon': 116.407178,
                    'city': 'Beijing',
                    'regionName': 'Beijing',
                    'country': 'China'
                }
                mock_get.return_value = mock_response
                
                location = manager.get_location_by_ip()
                
                if not location:
                    print("  ❌ IP定位功能失败")
                    self.results['location_manager'] = "❌ IP定位功能失败"
                    return False
                
                if location['lat'] != 39.904697 or location['lng'] != 116.407178:
                    print("  ❌ IP定位数据错误")
                    self.results['location_manager'] = "❌ IP定位数据错误"
                    return False
            
            # 测试默认位置
            with patch.object(manager, 'get_system_location') as mock_system, \
                 patch.object(manager, 'get_location_by_ip') as mock_ip, \
                 patch.object(manager, 'manual_location_picker') as mock_manual:
                
                mock_system.return_value = None
                mock_ip.return_value = None
                mock_manual.return_value = None
                
                default_location = manager.get_best_location()
                
                if not default_location or default_location['source'] != '默认位置':
                    print("  ❌ 默认位置功能失败")
                    self.results['location_manager'] = "❌ 默认位置功能失败"
                    return False
            
            print("  ✅ 位置管理功能正常")
            self.results['location_manager'] = "✅ 功能正常"
            return True
            
        except Exception as e:
            print(f"  ❌ 位置管理验证失败: {e}")
            self.results['location_manager'] = f"❌ 验证失败: {e}"
            return False
    
    def verify_cookie_manager(self):
        """验证Cookie管理功能"""
        print("\n🍪 验证Cookie管理功能...")
        
        try:
            from modules.secure_storage import CookieManager
            
            # 创建临时Cookie管理器
            manager = CookieManager()
            manager.storage.storage_path = self.temp_dir
            manager.storage.key_file = os.path.join(self.temp_dir, "cookie_test.key")
            manager.storage.data_file = os.path.join(self.temp_dir, "cookie_test_data.enc")
            manager.storage.cipher = manager.storage._get_or_create_cipher()
            
            # 测试Cookie保存和加载
            test_cookies = [
                'username=test1;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie1',
                'username=test2;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie2'
            ]
            
            user_info = {
                'class_id': '12345',
                'location': {'lat': 39.904697, 'lng': 116.407178}
            }
            
            # Mock Cookie验证
            with patch.object(manager, 'validate_cookie') as mock_validate:
                mock_validate.return_value = True
                
                # 保存Cookie
                save_result = manager.save_cookies(test_cookies, user_info)
                if not save_result:
                    print("  ❌ Cookie保存失败")
                    self.results['cookie_manager'] = "❌ Cookie保存失败"
                    return False
                
                # 加载Cookie
                loaded_cookies = manager.load_cookies()
                if len(loaded_cookies) != 2:
                    print("  ❌ Cookie加载数量错误")
                    self.results['cookie_manager'] = "❌ Cookie加载数量错误"
                    return False
                
                # 验证Cookie内容
                if 'username=test1' not in loaded_cookies[0]:
                    print("  ❌ Cookie内容验证失败")
                    self.results['cookie_manager'] = "❌ Cookie内容验证失败"
                    return False
                
                # 获取用户信息
                loaded_info = manager.get_user_info()
                if loaded_info['class_id'] != '12345':
                    print("  ❌ 用户信息验证失败")
                    self.results['cookie_manager'] = "❌ 用户信息验证失败"
                    return False
            
            print("  ✅ Cookie管理功能正常")
            self.results['cookie_manager'] = "✅ 功能正常"
            return True
            
        except Exception as e:
            print(f"  ❌ Cookie管理验证失败: {e}")
            self.results['cookie_manager'] = f"❌ 验证失败: {e}"
            return False
    
    def verify_main_application(self):
        """验证主应用程序功能"""
        print("\n🚀 验证主应用程序功能...")
        
        try:
            from main_enhanced import EnhancedAutoCheckBJMF
            
            # 创建应用实例
            app = EnhancedAutoCheckBJMF()
            app.current_directory = self.temp_dir
            app.config_file = os.path.join(self.temp_dir, "test_config.json")
            
            # 测试配置验证
            valid_config = {
                'class': '12345',
                'lat': '39.904697',
                'lng': '116.407178',
                'acc': '100',
                'cookie': ['username=test;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie'],
                'scheduletime': '08:30',
                'pushplus': '',
                'debug': False,
                'configLock': True
            }
            
            if not app._validate_json_config(valid_config):
                print("  ❌ 有效配置验证失败")
                self.results['main_application'] = "❌ 有效配置验证失败"
                return False
            
            # 测试无效配置
            invalid_config = {
                'class': '12345',
                'lat': '999',  # 无效纬度
                'lng': '116.407178',
                'acc': '100',
                'cookie': ['invalid_cookie'],
                'scheduletime': '8:30',  # 无效时间格式
            }
            
            if app._validate_json_config(invalid_config):
                print("  ❌ 无效配置应该被拒绝")
                self.results['main_application'] = "❌ 无效配置应该被拒绝"
                return False
            
            # 测试坐标偏移
            original_lat = 39.904697
            modified_lat = app.modify_decimal_part(original_lat)
            
            if not isinstance(modified_lat, float):
                print("  ❌ 坐标偏移返回类型错误")
                self.results['main_application'] = "❌ 坐标偏移返回类型错误"
                return False
            
            if abs(modified_lat - original_lat) > 0.01:
                print("  ❌ 坐标偏移幅度过大")
                self.results['main_application'] = "❌ 坐标偏移幅度过大"
                return False
            
            print("  ✅ 主应用程序功能正常")
            self.results['main_application'] = "✅ 功能正常"
            return True
            
        except Exception as e:
            print(f"  ❌ 主应用程序验证失败: {e}")
            self.results['main_application'] = f"❌ 验证失败: {e}"
            return False
    
    def verify_signing_functionality(self):
        """验证签到功能"""
        print("\n📝 验证签到功能...")
        
        try:
            from main_enhanced import EnhancedAutoCheckBJMF
            
            app = EnhancedAutoCheckBJMF()
            app.config = {
                'class': '12345',
                'lat': '39.904697',
                'lng': '116.407178',
                'acc': '100'
            }
            
            # Mock HTTP请求
            with patch('requests.get') as mock_get, \
                 patch('requests.post') as mock_post:
                
                # Mock签到页面响应
                mock_get_response = Mock()
                mock_get_response.status_code = 200
                mock_get_response.text = '''
                <html>
                    <title>课程页面</title>
                    <script>punch_gps(67890)</script>
                </html>
                '''
                mock_get.return_value = mock_get_response
                
                # Mock签到请求响应
                mock_post_response = Mock()
                mock_post_response.status_code = 200
                mock_post_response.text = '<div id="title">签到成功</div>'
                mock_post.return_value = mock_post_response
                
                # 测试签到
                test_cookies = ['username=test;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=test_cookie']
                error_cookies, null_cookie = app.qiandao(test_cookies)
                
                if len(error_cookies) > 0:
                    print("  ❌ 签到过程中出现错误")
                    self.results['signing_functionality'] = "❌ 签到过程中出现错误"
                    return False
                
                if null_cookie > 0:
                    print("  ❌ Cookie格式验证失败")
                    self.results['signing_functionality'] = "❌ Cookie格式验证失败"
                    return False
            
            print("  ✅ 签到功能正常")
            self.results['signing_functionality'] = "✅ 功能正常"
            return True
            
        except Exception as e:
            print(f"  ❌ 签到功能验证失败: {e}")
            self.results['signing_functionality'] = f"❌ 验证失败: {e}"
            return False
    
    def verify_dependencies(self):
        """验证依赖包"""
        print("\n📦 验证依赖包...")
        
        required_packages = [
            'requests',
            'beautifulsoup4',
            'schedule',
            'cryptography'
        ]
        
        optional_packages = [
            'selenium',
            'keyring',
            'tkinter'
        ]
        
        dependency_results = {}
        
        for package in required_packages:
            try:
                # 特殊处理某些包名
                if package == 'beautifulsoup4':
                    import bs4
                else:
                    __import__(package.replace('-', '_'))
                dependency_results[package] = "✅ 已安装"
                print(f"  ✅ {package}")
            except ImportError:
                dependency_results[package] = "❌ 未安装"
                print(f"  ❌ {package} - 未安装")
        
        for package in optional_packages:
            try:
                __import__(package.replace('-', '_'))
                dependency_results[package] = "✅ 已安装"
                print(f"  ✅ {package} (可选)")
            except ImportError:
                dependency_results[package] = "⚠️ 未安装 (可选)"
                print(f"  ⚠️ {package} - 未安装 (可选)")
        
        self.results['dependencies'] = dependency_results
        
        # 检查必需包是否都已安装
        missing_required = [pkg for pkg in required_packages 
                          if "未安装" in dependency_results.get(pkg, "")]
        
        return len(missing_required) == 0
    
    def generate_report(self):
        """生成验证报告"""
        print("\n" + "=" * 50)
        print("📊 功能验证报告")
        print("=" * 50)
        
        total_tests = len(self.results)
        passed_tests = 0
        
        for category, result in self.results.items():
            if isinstance(result, dict):
                # 处理字典类型的结果（如依赖包）
                category_passed = all("✅" in str(v) or "⚠️" in str(v) for v in result.values())
                if category_passed:
                    passed_tests += 1
                print(f"\n{category.replace('_', ' ').title()}:")
                for item, status in result.items():
                    print(f"  {item}: {status}")
            else:
                # 处理字符串类型的结果
                if "✅" in result:
                    passed_tests += 1
                print(f"\n{category.replace('_', ' ').title()}: {result}")
        
        print(f"\n📈 总体结果: {passed_tests}/{total_tests} 通过")
        
        if passed_tests == total_tests:
            print("🎉 所有功能验证通过！")
            return True
        else:
            print("❌ 部分功能验证失败，请检查上述问题")
            return False
    
    def cleanup(self):
        """清理临时文件"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass
    
    def run_all_verifications(self):
        """运行所有验证"""
        try:
            verifications = [
                self.verify_dependencies,
                self.verify_module_imports,
                self.verify_secure_storage,
                self.verify_location_manager,
                self.verify_cookie_manager,
                self.verify_main_application,
                self.verify_signing_functionality
            ]
            
            for verification in verifications:
                verification()
                time.sleep(0.5)  # 短暂延迟，便于阅读
            
            return self.generate_report()
            
        finally:
            self.cleanup()


def main():
    """主函数"""
    verifier = FunctionalityVerifier()
    success = verifier.run_all_verifications()
    
    if success:
        print("\n✅ 功能验证完成，所有核心功能正常！")
        sys.exit(0)
    else:
        print("\n❌ 功能验证失败，请修复问题后重试")
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ 验证被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 验证过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
