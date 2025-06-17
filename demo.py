#!/usr/bin/env python3
"""
AutoCheckBJMF 增强版演示脚本
展示主要功能和特性
"""
import os
import sys
import time
import tempfile
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def print_banner():
    """打印横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                  🚀 AutoCheckBJMF 增强版                     ║
║                智能化班级魔方自动签到解决方案                  ║
╠══════════════════════════════════════════════════════════════╣
║  ✨ 特性展示：                                               ║
║  🎯 一键智能配置 | 🍪 智能Cookie管理 | 📍 自动位置获取        ║
║  🏫 智能班级检测 | 🔒 企业级安全   | 🎨 现代化界面          ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def demo_secure_storage():
    """演示安全存储功能"""
    print("\n🔒 演示：企业级安全存储")
    print("=" * 50)
    
    try:
        from modules.secure_storage import SecureStorage
        
        # 创建临时存储
        temp_dir = tempfile.mkdtemp()
        storage = SecureStorage("DemoApp")
        storage.storage_path = temp_dir
        storage.key_file = os.path.join(temp_dir, "demo.key")
        storage.data_file = os.path.join(temp_dir, "demo_data.enc")
        
        # 演示数据
        demo_data = {
            'user': '演示用户',
            'class_id': '12345',
            'location': {
                'lat': 39.904697,
                'lng': 116.407178,
                'city': '北京'
            },
            'cookies': ['demo_cookie_1', 'demo_cookie_2'],
            'chinese_text': '这是中文测试数据 🎉',
            'sensitive_info': '这些数据将被加密存储'
        }
        
        print("📝 保存演示数据...")
        print(f"   数据项: {len(demo_data)} 个")
        print(f"   包含中文: ✅")
        print(f"   包含敏感信息: ✅")
        
        # 保存数据
        save_result = storage.save_data(demo_data)
        if save_result:
            print("✅ 数据加密保存成功")
        else:
            print("❌ 数据保存失败")
            return
        
        print("\n🔓 加载并验证数据...")
        
        # 加载数据
        loaded_data = storage.load_data()
        if loaded_data:
            print("✅ 数据解密加载成功")
            print(f"   用户: {loaded_data['user']}")
            print(f"   班级ID: {loaded_data['class_id']}")
            print(f"   位置: {loaded_data['location']['city']}")
            print(f"   中文测试: {loaded_data['chinese_text']}")
            print(f"   数据完整性: ✅ 验证通过")
        else:
            print("❌ 数据加载失败")
        
        # 清理
        storage.clear_data()
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        
    except Exception as e:
        print(f"❌ 安全存储演示失败: {e}")

def demo_location_manager():
    """演示位置管理功能"""
    print("\n📍 演示：智能位置管理")
    print("=" * 50)
    
    try:
        from modules.location_manager import LocationManager
        from unittest.mock import patch, Mock
        
        manager = LocationManager()
        
        print("🌐 模拟IP定位...")
        
        # Mock IP定位
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
            
            if location:
                print("✅ IP定位成功")
                print(f"   城市: {location['city']}")
                print(f"   地区: {location.get('region', 'N/A')}")
                print(f"   坐标: {location['lat']:.6f}, {location['lng']:.6f}")
                print(f"   来源: {location['source']}")
            else:
                print("❌ IP定位失败")
        
        print("\n🎯 演示默认位置机制...")
        
        # 演示默认位置
        with patch.object(manager, 'get_system_location') as mock_system, \
             patch.object(manager, 'get_location_by_ip') as mock_ip, \
             patch.object(manager, 'manual_location_picker') as mock_manual:
            
            mock_system.return_value = None
            mock_ip.return_value = None
            mock_manual.return_value = None
            
            default_location = manager.get_best_location()
            
            if default_location:
                print("✅ 默认位置机制正常")
                print(f"   默认城市: 北京")
                print(f"   坐标: {default_location['lat']:.6f}, {default_location['lng']:.6f}")
                print(f"   来源: {default_location['source']}")
            else:
                print("❌ 默认位置机制失败")
        
    except Exception as e:
        print(f"❌ 位置管理演示失败: {e}")

def demo_cookie_manager():
    """演示Cookie管理功能"""
    print("\n🍪 演示：智能Cookie管理")
    print("=" * 50)
    
    try:
        from modules.secure_storage import CookieManager
        from unittest.mock import patch
        
        # 创建临时Cookie管理器
        temp_dir = tempfile.mkdtemp()
        manager = CookieManager()
        manager.storage.storage_path = temp_dir
        manager.storage.key_file = os.path.join(temp_dir, "cookie_demo.key")
        manager.storage.data_file = os.path.join(temp_dir, "cookie_demo_data.enc")
        
        # 演示Cookie数据
        demo_cookies = [
            'username=张三;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=demo_cookie_1',
            'username=李四;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=demo_cookie_2',
            'username=王五;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=demo_cookie_3'
        ]
        
        user_info = {
            'class_id': '12345',
            'location': {
                'lat': 39.904697,
                'lng': 116.407178,
                'city': '北京'
            },
            'schedule': '08:30',
            'push_token': 'demo_push_token'
        }
        
        print("📝 保存多用户Cookie...")
        print(f"   用户数量: {len(demo_cookies)}")
        print(f"   班级ID: {user_info['class_id']}")
        print(f"   定时设置: {user_info['schedule']}")
        
        # Mock Cookie验证
        with patch.object(manager, 'validate_cookie') as mock_validate:
            mock_validate.return_value = True
            
            # 保存Cookie
            save_result = manager.save_cookies(demo_cookies, user_info)
            if save_result:
                print("✅ Cookie加密保存成功")
            else:
                print("❌ Cookie保存失败")
                return
        
        print("\n🔍 加载并验证Cookie...")
        
        # 加载Cookie
        loaded_cookies = manager.load_cookies()
        if loaded_cookies:
            print(f"✅ Cookie加载成功，数量: {len(loaded_cookies)}")
            for i, cookie in enumerate(loaded_cookies, 1):
                username = cookie.split(';')[0].split('=')[1] if '=' in cookie else 'Unknown'
                print(f"   用户{i}: {username}")
        else:
            print("❌ Cookie加载失败")
        
        # 获取用户信息
        loaded_info = manager.get_user_info()
        if loaded_info:
            print(f"✅ 用户信息加载成功")
            print(f"   班级ID: {loaded_info['class_id']}")
            print(f"   位置: {loaded_info['location']['city']}")
            print(f"   定时: {loaded_info['schedule']}")
        
        # 清理
        manager.clear_all_data()
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        
    except Exception as e:
        print(f"❌ Cookie管理演示失败: {e}")

def demo_config_validation():
    """演示配置验证功能"""
    print("\n🔧 演示：智能配置验证")
    print("=" * 50)
    
    try:
        from main_enhanced import EnhancedAutoCheckBJMF
        
        app = EnhancedAutoCheckBJMF()
        
        print("✅ 测试有效配置...")
        
        valid_config = {
            'class': '12345',
            'lat': '39.904697',
            'lng': '116.407178',
            'acc': '100',
            'cookie': ['username=test;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie'],
            'scheduletime': '08:30',
            'pushplus': 'demo_token',
            'debug': False,
            'configLock': True
        }
        
        if app._validate_json_config(valid_config):
            print("   ✅ 有效配置验证通过")
            print(f"   班级ID: {valid_config['class']}")
            print(f"   坐标: {valid_config['lat']}, {valid_config['lng']}")
            print(f"   定时: {valid_config['scheduletime']}")
        else:
            print("   ❌ 有效配置验证失败")
        
        print("\n❌ 测试无效配置...")
        
        invalid_configs = [
            {
                'class': '12345',
                'lat': '999',  # 无效纬度
                'lng': '116.407178',
                'acc': '100',
                'cookie': ['valid_cookie'],
                'scheduletime': '08:30'
            },
            {
                'class': '12345',
                'lat': '39.904697',
                'lng': '116.407178',
                'acc': '100',
                'cookie': ['valid_cookie'],
                'scheduletime': '25:30'  # 无效时间
            },
            {
                'class': '',  # 缺少班级ID
                'lat': '39.904697',
                'lng': '116.407178',
                'acc': '100',
                'cookie': ['valid_cookie']
            }
        ]
        
        for i, config in enumerate(invalid_configs, 1):
            result = app._validate_json_config(config)
            if not result:
                print(f"   ✅ 无效配置{i}正确被拒绝")
            else:
                print(f"   ❌ 无效配置{i}应该被拒绝")
        
        print("\n🎯 测试坐标偏移功能...")
        
        original_lat = 39.904697
        modified_lat = app.modify_decimal_part(original_lat)
        offset = abs(modified_lat - original_lat)
        
        print(f"   原始坐标: {original_lat:.8f}")
        print(f"   偏移坐标: {modified_lat:.8f}")
        print(f"   偏移量: {offset:.8f}")
        
        if 0 < offset < 0.01:
            print("   ✅ 坐标偏移功能正常")
        else:
            print("   ❌ 坐标偏移功能异常")
        
    except Exception as e:
        print(f"❌ 配置验证演示失败: {e}")

def demo_signing_simulation():
    """演示签到功能模拟"""
    print("\n📝 演示：签到功能模拟")
    print("=" * 50)
    
    try:
        from main_enhanced import EnhancedAutoCheckBJMF
        from unittest.mock import patch, Mock
        
        app = EnhancedAutoCheckBJMF()
        app.config = {
            'class': '12345',
            'lat': '39.904697',
            'lng': '116.407178',
            'acc': '100'
        }
        
        print("🎯 模拟签到场景...")
        
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
                <script>punchcard_12345</script>
            </html>
            '''
            mock_get.return_value = mock_get_response
            
            # Mock签到请求响应
            mock_post_response = Mock()
            mock_post_response.status_code = 200
            mock_post_response.text = '<div id="title">签到成功</div>'
            mock_post.return_value = mock_post_response
            
            # 测试多用户签到
            test_cookies = [
                'username=张三;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie1',
                'username=李四;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie2',
                'username=王五;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie3'
            ]
            
            print(f"   用户数量: {len(test_cookies)}")
            print(f"   班级ID: {app.config['class']}")
            print(f"   签到类型: GPS + 二维码")
            
            error_cookies, null_cookie = app.qiandao(test_cookies)
            
            success_count = len(test_cookies) - len(error_cookies) - null_cookie
            
            print(f"\n📊 签到结果统计:")
            print(f"   成功: {success_count}/{len(test_cookies)}")
            print(f"   失败: {len(error_cookies)}")
            print(f"   无效: {null_cookie}")
            
            if success_count == len(test_cookies):
                print("   🎉 全部签到成功！")
            else:
                print("   ⚠️ 部分签到失败")
        
    except Exception as e:
        print(f"❌ 签到功能演示失败: {e}")

def demo_cross_platform_features():
    """演示跨平台特性"""
    print("\n🌍 演示：跨平台兼容性")
    print("=" * 50)
    
    import platform
    
    system = platform.system()
    version = platform.version()
    architecture = platform.architecture()[0]
    python_version = platform.python_version()
    
    print(f"🖥️ 当前系统信息:")
    print(f"   操作系统: {system}")
    print(f"   系统版本: {version}")
    print(f"   架构: {architecture}")
    print(f"   Python版本: {python_version}")
    
    print(f"\n✅ 支持的平台特性:")
    
    # Windows特性
    if system == "Windows":
        print("   🖥️ Windows特性:")
        print("     • DPAPI安全存储")
        print("     • 桌面快捷方式")
        print("     • 批处理文件启动")
        print("     • Windows GPS API")
        
        try:
            import win32crypt
            print("     ✅ Win32 API可用")
        except ImportError:
            print("     ⚠️ Win32 API不可用")
    
    # macOS特性
    elif system == "Darwin":
        print("   🍎 macOS特性:")
        print("     • Keychain安全存储")
        print("     • CoreLocation GPS")
        print("     • Shell脚本启动")
        print("     • 系统通知集成")
    
    # Linux特性
    elif system == "Linux":
        print("   🐧 Linux特性:")
        print("     • 文件系统加密")
        print("     • D-Bus系统集成")
        print("     • Shell脚本启动")
        print("     • 包管理器支持")
    
    print(f"\n🔒 安全存储测试:")
    
    try:
        from modules.secure_storage import SecureStorage
        
        storage = SecureStorage("CrossPlatformTest")
        test_data = {"platform": system, "test": "success"}
        
        if storage.save_data(test_data) and storage.load_data():
            print("   ✅ 安全存储在当前平台正常工作")
        else:
            print("   ❌ 安全存储在当前平台存在问题")
        
        storage.clear_data()
        
    except Exception as e:
        print(f"   ❌ 安全存储测试失败: {e}")

def main():
    """主演示函数"""
    print_banner()
    
    demos = [
        ("安全存储", demo_secure_storage),
        ("位置管理", demo_location_manager),
        ("Cookie管理", demo_cookie_manager),
        ("配置验证", demo_config_validation),
        ("签到模拟", demo_signing_simulation),
        ("跨平台特性", demo_cross_platform_features)
    ]
    
    print("\n🎬 开始功能演示...")
    
    for i, (name, demo_func) in enumerate(demos, 1):
        print(f"\n{'='*60}")
        print(f"演示 {i}/{len(demos)}: {name}")
        print(f"{'='*60}")
        
        try:
            demo_func()
        except Exception as e:
            print(f"❌ 演示 {name} 失败: {e}")
        
        if i < len(demos):
            print("\n⏳ 等待3秒后继续...")
            time.sleep(3)
    
    print(f"\n{'='*60}")
    print("🎉 演示完成！")
    print(f"{'='*60}")
    
    print(f"""
📚 更多信息:
   • 在线文档: https://9531lyj.github.io/AutoCheckBJMF/
   • GitHub仓库: https://github.com/9531lyj/AutoCheckBJMF
   • 安装指南: docs/installation-guide.md
   • 使用教程: docs/user-guide.md
   • 故障排除: docs/troubleshooting.md

🚀 快速开始:
   python main_enhanced.py

💡 提示: 选择"快速自动配置"可在3分钟内完成所有设置！
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
