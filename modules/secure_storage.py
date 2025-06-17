"""
Cookie安全存储和管理模块
提供跨平台的安全存储解决方案，支持加密存储和自动刷新
"""
import os
import json
import platform
import base64
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import requests
from pathlib import Path


class SecureStorage:
    """安全存储管理器"""
    
    def __init__(self, app_name: str = "AutoCheckBJMF"):
        self.app_name = app_name
        self.system = platform.system()
        self.storage_path = self._get_storage_path()
        self.key_file = os.path.join(self.storage_path, "storage.key")
        self.data_file = os.path.join(self.storage_path, "secure_data.enc")
        
        # 确保存储目录存在
        os.makedirs(self.storage_path, exist_ok=True)
        
        # 初始化加密密钥
        self.cipher = self._get_or_create_cipher()
    
    def _get_storage_path(self) -> str:
        """获取存储路径"""
        if self.system == "Windows":
            # Windows: 使用AppData/Local
            base_path = os.path.join(os.path.expanduser("~"), "AppData", "Local")
        elif self.system == "Darwin":
            # macOS: 使用Application Support
            base_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
        else:
            # Linux: 使用.config
            base_path = os.path.join(os.path.expanduser("~"), ".config")
        
        return os.path.join(base_path, self.app_name)
    
    def _get_or_create_cipher(self) -> Fernet:
        """获取或创建加密密钥"""
        if os.path.exists(self.key_file):
            # 读取现有密钥
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            # 生成新密钥
            key = self._generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            
            # 设置文件权限（仅所有者可读写）
            if self.system != "Windows":
                os.chmod(self.key_file, 0o600)
        
        return Fernet(key)
    
    def _generate_key(self) -> bytes:
        """生成加密密钥"""
        if self.system == "Windows":
            # Windows: 使用DPAPI保护密钥
            try:
                import win32crypt
                # 生成随机密钥
                key = Fernet.generate_key()
                # 使用DPAPI加密密钥
                encrypted_key = win32crypt.CryptProtectData(key, None, None, None, None, 0)
                return base64.urlsafe_b64encode(encrypted_key)
            except ImportError:
                print("警告: 无法使用Windows DPAPI，使用标准加密")
        
        # 其他系统或DPAPI不可用时，使用基于机器信息的密钥
        machine_id = self._get_machine_id()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=machine_id.encode()[:16].ljust(16, b'0'),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(machine_id.encode()))
        return key
    
    def _get_machine_id(self) -> str:
        """获取机器唯一标识"""
        try:
            if self.system == "Windows":
                import subprocess
                result = subprocess.run(['wmic', 'csproduct', 'get', 'uuid'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        return lines[1].strip()
            elif self.system == "Darwin":
                result = subprocess.run(['system_profiler', 'SPHardwareDataType'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'Hardware UUID' in line:
                            return line.split(':')[1].strip()
            else:
                # Linux: 使用machine-id
                machine_id_files = ['/etc/machine-id', '/var/lib/dbus/machine-id']
                for file_path in machine_id_files:
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as f:
                            return f.read().strip()
        except:
            pass
        
        # 备用方案：使用用户名和主机名
        import getpass
        import socket
        return f"{getpass.getuser()}@{socket.gethostname()}"
    
    def save_data(self, data: Dict[str, Any]) -> bool:
        """保存加密数据"""
        try:
            # 添加时间戳
            data['_timestamp'] = datetime.now().isoformat()
            data['_version'] = "1.0"
            
            # 序列化数据
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            
            # 加密数据
            encrypted_data = self.cipher.encrypt(json_data.encode('utf-8'))
            
            # 保存到文件
            with open(self.data_file, 'wb') as f:
                f.write(encrypted_data)
            
            # 设置文件权限
            if self.system != "Windows":
                os.chmod(self.data_file, 0o600)
            
            return True
            
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def load_data(self) -> Optional[Dict[str, Any]]:
        """加载解密数据"""
        try:
            if not os.path.exists(self.data_file):
                return None
            
            # 读取加密数据
            with open(self.data_file, 'rb') as f:
                encrypted_data = f.read()
            
            # 解密数据
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # 反序列化数据
            data = json.loads(decrypted_data.decode('utf-8'))
            
            return data
            
        except Exception as e:
            print(f"加载数据失败: {e}")
            return None
    
    def clear_data(self) -> bool:
        """清除存储的数据"""
        try:
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
            return True
        except Exception as e:
            print(f"清除数据失败: {e}")
            return False


class CookieManager:
    """Cookie管理器 - 提供Cookie的存储、验证和刷新功能"""
    
    def __init__(self):
        self.storage = SecureStorage()
        self.target_domain = "k8n.cn"
        self.target_cookie = "remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d"
    
    def save_cookies(self, cookies: List[str], user_info: Dict = None) -> bool:
        """保存Cookie到安全存储"""
        try:
            data = self.storage.load_data() or {}
            
            # 更新Cookie数据
            data['cookies'] = cookies
            data['user_info'] = user_info or {}
            data['last_updated'] = datetime.now().isoformat()
            
            # 验证Cookie有效性
            valid_cookies = []
            for cookie in cookies:
                if self.validate_cookie(cookie):
                    valid_cookies.append(cookie)
                    print(f"✅ Cookie验证通过")
                else:
                    print(f"❌ Cookie验证失败")
            
            data['cookies'] = valid_cookies
            data['validation_time'] = datetime.now().isoformat()
            
            return self.storage.save_data(data)
            
        except Exception as e:
            print(f"保存Cookie失败: {e}")
            return False
    
    def load_cookies(self) -> List[str]:
        """从安全存储加载Cookie"""
        try:
            data = self.storage.load_data()
            if not data:
                return []
            
            cookies = data.get('cookies', [])
            
            # 检查Cookie是否需要验证
            last_validation = data.get('validation_time')
            if last_validation:
                last_time = datetime.fromisoformat(last_validation)
                if datetime.now() - last_time > timedelta(hours=1):
                    # 超过1小时，重新验证
                    print("🔍 Cookie已超过1小时未验证，正在重新验证...")
                    cookies = self.refresh_cookies(cookies)
            
            return cookies
            
        except Exception as e:
            print(f"加载Cookie失败: {e}")
            return []
    
    def validate_cookie(self, cookie: str) -> bool:
        """验证Cookie有效性"""
        try:
            # 提取Cookie值
            import re
            pattern = r'remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=([^;]+)'
            match = re.search(pattern, cookie)
            
            if not match:
                return False
            
            cookie_value = match.group(1)
            
            # 发送测试请求
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Cookie': f'{self.target_cookie}={cookie_value}'
            }
            
            response = requests.get(f"http://{self.target_domain}/student", 
                                  headers=headers, timeout=10)
            
            # 检查响应
            if response.status_code == 200:
                # 检查是否包含登录页面的特征
                if "login" not in response.url and "student" in response.url:
                    return True
            
            return False
            
        except Exception as e:
            print(f"验证Cookie失败: {e}")
            return False
    
    def refresh_cookies(self, cookies: List[str]) -> List[str]:
        """刷新Cookie有效性"""
        valid_cookies = []
        
        for cookie in cookies:
            if self.validate_cookie(cookie):
                valid_cookies.append(cookie)
                print(f"✅ Cookie仍然有效")
            else:
                print(f"❌ Cookie已失效")
        
        # 更新存储
        if valid_cookies != cookies:
            data = self.storage.load_data() or {}
            data['cookies'] = valid_cookies
            data['validation_time'] = datetime.now().isoformat()
            self.storage.save_data(data)
        
        return valid_cookies
    
    def get_user_info(self) -> Dict:
        """获取用户信息"""
        try:
            data = self.storage.load_data()
            if data:
                return data.get('user_info', {})
        except:
            pass
        return {}
    
    def clear_all_data(self) -> bool:
        """清除所有存储的数据"""
        return self.storage.clear_data()


def test_secure_storage():
    """测试安全存储"""
    # 测试基本存储
    storage = SecureStorage()
    
    test_data = {
        'test_key': 'test_value',
        'number': 123,
        'list': [1, 2, 3]
    }
    
    print("测试保存数据...")
    if storage.save_data(test_data):
        print("✅ 数据保存成功")
    else:
        print("❌ 数据保存失败")
    
    print("测试加载数据...")
    loaded_data = storage.load_data()
    if loaded_data:
        print(f"✅ 数据加载成功: {loaded_data}")
    else:
        print("❌ 数据加载失败")
    
    # 测试Cookie管理
    print("\n测试Cookie管理...")
    cookie_manager = CookieManager()
    
    test_cookies = [
        "username=test;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=test_value"
    ]
    
    if cookie_manager.save_cookies(test_cookies):
        print("✅ Cookie保存成功")
    else:
        print("❌ Cookie保存失败")
    
    loaded_cookies = cookie_manager.load_cookies()
    print(f"加载的Cookie: {loaded_cookies}")


if __name__ == "__main__":
    test_secure_storage()
