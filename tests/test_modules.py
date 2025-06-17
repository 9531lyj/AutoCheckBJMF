"""
AutoCheckBJMF 增强版模块单元测试
"""
import unittest
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from modules.secure_storage import SecureStorage, CookieManager
    from modules.location_manager import LocationManager
    from modules.browser_cookie_extractor import BrowserCookieExtractor
except ImportError as e:
    print(f"模块导入失败: {e}")
    print("请确保所有模块文件都存在")
    sys.exit(1)


class TestSecureStorage(unittest.TestCase):
    """安全存储测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = SecureStorage("TestApp")
        # 使用临时目录
        self.storage.storage_path = self.temp_dir
        self.storage.key_file = os.path.join(self.temp_dir, "test.key")
        self.storage.data_file = os.path.join(self.temp_dir, "test_data.enc")
        self.storage.cipher = self.storage._get_or_create_cipher()
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_save_and_load_data(self):
        """测试数据保存和加载"""
        test_data = {
            'test_key': 'test_value',
            'number': 123,
            'list': [1, 2, 3],
            'dict': {'nested': 'value'}
        }
        
        # 保存数据
        result = self.storage.save_data(test_data)
        self.assertTrue(result)
        
        # 加载数据
        loaded_data = self.storage.load_data()
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data['test_key'], 'test_value')
        self.assertEqual(loaded_data['number'], 123)
        self.assertEqual(loaded_data['list'], [1, 2, 3])
        self.assertEqual(loaded_data['dict']['nested'], 'value')
    
    def test_save_empty_data(self):
        """测试保存空数据"""
        empty_data = {}
        result = self.storage.save_data(empty_data)
        self.assertTrue(result)
        
        loaded_data = self.storage.load_data()
        self.assertIsNotNone(loaded_data)
        self.assertIn('_timestamp', loaded_data)
        self.assertIn('_version', loaded_data)
    
    def test_load_nonexistent_data(self):
        """测试加载不存在的数据"""
        result = self.storage.load_data()
        self.assertIsNone(result)
    
    def test_clear_data(self):
        """测试清除数据"""
        # 先保存一些数据
        test_data = {'test': 'data'}
        self.storage.save_data(test_data)
        
        # 确认数据存在
        self.assertIsNotNone(self.storage.load_data())
        
        # 清除数据
        result = self.storage.clear_data()
        self.assertTrue(result)
        
        # 确认数据已清除
        self.assertIsNone(self.storage.load_data())
    
    def test_unicode_data(self):
        """测试Unicode数据处理"""
        unicode_data = {
            'chinese': '中文测试',
            'emoji': '🚀🎉✅',
            'special': 'àáâãäåæçèéêë'
        }
        
        result = self.storage.save_data(unicode_data)
        self.assertTrue(result)
        
        loaded_data = self.storage.load_data()
        self.assertEqual(loaded_data['chinese'], '中文测试')
        self.assertEqual(loaded_data['emoji'], '🚀🎉✅')
        self.assertEqual(loaded_data['special'], 'àáâãäåæçèéêë')


class TestCookieManager(unittest.TestCase):
    """Cookie管理器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.cookie_manager = CookieManager()
        # 使用临时存储
        self.cookie_manager.storage.storage_path = self.temp_dir
        self.cookie_manager.storage.key_file = os.path.join(self.temp_dir, "test.key")
        self.cookie_manager.storage.data_file = os.path.join(self.temp_dir, "test_data.enc")
        self.cookie_manager.storage.cipher = self.cookie_manager.storage._get_or_create_cipher()
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_save_and_load_cookies(self):
        """测试Cookie保存和加载"""
        test_cookies = [
            'username=test1;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie1',
            'username=test2;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie2'
        ]
        
        user_info = {
            'class_id': '12345',
            'location': {'lat': 39.904697, 'lng': 116.407178}
        }
        
        # Mock Cookie验证
        with patch.object(self.cookie_manager, 'validate_cookie') as mock_validate:
            mock_validate.return_value = True
            
            result = self.cookie_manager.save_cookies(test_cookies, user_info)
            self.assertTrue(result)
        
        # 加载Cookie
        loaded_cookies = self.cookie_manager.load_cookies()
        self.assertEqual(len(loaded_cookies), 2)
        self.assertIn('username=test1', loaded_cookies[0])
        self.assertIn('username=test2', loaded_cookies[1])
    
    @patch('requests.get')
    def test_validate_cookie_success(self, mock_get):
        """测试Cookie验证成功"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = 'http://k8n.cn/student/dashboard'
        mock_get.return_value = mock_response
        
        test_cookie = 'username=test;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=valid_cookie'
        result = self.cookie_manager.validate_cookie(test_cookie)
        self.assertTrue(result)
    
    @patch('requests.get')
    def test_validate_cookie_failure(self, mock_get):
        """测试Cookie验证失败"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = 'http://k8n.cn/student/login'  # 重定向到登录页
        mock_get.return_value = mock_response
        
        test_cookie = 'username=test;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=invalid_cookie'
        result = self.cookie_manager.validate_cookie(test_cookie)
        self.assertFalse(result)
    
    def test_validate_cookie_invalid_format(self):
        """测试无效Cookie格式"""
        invalid_cookies = [
            'invalid_cookie',
            'username=test',
            'remember_student_xxx=cookie'
        ]
        
        for cookie in invalid_cookies:
            result = self.cookie_manager.validate_cookie(cookie)
            self.assertFalse(result)
    
    def test_get_user_info(self):
        """测试获取用户信息"""
        test_cookies = ['username=test;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie']
        user_info = {
            'class_id': '12345',
            'location': {'lat': 39.904697, 'lng': 116.407178}
        }
        
        with patch.object(self.cookie_manager, 'validate_cookie') as mock_validate:
            mock_validate.return_value = True
            self.cookie_manager.save_cookies(test_cookies, user_info)
        
        loaded_info = self.cookie_manager.get_user_info()
        self.assertEqual(loaded_info['class_id'], '12345')
        self.assertEqual(loaded_info['location']['lat'], 39.904697)


class TestLocationManager(unittest.TestCase):
    """位置管理器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.location_manager = LocationManager()
    
    @patch('requests.get')
    def test_get_location_by_ip_success(self, mock_get):
        """测试IP定位成功"""
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
        
        result = self.location_manager.get_location_by_ip()
        self.assertIsNotNone(result)
        self.assertEqual(result['lat'], 39.904697)
        self.assertEqual(result['lng'], 116.407178)
        self.assertEqual(result['city'], 'Beijing')
        self.assertEqual(result['source'], 'IP定位')
    
    @patch('requests.get')
    def test_get_location_by_ip_failure(self, mock_get):
        """测试IP定位失败"""
        mock_get.side_effect = Exception("Network error")
        
        result = self.location_manager.get_location_by_ip()
        self.assertIsNone(result)
    
    @patch('requests.get')
    def test_get_location_by_ip_ipinfo(self, mock_get):
        """测试使用ipinfo.io定位"""
        # 第一个API失败，第二个成功
        def side_effect(url, **kwargs):
            if 'ip-api.com' in url:
                raise Exception("First API failed")
            elif 'ipinfo.io' in url:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'loc': '39.904697,116.407178',
                    'city': 'Beijing',
                    'region': 'Beijing',
                    'country': 'CN'
                }
                return mock_response
        
        mock_get.side_effect = side_effect
        
        result = self.location_manager.get_location_by_ip()
        self.assertIsNotNone(result)
        self.assertEqual(result['lat'], 39.904697)
        self.assertEqual(result['lng'], 116.407178)
    
    def test_get_best_location_default(self):
        """测试获取默认位置"""
        # Mock所有定位方法失败
        with patch.object(self.location_manager, 'get_system_location') as mock_system, \
             patch.object(self.location_manager, 'get_location_by_ip') as mock_ip, \
             patch.object(self.location_manager, 'manual_location_picker') as mock_manual:
            
            mock_system.return_value = None
            mock_ip.return_value = None
            mock_manual.return_value = None
            
            result = self.location_manager.get_best_location()
            
            # 应该返回默认位置（北京）
            self.assertIsNotNone(result)
            self.assertEqual(result['lat'], 39.90469700)
            self.assertEqual(result['lng'], 116.40717800)
            self.assertEqual(result['source'], '默认位置')


class TestBrowserCookieExtractor(unittest.TestCase):
    """浏览器Cookie提取器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.extractor = BrowserCookieExtractor()
    
    def test_get_browser_paths(self):
        """测试获取浏览器路径"""
        paths = self.extractor.get_browser_paths()
        self.assertIsInstance(paths, dict)
        
        # 检查路径格式
        for browser, path in paths.items():
            self.assertIsInstance(browser, str)
            self.assertIsInstance(path, str)
            self.assertTrue(os.path.exists(path), f"浏览器路径不存在: {path}")
    
    @patch('os.path.exists')
    def test_get_browser_paths_no_browsers(self, mock_exists):
        """测试无浏览器情况"""
        mock_exists.return_value = False
        
        paths = self.extractor.get_browser_paths()
        self.assertEqual(len(paths), 0)
    
    def test_format_cookies_for_requests(self):
        """测试Cookie格式化"""
        test_cookies = [
            {
                'name': 'remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d',
                'value': 'test_cookie_value',
                'domain': 'k8n.cn',
                'source_browser': 'chrome'
            }
        ]
        
        formatted = self.extractor.format_cookies_for_requests(test_cookies)
        self.assertEqual(len(formatted), 1)
        self.assertIn('username=从chrome提取', formatted[0])
        self.assertIn('remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=test_cookie_value', formatted[0])
    
    def test_format_cookies_empty_list(self):
        """测试空Cookie列表格式化"""
        formatted = self.extractor.format_cookies_for_requests([])
        self.assertEqual(len(formatted), 0)
    
    def test_format_cookies_wrong_name(self):
        """测试错误Cookie名称"""
        test_cookies = [
            {
                'name': 'wrong_cookie_name',
                'value': 'test_value',
                'domain': 'k8n.cn',
                'source_browser': 'chrome'
            }
        ]
        
        formatted = self.extractor.format_cookies_for_requests(test_cookies)
        self.assertEqual(len(formatted), 0)


class TestIntegration(unittest.TestCase):
    """集成测试类"""
    
    def test_secure_storage_cookie_manager_integration(self):
        """测试安全存储和Cookie管理器集成"""
        temp_dir = tempfile.mkdtemp()
        
        try:
            # 创建Cookie管理器
            cookie_manager = CookieManager()
            cookie_manager.storage.storage_path = temp_dir
            cookie_manager.storage.key_file = os.path.join(temp_dir, "test.key")
            cookie_manager.storage.data_file = os.path.join(temp_dir, "test_data.enc")
            cookie_manager.storage.cipher = cookie_manager.storage._get_or_create_cipher()
            
            # 保存Cookie
            test_cookies = ['username=test;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie']
            user_info = {'class_id': '12345'}
            
            with patch.object(cookie_manager, 'validate_cookie') as mock_validate:
                mock_validate.return_value = True
                result = cookie_manager.save_cookies(test_cookies, user_info)
                self.assertTrue(result)
            
            # 创建新的Cookie管理器实例（模拟程序重启）
            new_cookie_manager = CookieManager()
            new_cookie_manager.storage.storage_path = temp_dir
            new_cookie_manager.storage.key_file = os.path.join(temp_dir, "test.key")
            new_cookie_manager.storage.data_file = os.path.join(temp_dir, "test_data.enc")
            new_cookie_manager.storage.cipher = new_cookie_manager.storage._get_or_create_cipher()
            
            # 加载Cookie
            loaded_cookies = new_cookie_manager.load_cookies()
            self.assertEqual(len(loaded_cookies), 1)
            self.assertIn('username=test', loaded_cookies[0])
            
            # 获取用户信息
            loaded_info = new_cookie_manager.get_user_info()
            self.assertEqual(loaded_info['class_id'], '12345')
            
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试用例
    test_suite.addTest(unittest.makeSuite(TestSecureStorage))
    test_suite.addTest(unittest.makeSuite(TestCookieManager))
    test_suite.addTest(unittest.makeSuite(TestLocationManager))
    test_suite.addTest(unittest.makeSuite(TestBrowserCookieExtractor))
    test_suite.addTest(unittest.makeSuite(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出测试结果
    if result.wasSuccessful():
        print("\n✅ 所有模块测试通过！")
    else:
        print(f"\n❌ 模块测试失败: {len(result.failures)} 个失败, {len(result.errors)} 个错误")
        for failure in result.failures:
            print(f"失败: {failure[0]}")
            print(f"详情: {failure[1]}")
        for error in result.errors:
            print(f"错误: {error[0]}")
            print(f"详情: {error[1]}")
        sys.exit(1)
