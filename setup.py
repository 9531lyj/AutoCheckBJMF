"""
AutoCheckBJMF 增强版安装脚本
"""
import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    
    print(f"✅ Python版本检查通过: {sys.version}")
    return True


def install_requirements():
    """安装依赖包"""
    print("📦 正在安装依赖包...")
    
    try:
        # 升级pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # 安装基础依赖
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ 依赖包安装完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False


def install_webdriver():
    """安装WebDriver"""
    print("🌐 正在配置WebDriver...")
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        from webdriver_manager.firefox import GeckoDriverManager
        
        # 尝试安装Chrome WebDriver
        try:
            ChromeDriverManager().install()
            print("✅ Chrome WebDriver安装成功")
        except Exception as e:
            print(f"⚠️ Chrome WebDriver安装失败: {e}")
        
        # 尝试安装Edge WebDriver
        try:
            EdgeChromiumDriverManager().install()
            print("✅ Edge WebDriver安装成功")
        except Exception as e:
            print(f"⚠️ Edge WebDriver安装失败: {e}")
        
        # 尝试安装Firefox WebDriver
        try:
            GeckoDriverManager().install()
            print("✅ Firefox WebDriver安装成功")
        except Exception as e:
            print(f"⚠️ Firefox WebDriver安装失败: {e}")
        
        return True
        
    except ImportError:
        print("⚠️ webdriver-manager未安装，跳过WebDriver配置")
        return True
    except Exception as e:
        print(f"❌ WebDriver配置失败: {e}")
        return False


def create_directories():
    """创建必要的目录"""
    print("📁 创建目录结构...")
    
    directories = [
        "modules",
        "logs",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ 创建目录: {directory}")
    
    return True


def create_desktop_shortcut():
    """创建桌面快捷方式（Windows）"""
    if platform.system() != "Windows":
        return True
    
    try:
        import win32com.client
        
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "AutoCheckBJMF增强版.lnk")
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = os.path.join(os.getcwd(), "main_enhanced.py")
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print(f"✅ 桌面快捷方式已创建: {shortcut_path}")
        return True
        
    except ImportError:
        print("⚠️ 无法创建桌面快捷方式，请手动创建")
        return True
    except Exception as e:
        print(f"⚠️ 创建桌面快捷方式失败: {e}")
        return True


def create_batch_files():
    """创建批处理文件（Windows）或shell脚本（Linux/macOS）"""
    system = platform.system()
    
    if system == "Windows":
        # 创建启动批处理文件
        batch_content = f"""@echo off
cd /d "{os.getcwd()}"
python main_enhanced.py
pause
"""
        with open("启动AutoCheckBJMF.bat", "w", encoding="gbk") as f:
            f.write(batch_content)
        
        # 创建配置批处理文件
        config_batch_content = f"""@echo off
cd /d "{os.getcwd()}"
python -c "from modules.gui_config import ConfigWizard; ConfigWizard().run()"
pause
"""
        with open("配置AutoCheckBJMF.bat", "w", encoding="gbk") as f:
            f.write(config_batch_content)
        
        print("✅ Windows批处理文件已创建")
        
    else:
        # 创建shell脚本
        script_content = f"""#!/bin/bash
cd "{os.getcwd()}"
python3 main_enhanced.py
"""
        with open("start_autocheckbjmf.sh", "w") as f:
            f.write(script_content)
        os.chmod("start_autocheckbjmf.sh", 0o755)
        
        # 创建配置脚本
        config_script_content = f"""#!/bin/bash
cd "{os.getcwd()}"
python3 -c "from modules.gui_config import ConfigWizard; ConfigWizard().run()"
"""
        with open("config_autocheckbjmf.sh", "w") as f:
            f.write(config_script_content)
        os.chmod("config_autocheckbjmf.sh", 0o755)
        
        print("✅ Shell脚本已创建")
    
    return True


def test_installation():
    """测试安装"""
    print("🧪 测试安装...")
    
    try:
        # 测试模块导入
        sys.path.append(os.path.join(os.getcwd(), 'modules'))
        
        from modules.location_manager import LocationManager
        from modules.secure_storage import SecureStorage
        from modules.browser_cookie_extractor import BrowserCookieExtractor
        
        print("✅ 模块导入测试通过")
        
        # 测试基本功能
        storage = SecureStorage("AutoCheckBJMF_Test")
        test_data = {"test": "data"}
        
        if storage.save_data(test_data) and storage.load_data():
            print("✅ 安全存储测试通过")
        else:
            print("⚠️ 安全存储测试失败")
        
        # 清理测试数据
        storage.clear_data()
        
        return True
        
    except Exception as e:
        print(f"❌ 安装测试失败: {e}")
        return False


def main():
    """主安装函数"""
    print("=" * 60)
    print("AutoCheckBJMF 增强版 - 安装程序")
    print("=" * 60)
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 创建目录结构
    if not create_directories():
        return False
    
    # 安装依赖包
    if not install_requirements():
        return False
    
    # 配置WebDriver
    if not install_webdriver():
        print("⚠️ WebDriver配置失败，自动登录功能可能不可用")
    
    # 创建快捷方式和脚本
    create_desktop_shortcut()
    create_batch_files()
    
    # 测试安装
    if not test_installation():
        print("⚠️ 安装测试失败，但基本功能应该可用")
    
    print("\n" + "=" * 60)
    print("🎉 安装完成！")
    print("\n使用方法：")
    
    system = platform.system()
    if system == "Windows":
        print("1. 双击 '启动AutoCheckBJMF.bat' 运行程序")
        print("2. 双击 '配置AutoCheckBJMF.bat' 重新配置")
        print("3. 或者运行: python main_enhanced.py")
    else:
        print("1. 运行: ./start_autocheckbjmf.sh")
        print("2. 配置: ./config_autocheckbjmf.sh")
        print("3. 或者运行: python3 main_enhanced.py")
    
    print("\n功能特点：")
    print("• 🚀 自动配置向导")
    print("• 🍪 智能Cookie管理")
    print("• 📍 自动位置获取")
    print("• 🔒 安全数据存储")
    print("• 🌐 多浏览器支持")
    print("• ⏰ 定时签到功能")
    
    print("\n如有问题，请查看项目文档或提交Issue")
    print("项目地址：https://github.com/JasonYANG170/AutoCheckBJMF")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ 安装被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 安装过程中发生错误: {e}")
        sys.exit(1)
