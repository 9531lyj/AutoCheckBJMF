"""
自动登录和Cookie获取模块
使用Selenium/Playwright实现自动登录并提取Cookie
"""
import time
import json
import os
from typing import Optional, Dict, List
import tkinter as tk
from tkinter import messagebox, simpledialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException, WebDriverException


class AutoLogin:
    """自动登录管理器"""
    
    def __init__(self):
        self.login_url = "https://k8n.cn/student/login"
        self.target_cookie = "remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d"
        self.driver = None
    
    def get_available_browsers(self) -> List[str]:
        """检测可用的浏览器"""
        browsers = []
        
        # 检测Chrome
        try:
            options = ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=options)
            driver.quit()
            browsers.append('chrome')
        except:
            pass
        
        # 检测Edge
        try:
            options = EdgeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Edge(options=options)
            driver.quit()
            browsers.append('edge')
        except:
            pass
        
        # 检测Firefox
        try:
            options = FirefoxOptions()
            options.add_argument('--headless')
            driver = webdriver.Firefox(options=options)
            driver.quit()
            browsers.append('firefox')
        except:
            pass
        
        return browsers
    
    def create_driver(self, browser: str = 'chrome', headless: bool = False) -> webdriver:
        """创建WebDriver实例"""
        try:
            if browser == 'chrome':
                options = ChromeOptions()
                if headless:
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                
                driver = webdriver.Chrome(options=options)
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
            elif browser == 'edge':
                options = EdgeOptions()
                if headless:
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                
                driver = webdriver.Edge(options=options)
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
            elif browser == 'firefox':
                options = FirefoxOptions()
                if headless:
                    options.add_argument('--headless')
                options.set_preference("dom.webdriver.enabled", False)
                options.set_preference('useAutomationExtension', False)
                
                driver = webdriver.Firefox(options=options)
                
            else:
                raise ValueError(f"不支持的浏览器: {browser}")
            
            return driver
            
        except Exception as e:
            raise Exception(f"创建{browser}驱动失败: {e}")
    
    def manual_login_with_browser(self, browser: str = 'chrome') -> Optional[str]:
        """手动登录模式 - 打开浏览器让用户手动登录"""
        try:
            print(f"🌐 正在启动 {browser} 浏览器...")
            self.driver = self.create_driver(browser, headless=False)
            
            # 访问登录页面
            self.driver.get(self.login_url)
            print("📱 请在浏览器中完成登录...")
            
            # 等待用户登录
            root = tk.Tk()
            root.withdraw()
            
            messagebox.showinfo(
                "手动登录",
                f"浏览器已打开登录页面。\n\n"
                f"请在浏览器中完成登录，然后点击确定。\n"
                f"程序将自动提取Cookie。"
            )
            
            # 检查是否登录成功
            current_url = self.driver.current_url
            if "student" in current_url and "login" not in current_url:
                # 登录成功，提取Cookie
                cookies = self.driver.get_cookies()
                target_cookie = None
                
                for cookie in cookies:
                    if cookie['name'] == self.target_cookie:
                        target_cookie = cookie['value']
                        break
                
                if target_cookie:
                    print("✅ Cookie提取成功")
                    formatted_cookie = f"username=手动登录;{self.target_cookie}={target_cookie}"
                    return formatted_cookie
                else:
                    print("❌ 未找到目标Cookie")
            else:
                print("❌ 登录失败或未完成登录")
            
            root.destroy()
            
        except Exception as e:
            print(f"手动登录失败: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        return None
    
    def auto_login_with_credentials(self, username: str, password: str, browser: str = 'chrome') -> Optional[str]:
        """自动登录模式 - 使用用户名密码自动登录"""
        try:
            print(f"🤖 正在使用 {browser} 自动登录...")
            self.driver = self.create_driver(browser, headless=True)
            
            # 访问登录页面
            self.driver.get(self.login_url)
            
            # 等待页面加载
            wait = WebDriverWait(self.driver, 10)
            
            # 查找并填写用户名
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_field.clear()
            username_field.send_keys(username)
            
            # 查找并填写密码
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(password)
            
            # 查找并点击登录按钮
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # 等待登录完成
            time.sleep(3)
            
            # 检查是否登录成功
            current_url = self.driver.current_url
            if "student" in current_url and "login" not in current_url:
                # 登录成功，提取Cookie
                cookies = self.driver.get_cookies()
                target_cookie = None
                
                for cookie in cookies:
                    if cookie['name'] == self.target_cookie:
                        target_cookie = cookie['value']
                        break
                
                if target_cookie:
                    print("✅ 自动登录成功，Cookie提取完成")
                    formatted_cookie = f"username={username};{self.target_cookie}={target_cookie}"
                    return formatted_cookie
                else:
                    print("❌ 登录成功但未找到目标Cookie")
            else:
                # 检查是否有错误信息
                try:
                    error_element = self.driver.find_element(By.CLASS_NAME, "alert-danger")
                    error_message = error_element.text
                    print(f"❌ 登录失败: {error_message}")
                except:
                    print("❌ 登录失败: 未知错误")
            
        except TimeoutException:
            print("❌ 登录超时，请检查网络连接")
        except WebDriverException as e:
            print(f"❌ 浏览器错误: {e}")
        except Exception as e:
            print(f"❌ 自动登录失败: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        return None
    
    def get_login_credentials(self) -> Optional[tuple]:
        """获取登录凭据"""
        try:
            root = tk.Tk()
            root.withdraw()
            
            # 询问登录方式
            choice = messagebox.askyesnocancel(
                "登录方式选择",
                "选择登录方式：\n\n"
                "是 - 自动登录（需要输入用户名密码）\n"
                "否 - 手动登录（打开浏览器手动操作）\n"
                "取消 - 跳过自动登录"
            )
            
            if choice is True:
                # 自动登录
                username = simpledialog.askstring("用户名", "请输入学号/用户名:")
                if username:
                    password = simpledialog.askstring("密码", "请输入密码:", show='*')
                    if password:
                        return (username, password, 'auto')
            elif choice is False:
                # 手动登录
                return (None, None, 'manual')
            
            root.destroy()
            
        except Exception as e:
            print(f"获取登录凭据失败: {e}")
        
        return None
    
    def login_and_get_cookie(self) -> Optional[str]:
        """登录并获取Cookie的主要方法"""
        # 检测可用浏览器
        browsers = self.get_available_browsers()
        
        if not browsers:
            print("❌ 未检测到可用的浏览器驱动")
            print("请安装Chrome、Edge或Firefox浏览器及对应的WebDriver")
            return None
        
        print(f"✅ 检测到可用浏览器: {', '.join(browsers)}")
        
        # 选择浏览器
        browser = browsers[0]  # 默认使用第一个可用浏览器
        if len(browsers) > 1:
            try:
                root = tk.Tk()
                root.withdraw()
                
                browser_choice = messagebox.askyesnocancel(
                    "浏览器选择",
                    f"检测到多个浏览器：{', '.join(browsers)}\n\n"
                    f"是 - 使用 {browsers[0]}\n"
                    f"否 - 使用 {browsers[1] if len(browsers) > 1 else browsers[0]}\n"
                    f"取消 - 使用默认浏览器"
                )
                
                if browser_choice is False and len(browsers) > 1:
                    browser = browsers[1]
                
                root.destroy()
                
            except:
                pass
        
        # 获取登录凭据
        credentials = self.get_login_credentials()
        if not credentials:
            return None
        
        username, password, mode = credentials
        
        # 执行登录
        if mode == 'auto' and username and password:
            return self.auto_login_with_credentials(username, password, browser)
        elif mode == 'manual':
            return self.manual_login_with_browser(browser)
        
        return None


def test_auto_login():
    """测试自动登录"""
    login_manager = AutoLogin()
    cookie = login_manager.login_and_get_cookie()
    
    if cookie:
        print(f"✅ 获取到Cookie: {cookie[:50]}...")
    else:
        print("❌ 未能获取Cookie")


if __name__ == "__main__":
    test_auto_login()
