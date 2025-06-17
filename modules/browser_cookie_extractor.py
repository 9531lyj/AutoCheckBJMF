"""
浏览器Cookie提取模块
支持从Chrome、Edge、Firefox等主流浏览器自动提取Cookie
"""
import os
import sqlite3
import json
import platform
import shutil
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class BrowserCookieExtractor:
    """浏览器Cookie提取器"""
    
    def __init__(self):
        self.system = platform.system()
        self.target_domain = "k8n.cn"
        self.target_cookie = "remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d"
    
    def get_browser_paths(self) -> Dict[str, str]:
        """获取不同浏览器的Cookie数据库路径"""
        paths = {}
        
        if self.system == "Windows":
            user_data = os.path.expanduser("~")
            paths = {
                'chrome': os.path.join(user_data, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cookies"),
                'edge': os.path.join(user_data, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cookies"),
                'firefox': self._get_firefox_profile_path(),
                'opera': os.path.join(user_data, "AppData", "Roaming", "Opera Software", "Opera Stable", "Cookies"),
                'brave': os.path.join(user_data, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Cookies")
            }
        elif self.system == "Darwin":  # macOS
            user_data = os.path.expanduser("~")
            paths = {
                'chrome': os.path.join(user_data, "Library", "Application Support", "Google", "Chrome", "Default", "Cookies"),
                'edge': os.path.join(user_data, "Library", "Application Support", "Microsoft Edge", "Default", "Cookies"),
                'firefox': self._get_firefox_profile_path(),
                'safari': os.path.join(user_data, "Library", "Cookies", "Cookies.binarycookies"),
                'opera': os.path.join(user_data, "Library", "Application Support", "com.operasoftware.Opera", "Cookies"),
                'brave': os.path.join(user_data, "Library", "Application Support", "BraveSoftware", "Brave-Browser", "Default", "Cookies")
            }
        elif self.system == "Linux":
            user_data = os.path.expanduser("~")
            paths = {
                'chrome': os.path.join(user_data, ".config", "google-chrome", "Default", "Cookies"),
                'chromium': os.path.join(user_data, ".config", "chromium", "Default", "Cookies"),
                'firefox': self._get_firefox_profile_path(),
                'opera': os.path.join(user_data, ".config", "opera", "Cookies"),
                'brave': os.path.join(user_data, ".config", "BraveSoftware", "Brave-Browser", "Default", "Cookies")
            }
        
        return {k: v for k, v in paths.items() if v and os.path.exists(v)}
    
    def _get_firefox_profile_path(self) -> Optional[str]:
        """获取Firefox配置文件路径"""
        try:
            if self.system == "Windows":
                firefox_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
            elif self.system == "Darwin":
                firefox_dir = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Firefox", "Profiles")
            elif self.system == "Linux":
                firefox_dir = os.path.join(os.path.expanduser("~"), ".mozilla", "firefox")
            else:
                return None
            
            if os.path.exists(firefox_dir):
                # 查找默认配置文件
                for profile in os.listdir(firefox_dir):
                    if profile.endswith('.default') or profile.endswith('.default-release'):
                        cookies_path = os.path.join(firefox_dir, profile, "cookies.sqlite")
                        if os.path.exists(cookies_path):
                            return cookies_path
        except Exception as e:
            print(f"获取Firefox配置文件路径失败: {e}")
        
        return None
    
    def extract_chrome_cookies(self, cookies_path: str) -> List[Dict]:
        """从Chrome/Edge/Brave等Chromium浏览器提取Cookie"""
        cookies = []
        temp_db = None
        
        try:
            # 复制数据库文件到临时位置（避免锁定问题）
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            shutil.copy2(cookies_path, temp_db.name)
            temp_db.close()
            
            # 连接数据库
            conn = sqlite3.connect(temp_db.name)
            cursor = conn.cursor()
            
            # 查询目标域名的Cookie
            query = """
            SELECT name, value, host_key, path, expires_utc, is_secure, is_httponly, encrypted_value
            FROM cookies 
            WHERE host_key LIKE ? OR host_key LIKE ?
            """
            
            cursor.execute(query, (f'%{self.target_domain}%', f'%.{self.target_domain}%'))
            rows = cursor.fetchall()
            
            for row in rows:
                name, value, host_key, path, expires_utc, is_secure, is_httponly, encrypted_value = row
                
                # 如果value为空但有encrypted_value，尝试解密
                if not value and encrypted_value:
                    try:
                        value = self._decrypt_chrome_cookie(encrypted_value)
                    except Exception as e:
                        print(f"解密Cookie失败: {e}")
                        continue
                
                if name == self.target_cookie and value:
                    cookies.append({
                        'name': name,
                        'value': value,
                        'domain': host_key,
                        'path': path,
                        'expires': expires_utc,
                        'secure': bool(is_secure),
                        'httponly': bool(is_httponly),
                        'browser': 'chrome-based'
                    })
            
            conn.close()
            
        except Exception as e:
            print(f"提取Chrome Cookie失败: {e}")
        finally:
            # 清理临时文件
            if temp_db and os.path.exists(temp_db.name):
                try:
                    os.unlink(temp_db.name)
                except:
                    pass
        
        return cookies
    
    def _decrypt_chrome_cookie(self, encrypted_value: bytes) -> str:
        """解密Chrome Cookie值"""
        try:
            if self.system == "Windows":
                # Windows使用DPAPI
                import win32crypt
                return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8')
            elif self.system == "Darwin":
                # macOS使用Keychain
                return self._decrypt_macos_chrome_cookie(encrypted_value)
            elif self.system == "Linux":
                # Linux使用密钥文件
                return self._decrypt_linux_chrome_cookie(encrypted_value)
        except Exception as e:
            print(f"解密Cookie失败: {e}")
            return ""
    
    def _decrypt_macos_chrome_cookie(self, encrypted_value: bytes) -> str:
        """解密macOS Chrome Cookie"""
        try:
            import keyring
            # 从Keychain获取密钥
            password = keyring.get_password("Chrome Safe Storage", "Chrome")
            if not password:
                return ""
            
            # 使用密钥解密
            key = PBKDF2HMAC(
                algorithm=hashes.SHA1(),
                length=16,
                salt=b'saltysalt',
                iterations=1003,
            ).derive(password.encode())
            
            # 移除前缀并解密
            encrypted_value = encrypted_value[3:]  # 移除'v10'前缀
            cipher = Fernet(base64.urlsafe_b64encode(key))
            return cipher.decrypt(encrypted_value).decode('utf-8')
            
        except Exception as e:
            print(f"macOS Cookie解密失败: {e}")
            return ""
    
    def _decrypt_linux_chrome_cookie(self, encrypted_value: bytes) -> str:
        """解密Linux Chrome Cookie"""
        try:
            # Linux Chrome使用固定密钥
            password = "peanuts".encode('utf8')
            key = PBKDF2HMAC(
                algorithm=hashes.SHA1(),
                length=16,
                salt=b'saltysalt',
                iterations=1,
            ).derive(password)
            
            # 移除前缀并解密
            encrypted_value = encrypted_value[3:]  # 移除'v11'前缀
            cipher = Fernet(base64.urlsafe_b64encode(key))
            return cipher.decrypt(encrypted_value).decode('utf-8')
            
        except Exception as e:
            print(f"Linux Cookie解密失败: {e}")
            return ""
    
    def extract_firefox_cookies(self, cookies_path: str) -> List[Dict]:
        """从Firefox提取Cookie"""
        cookies = []
        temp_db = None
        
        try:
            # 复制数据库文件
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            shutil.copy2(cookies_path, temp_db.name)
            temp_db.close()
            
            # 连接数据库
            conn = sqlite3.connect(temp_db.name)
            cursor = conn.cursor()
            
            # Firefox数据库结构
            query = """
            SELECT name, value, host, path, expiry, isSecure, isHttpOnly
            FROM moz_cookies 
            WHERE host LIKE ? OR host LIKE ?
            """
            
            cursor.execute(query, (f'%{self.target_domain}%', f'%.{self.target_domain}%'))
            rows = cursor.fetchall()
            
            for row in rows:
                name, value, host, path, expiry, is_secure, is_httponly = row
                
                if name == self.target_cookie and value:
                    cookies.append({
                        'name': name,
                        'value': value,
                        'domain': host,
                        'path': path,
                        'expires': expiry,
                        'secure': bool(is_secure),
                        'httponly': bool(is_httponly),
                        'browser': 'firefox'
                    })
            
            conn.close()
            
        except Exception as e:
            print(f"提取Firefox Cookie失败: {e}")
        finally:
            if temp_db and os.path.exists(temp_db.name):
                try:
                    os.unlink(temp_db.name)
                except:
                    pass
        
        return cookies
    
    def extract_all_cookies(self) -> List[Dict]:
        """从所有支持的浏览器提取Cookie"""
        all_cookies = []
        browser_paths = self.get_browser_paths()
        
        print(f"🔍 检测到 {len(browser_paths)} 个浏览器")
        
        for browser, path in browser_paths.items():
            try:
                print(f"📖 正在从 {browser} 提取Cookie...")
                
                if browser == 'firefox':
                    cookies = self.extract_firefox_cookies(path)
                else:
                    cookies = self.extract_chrome_cookies(path)
                
                if cookies:
                    print(f"✅ 从 {browser} 提取到 {len(cookies)} 个相关Cookie")
                    for cookie in cookies:
                        cookie['source_browser'] = browser
                    all_cookies.extend(cookies)
                else:
                    print(f"❌ 从 {browser} 未找到目标Cookie")
                    
            except Exception as e:
                print(f"❌ 从 {browser} 提取Cookie失败: {e}")
        
        return all_cookies
    
    def format_cookies_for_requests(self, cookies: List[Dict]) -> List[str]:
        """将Cookie格式化为requests可用的格式"""
        formatted_cookies = []
        
        for cookie in cookies:
            if cookie['name'] == self.target_cookie:
                # 格式化为程序需要的格式
                cookie_string = f"{cookie['name']}={cookie['value']}"
                
                # 添加浏览器信息作为备注
                browser_info = cookie.get('source_browser', 'unknown')
                formatted_cookie = f"username=从{browser_info}提取;{cookie_string}"
                
                formatted_cookies.append(formatted_cookie)
        
        return formatted_cookies


def test_browser_cookie_extractor():
    """测试浏览器Cookie提取器"""
    extractor = BrowserCookieExtractor()
    cookies = extractor.extract_all_cookies()
    
    if cookies:
        print(f"\n✅ 总共提取到 {len(cookies)} 个Cookie")
        formatted = extractor.format_cookies_for_requests(cookies)
        for cookie in formatted:
            print(f"Cookie: {cookie[:50]}...")
    else:
        print("❌ 未找到任何Cookie")


if __name__ == "__main__":
    test_browser_cookie_extractor()
