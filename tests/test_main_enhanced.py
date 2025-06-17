"""
AutoCheckBJMF 增强版主程序单元测试
"""
import unittest
import tempfile
import os
import json
import sys
from unittest.mock import Mock, patch, MagicMock

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_enhanced import EnhancedAutoCheckBJMF


class TestEnhancedAutoCheckBJMF(unittest.TestCase):
    """增强版主程序测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.app = EnhancedAutoCheckBJMF()
        self.app.current_directory = self.temp_dir
        self.app.config_file = os.path.join(self.temp_dir, "config.json")
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_setup_logging(self):
        """测试日志系统设置"""
        self.app.setup_logging()
        self.assertIsNotNone(self.app.logger)
        self.assertEqual(self.app.logger.name, 'AutoCheckBJMF')
    
    def test_validate_config_data_valid(self):
        """测试有效配置数据验证"""
        user_info = {
            'class_id': '12345',
            'location': {
                'lat': 39.904697,
                'lng': 116.407178,
                'alt': 100
            }
        }
        cookies = ['username=test;remember_student_xxx=test_cookie']
        
        result = self.app._validate_config_data(user_info, cookies)
        self.assertTrue(result)
    
    def test_validate_config_data_invalid_coordinates(self):
        """测试无效坐标验证"""
        user_info = {
            'class_id': '12345',
            'location': {
                'lat': 999,  # 无效纬度
                'lng': 116.407178,
                'alt': 100
            }
        }
        cookies = ['username=test;remember_student_xxx=test_cookie']
        
        result = self.app._validate_config_data(user_info, cookies)
        self.assertFalse(result)
    
    def test_validate_config_data_missing_class_id(self):
        """测试缺少班级ID验证"""
        user_info = {
            'location': {
                'lat': 39.904697,
                'lng': 116.407178,
                'alt': 100
            }
        }
        cookies = ['username=test;remember_student_xxx=test_cookie']
        
        result = self.app._validate_config_data(user_info, cookies)
        self.assertFalse(result)
    
    def test_validate_json_config_valid(self):
        """测试有效JSON配置验证"""
        config_data = {
            'class': '12345',
            'lat': '39.904697',
            'lng': '116.407178',
            'acc': '100',
            'cookie': ['username=test;remember_student_xxx=test_cookie'],
            'scheduletime': '08:30',
            'pushplus': '',
            'debug': False,
            'configLock': True
        }
        
        result = self.app._validate_json_config(config_data)
        self.assertTrue(result)
    
    def test_validate_json_config_invalid_schedule(self):
        """测试无效定时格式验证"""
        config_data = {
            'class': '12345',
            'lat': '39.904697',
            'lng': '116.407178',
            'acc': '100',
            'cookie': ['username=test;remember_student_xxx=test_cookie'],
            'scheduletime': '8:30',  # 无效格式，应为08:30
            'pushplus': '',
            'debug': False,
            'configLock': True
        }
        
        result = self.app._validate_json_config(config_data)
        self.assertFalse(result)
    
    def test_save_config(self):
        """测试配置保存"""
        self.app.config = {
            'class': '12345',
            'lat': '39.904697',
            'lng': '116.407178',
            'acc': '100',
            'cookie': ['username=test;remember_student_xxx=test_cookie'],
            'scheduletime': '08:30',
            'pushplus': '',
            'debug': False,
            'configLock': True
        }
        
        with patch.object(self.app.cookie_manager, 'save_cookies') as mock_save:
            mock_save.return_value = True
            self.app.save_config()
            
            # 检查文件是否创建
            self.assertTrue(os.path.exists(self.app.config_file))
            
            # 检查文件内容
            with open(self.app.config_file, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
            
            self.assertEqual(saved_config['class'], '12345')
            self.assertEqual(saved_config['lat'], '39.904697')
    
    def test_load_config_from_file(self):
        """测试从文件加载配置"""
        # 创建测试配置文件
        test_config = {
            'class': '12345',
            'lat': '39.904697',
            'lng': '116.407178',
            'acc': '100',
            'cookie': ['username=test;remember_student_xxx=test_cookie'],
            'scheduletime': '08:30',
            'pushplus': '',
            'debug': False,
            'configLock': True
        }
        
        with open(self.app.config_file, 'w', encoding='utf-8') as f:
            json.dump(test_config, f)
        
        # Mock安全存储返回空
        with patch.object(self.app.cookie_manager.storage, 'load_data') as mock_load:
            mock_load.return_value = None
            
            result = self.app.load_config()
            self.assertTrue(result)
            self.assertEqual(self.app.config['class'], '12345')
    
    def test_load_config_invalid_json(self):
        """测试加载无效JSON配置"""
        # 创建无效JSON文件
        with open(self.app.config_file, 'w', encoding='utf-8') as f:
            f.write('invalid json content')
        
        with patch.object(self.app.cookie_manager.storage, 'load_data') as mock_load:
            mock_load.return_value = None
            
            result = self.app.load_config()
            self.assertFalse(result)
    
    def test_modify_decimal_part(self):
        """测试坐标随机偏移"""
        original = 39.90469700
        modified = self.app.modify_decimal_part(original)
        
        # 检查返回值是浮点数
        self.assertIsInstance(modified, float)
        
        # 检查偏移范围合理
        diff = abs(modified - original)
        self.assertLess(diff, 0.01)  # 偏移应该很小
    
    @patch('requests.get')
    def test_qiandao_success(self, mock_get):
        """测试签到成功"""
        # 设置配置
        self.app.config = {
            'class': '12345',
            'lat': '39.904697',
            'lng': '116.407178',
            'acc': '100'
        }
        
        # Mock HTTP响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <title>课程页面</title>
            <script>punch_gps(67890)</script>
        </html>
        '''
        mock_get.return_value = mock_response
        
        # Mock POST请求
        with patch('requests.post') as mock_post:
            mock_post_response = Mock()
            mock_post_response.status_code = 200
            mock_post_response.text = '<div id="title">签到成功</div>'
            mock_post.return_value = mock_post_response
            
            cookies = ['username=test;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=test_cookie']
            error_cookies, null_cookie = self.app.qiandao(cookies)
            
            self.assertEqual(len(error_cookies), 0)
            self.assertEqual(null_cookie, 0)
    
    @patch('requests.get')
    def test_qiandao_no_tasks(self, mock_get):
        """测试无签到任务"""
        # 设置配置
        self.app.config = {
            'class': '12345',
            'lat': '39.904697',
            'lng': '116.407178',
            'acc': '100'
        }
        
        # Mock HTTP响应 - 无签到任务
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <title>课程页面</title>
            <p>当前无签到任务</p>
        </html>
        '''
        mock_get.return_value = mock_response
        
        cookies = ['username=test;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=test_cookie']
        error_cookies, null_cookie = self.app.qiandao(cookies)
        
        self.assertEqual(len(error_cookies), 0)
        self.assertEqual(null_cookie, 0)
    
    def test_qiandao_invalid_cookie_format(self):
        """测试无效Cookie格式"""
        self.app.config = {
            'class': '12345',
            'lat': '39.904697',
            'lng': '116.407178',
            'acc': '100'
        }
        
        cookies = ['invalid_cookie_format']
        error_cookies, null_cookie = self.app.qiandao(cookies)
        
        self.assertEqual(len(error_cookies), 0)
        self.assertEqual(null_cookie, 1)
    
    def test_qiandao_missing_config(self):
        """测试配置信息不完整"""
        self.app.config = {
            'class': '',  # 缺少班级ID
            'lat': '39.904697',
            'lng': '116.407178',
            'acc': '100'
        }
        
        cookies = ['username=test;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=test_cookie']
        error_cookies, null_cookie = self.app.qiandao(cookies)
        
        self.assertEqual(len(error_cookies), 0)
        self.assertEqual(null_cookie, 1)


class TestConfigValidation(unittest.TestCase):
    """配置验证测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.app = EnhancedAutoCheckBJMF()
    
    def test_coordinate_validation(self):
        """测试坐标验证"""
        # 有效坐标
        valid_coords = [
            (0, 0),
            (39.904697, 116.407178),
            (-90, -180),
            (90, 180)
        ]
        
        for lat, lng in valid_coords:
            user_info = {
                'class_id': '12345',
                'location': {'lat': lat, 'lng': lng}
            }
            cookies = ['test_cookie']
            result = self.app._validate_config_data(user_info, cookies)
            self.assertTrue(result, f"坐标 ({lat}, {lng}) 应该有效")
        
        # 无效坐标
        invalid_coords = [
            (91, 0),    # 纬度超出范围
            (-91, 0),   # 纬度超出范围
            (0, 181),   # 经度超出范围
            (0, -181),  # 经度超出范围
        ]
        
        for lat, lng in invalid_coords:
            user_info = {
                'class_id': '12345',
                'location': {'lat': lat, 'lng': lng}
            }
            cookies = ['test_cookie']
            result = self.app._validate_config_data(user_info, cookies)
            self.assertFalse(result, f"坐标 ({lat}, {lng}) 应该无效")
    
    def test_schedule_time_validation(self):
        """测试定时格式验证"""
        # 有效格式
        valid_times = ['00:00', '08:30', '23:59', '12:00']
        
        for time_str in valid_times:
            config_data = {
                'class': '12345',
                'lat': '39.904697',
                'lng': '116.407178',
                'acc': '100',
                'cookie': ['test_cookie'],
                'scheduletime': time_str
            }
            result = self.app._validate_json_config(config_data)
            self.assertTrue(result, f"时间格式 {time_str} 应该有效")
        
        # 无效格式
        invalid_times = ['8:30', '24:00', '12:60', 'abc', '']
        
        for time_str in invalid_times:
            if time_str == '':  # 空字符串是有效的（表示不设定时）
                continue
                
            config_data = {
                'class': '12345',
                'lat': '39.904697',
                'lng': '116.407178',
                'acc': '100',
                'cookie': ['test_cookie'],
                'scheduletime': time_str
            }
            result = self.app._validate_json_config(config_data)
            self.assertFalse(result, f"时间格式 {time_str} 应该无效")


if __name__ == '__main__':
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试用例
    test_suite.addTest(unittest.makeSuite(TestEnhancedAutoCheckBJMF))
    test_suite.addTest(unittest.makeSuite(TestConfigValidation))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出测试结果
    if result.wasSuccessful():
        print("\n✅ 所有测试通过！")
    else:
        print(f"\n❌ 测试失败: {len(result.failures)} 个失败, {len(result.errors)} 个错误")
        sys.exit(1)
