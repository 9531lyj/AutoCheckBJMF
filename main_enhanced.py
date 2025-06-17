"""
AutoCheckBJMF 增强版主程序
集成了自动化配置、Cookie管理、图形界面等功能
"""
import os
import sys
import json
import time
import random
import requests
import re
import schedule
from datetime import datetime
import logging
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

try:
    from modules.gui_config import ConfigWizard
    from modules.secure_storage import CookieManager
    from modules.location_manager import LocationManager
    from modules.browser_cookie_extractor import BrowserCookieExtractor
    from modules.auto_login import AutoLogin
    from modules.class_detector import ClassDetector
except ImportError as e:
    print(f"模块导入失败: {e}")
    print("请确保所有依赖模块都已正确安装")
    sys.exit(1)


class EnhancedAutoCheckBJMF:
    """增强版自动签到主程序"""
    
    def __init__(self):
        self.config = {}
        self.cookie_manager = CookieManager()
        self.current_directory = os.getcwd()
        self.config_file = os.path.join(self.current_directory, "config.json")
        self.logger = None
        self.setup_logging()
        
        print("=" * 50)
        print("AutoCheckBJMF 增强版")
        print("项目地址：https://github.com/JasonYANG170/AutoCheckBJMF")
        print("增强功能：自动配置、安全存储、智能检测")
        print("=" * 50)
    
    def setup_logging(self):
        """设置日志系统"""
        try:
            self.logger = logging.getLogger('AutoCheckBJMF')
            self.logger.setLevel(logging.INFO)

            # 清除现有处理器，避免重复
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)

            # 创建日志目录
            log_dir = os.path.join(self.current_directory, 'logs')
            os.makedirs(log_dir, exist_ok=True)

            # 文件处理器 - 按日期轮转
            log_file = os.path.join(log_dir, f'AutoCheckBJMF_{datetime.now().strftime("%Y%m%d")}.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(file_handler)

            # 控制台处理器 - 简化格式
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(logging.INFO)
            self.logger.addHandler(console_handler)

            # 错误处理器 - 单独记录错误
            error_file = os.path.join(log_dir, f'errors_{datetime.now().strftime("%Y%m%d")}.log')
            error_handler = logging.FileHandler(error_file, encoding='utf-8')
            error_handler.setFormatter(file_formatter)
            error_handler.setLevel(logging.ERROR)
            self.logger.addHandler(error_handler)

            self.logger.info("日志系统初始化完成")

        except Exception as e:
            print(f"日志系统初始化失败: {e}")
            # 创建基本的控制台日志
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger('AutoCheckBJMF')
    
    def load_config(self) -> bool:
        """加载配置文件"""
        try:
            self.logger.info("开始加载配置文件")

            # 首先尝试从安全存储加载
            try:
                secure_data = self.cookie_manager.storage.load_data()
                if secure_data and 'user_info' in secure_data:
                    user_info = secure_data['user_info']
                    cookies = self.cookie_manager.load_cookies()

                    if cookies and user_info.get('class_id'):
                        # 验证配置完整性
                        if self._validate_config_data(user_info, cookies):
                            self.config = {
                                'class': str(user_info.get('class_id', '')),
                                'lat': str(user_info.get('location', {}).get('lat', '')),
                                'lng': str(user_info.get('location', {}).get('lng', '')),
                                'acc': str(user_info.get('location', {}).get('alt', '100')),
                                'cookie': cookies,
                                'scheduletime': user_info.get('schedule', ''),
                                'pushplus': user_info.get('push_token', ''),
                                'debug': False,
                                'configLock': True
                            }
                            self.logger.info("从安全存储加载配置成功")
                            print("✅ 从安全存储加载配置成功")
                            return True
                        else:
                            self.logger.warning("安全存储中的配置数据不完整")
            except Exception as e:
                self.logger.warning(f"从安全存储加载配置失败: {e}")

            # 尝试从传统配置文件加载
            if os.path.exists(self.config_file):
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)

                    # 验证配置文件格式
                    if self._validate_json_config(config_data):
                        self.config = config_data
                        self.logger.info("从JSON配置文件加载配置成功")
                        print("✅ 从配置文件加载配置成功")
                        return True
                    else:
                        self.logger.error("配置文件格式验证失败")
                        print("❌ 配置文件格式错误")
                        return False

                except json.JSONDecodeError as e:
                    self.logger.error(f"配置文件JSON格式错误: {e}")
                    print("❌ 配置文件JSON格式错误")
                    return False
                except Exception as e:
                    self.logger.error(f"读取配置文件失败: {e}")
                    print("❌ 读取配置文件失败")
                    return False

            self.logger.info("未找到有效的配置文件")
            return False

        except Exception as e:
            self.logger.error(f"加载配置过程中发生未预期错误: {e}", exc_info=True)
            print(f"❌ 加载配置失败: {e}")
            return False

    def _validate_config_data(self, user_info: dict, cookies: list) -> bool:
        """验证配置数据完整性"""
        try:
            # 检查必需字段
            required_fields = ['class_id']
            for field in required_fields:
                if not user_info.get(field):
                    self.logger.warning(f"缺少必需字段: {field}")
                    return False

            # 检查Cookie
            if not cookies or not isinstance(cookies, list):
                self.logger.warning("Cookie数据无效")
                return False

            # 检查位置信息
            location = user_info.get('location', {})
            if location:
                lat = location.get('lat')
                lng = location.get('lng')
                if lat is not None and lng is not None:
                    try:
                        lat_f = float(lat)
                        lng_f = float(lng)
                        if not (-90 <= lat_f <= 90 and -180 <= lng_f <= 180):
                            self.logger.warning("坐标超出有效范围")
                            return False
                    except (ValueError, TypeError):
                        self.logger.warning("坐标格式无效")
                        return False

            return True

        except Exception as e:
            self.logger.error(f"配置验证失败: {e}")
            return False

    def _validate_json_config(self, config_data: dict) -> bool:
        """验证JSON配置文件格式"""
        try:
            # 检查必需字段
            required_fields = ['class', 'lat', 'lng', 'acc', 'cookie']
            for field in required_fields:
                if field not in config_data:
                    self.logger.warning(f"配置文件缺少必需字段: {field}")
                    return False

            # 检查Cookie格式
            cookies = config_data.get('cookie', [])
            if not isinstance(cookies, list):
                self.logger.warning("Cookie字段应为列表格式")
                return False

            # 检查坐标格式
            try:
                lat = float(config_data.get('lat', 0))
                lng = float(config_data.get('lng', 0))
                if not (-90 <= lat <= 90 and -180 <= lng <= 180):
                    self.logger.warning("坐标超出有效范围")
                    return False
            except (ValueError, TypeError):
                self.logger.warning("坐标格式无效")
                return False

            # 检查定时格式
            schedule_time = config_data.get('scheduletime', '')
            if schedule_time:
                import re
                if not re.match(r'^\d{2}:\d{2}$', schedule_time):
                    self.logger.warning("定时格式无效，应为HH:MM")
                    return False

                # 检查时间范围
                try:
                    hour, minute = schedule_time.split(':')
                    hour_int = int(hour)
                    minute_int = int(minute)
                    if not (0 <= hour_int <= 23 and 0 <= minute_int <= 59):
                        self.logger.warning("时间超出有效范围")
                        return False
                except ValueError:
                    self.logger.warning("时间格式解析失败")
                    return False

            return True

        except Exception as e:
            self.logger.error(f"JSON配置验证失败: {e}")
            return False
    
    def save_config(self):
        """保存配置文件"""
        try:
            # 保存到传统配置文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            
            # 保存到安全存储
            if 'cookie' in self.config:
                location_info = {}
                if self.config.get('lat') and self.config.get('lng'):
                    location_info = {
                        'lat': float(self.config['lat']),
                        'lng': float(self.config['lng']),
                        'alt': float(self.config.get('acc', 100))
                    }
                
                user_info = {
                    'class_id': self.config.get('class', ''),
                    'location': location_info,
                    'schedule': self.config.get('scheduletime', ''),
                    'push_token': self.config.get('pushplus', '')
                }
                
                self.cookie_manager.save_cookies(self.config['cookie'], user_info)
            
            print("✅ 配置保存成功")
            
        except Exception as e:
            self.logger.error(f"保存配置失败: {e}")
    
    def run_config_wizard(self):
        """运行配置向导"""
        print("🚀 启动配置向导...")
        
        def on_wizard_complete(config):
            if config:
                self.config = config
                self.save_config()
                print("✅ 配置向导完成")
            else:
                print("❌ 配置向导被取消")
        
        try:
            wizard = ConfigWizard(on_wizard_complete)
            wizard.run()
        except Exception as e:
            self.logger.error(f"配置向导运行失败: {e}")
            return False
        
        return bool(self.config)
    
    def quick_setup(self):
        """快速设置 - 自动检测和配置"""
        print("⚡ 启动快速设置...")
        
        try:
            # 1. 自动提取浏览器Cookie
            print("🔍 正在从浏览器提取Cookie...")
            extractor = BrowserCookieExtractor()
            browser_cookies = extractor.extract_all_cookies()
            
            if browser_cookies:
                cookies = extractor.format_cookies_for_requests(browser_cookies)
                print(f"✅ 从浏览器提取到 {len(cookies)} 个Cookie")
                
                # 2. 自动检测班级
                print("🏫 正在检测班级信息...")
                detector = ClassDetector()
                class_id = detector.get_class_id_interactive(cookies[0])
                
                if class_id:
                    print(f"✅ 检测到班级ID: {class_id}")
                    
                    # 3. 自动获取位置
                    print("📍 正在获取位置信息...")
                    location_manager = LocationManager()
                    location = location_manager.get_best_location()
                    
                    if location:
                        print(f"✅ 获取位置成功: {location.get('source', '未知来源')}")
                        
                        # 4. 生成配置
                        self.config = {
                            'class': class_id,
                            'lat': str(location['lat']),
                            'lng': str(location['lng']),
                            'acc': str(location.get('alt', 100)),
                            'cookie': cookies,
                            'scheduletime': '',  # 默认手动模式
                            'pushplus': '',
                            'debug': False,
                            'configLock': True
                        }
                        
                        self.save_config()
                        print("🎉 快速设置完成！")
                        return True
            
            print("❌ 快速设置失败，将启动配置向导")
            return False
            
        except Exception as e:
            self.logger.error(f"快速设置失败: {e}")
            return False
    
    def check_and_setup_config(self):
        """检查并设置配置"""
        # 尝试加载现有配置
        if self.load_config() and self.config.get('configLock'):
            print("✅ 发现现有配置")
            self.display_config_info()
            return True
        
        print("🔧 需要进行初始配置")
        
        # 询问用户选择配置方式
        try:
            root = tk.Tk()
            root.withdraw()
            
            choice = messagebox.askyesnocancel(
                "配置选择",
                "选择配置方式：\n\n"
                "是 - 快速自动配置（推荐）\n"
                "否 - 详细配置向导\n"
                "取消 - 退出程序"
            )
            
            root.destroy()
            
            if choice is True:
                # 快速配置
                if self.quick_setup():
                    return True
                else:
                    # 快速配置失败，使用向导
                    return self.run_config_wizard()
            elif choice is False:
                # 配置向导
                return self.run_config_wizard()
            else:
                # 取消
                print("👋 程序退出")
                return False
                
        except Exception as e:
            self.logger.error(f"配置选择失败: {e}")
            # 备用方案：直接使用快速配置
            return self.quick_setup() or self.run_config_wizard()
    
    def display_config_info(self):
        """显示配置信息"""
        print("\n" + "=" * 30 + " 配置信息 " + "=" * 30)
        print(f"班级ID: {self.config.get('class', 'N/A')}")
        print(f"纬度: {self.config.get('lat', 'N/A')}")
        print(f"经度: {self.config.get('lng', 'N/A')}")
        print(f"海拔: {self.config.get('acc', 'N/A')}")
        print(f"Cookie数量: {len(self.config.get('cookie', []))}")
        
        schedule_time = self.config.get('scheduletime', '')
        if schedule_time:
            print(f"定时签到: {schedule_time}")
        else:
            print("签到模式: 手动执行")
        
        push_token = self.config.get('pushplus', '')
        if push_token:
            print("推送通知: 已配置")
        else:
            print("推送通知: 未配置")
        
        print("=" * 70)
    
    def modify_decimal_part(self, num):
        """随机经纬度偏移（保持原有逻辑）"""
        num = float(num)
        num_str = f"{num:.8f}"
        decimal_index = num_str.find('.')
        decimal_part = num_str[decimal_index + 4:decimal_index + 9]
        decimal_value = int(decimal_part)
        random_offset = random.randint(-15000, 15000)
        new_decimal_value = decimal_value + random_offset
        new_decimal_str = f"{new_decimal_value:05d}"
        new_num_str = num_str[:decimal_index + 4] + new_decimal_str + num_str[decimal_index + 9:]
        new_num = float(new_num_str)
        return new_num
    
    def qiandao(self, cookies_list):
        """签到函数（增强版）"""
        class_id = self.config.get('class', '')
        lat = self.config.get('lat', '')
        lng = self.config.get('lng', '')
        acc = self.config.get('acc', '')
        push_token = self.config.get('pushplus', '')
        
        if not all([class_id, lat, lng, acc]):
            self.logger.error("配置信息不完整，无法执行签到")
            return [], 1
        
        url = f'http://k8n.cn/student/course/{class_id}/punchs'
        error_cookies = []
        null_cookie = 0
        
        self.logger.info(f"开始签到，目标班级: {class_id}")
        
        for uid, cookie in enumerate(cookies_list):
            try:
                # 提取用户备注
                pattern = r'username=([^;]+)'
                result = re.search(pattern, cookie)
                username_string = f" <{result.group(1)}>" if result else ""
                
                print(f"🔄 用户UID: {uid+1}{username_string} 正在签到...")
                self.logger.info(f"用户UID: {uid+1}{username_string} 开始签到")
                
                # 提取Cookie值
                pattern = r'remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=([^;]+)'
                result = re.search(pattern, cookie)
                
                if not result:
                    null_cookie += 1
                    print(f"❌ Cookie格式错误")
                    continue
                
                extracted_cookie = result.group(0)
                
                # 设置请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'X-Requested-With': 'com.tencent.mm',
                    'Referer': f'http://k8n.cn/student/course/{class_id}',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Cookie': extracted_cookie
                }
                
                # 获取签到页面
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code != 200:
                    print(f"❌ 请求失败，状态码: {response.status_code}")
                    error_cookies.append(cookie)
                    continue
                
                # 解析页面内容
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                title_tag = soup.find('title')
                
                if title_tag and "出错" in title_tag.text:
                    print(f"❌ 登录状态异常")
                    self.logger.error(f"用户UID: {uid+1}{username_string} 登录状态异常")
                    error_cookies.append(cookie)
                    continue
                
                # 查找签到任务
                gps_pattern = re.compile(r'punch_gps\((\d+)\)')
                qr_pattern = re.compile(r'punchcard_(\d+)')
                
                gps_matches = gps_pattern.findall(response.text)
                qr_matches = qr_pattern.findall(response.text)
                
                all_matches = gps_matches + qr_matches
                
                if not all_matches:
                    print(f"ℹ️ 未找到进行中的签到任务")
                    continue
                
                print(f"📍 找到签到任务: GPS({len(gps_matches)}) 扫码({len(qr_matches)})")
                
                # 执行签到
                for match in all_matches:
                    sign_url = f"http://k8n.cn/student/punchs/course/{class_id}/{match}"
                    
                    # 生成随机坐标偏移
                    new_lat = self.modify_decimal_part(lat)
                    new_lng = self.modify_decimal_part(lng)
                    
                    payload = {
                        'id': match,
                        'lat': new_lat,
                        'lng': new_lng,
                        'acc': acc,
                        'res': '',
                        'gps_addr': ''
                    }
                    
                    sign_response = requests.post(sign_url, headers=headers, data=payload, timeout=10)
                    
                    if sign_response.status_code == 200:
                        sign_soup = BeautifulSoup(sign_response.text, 'html.parser')
                        div_tag = sign_soup.find('div', id='title')
                        
                        if div_tag:
                            result_text = div_tag.text.strip()
                            print(f"✅ 签到结果: {result_text}")
                            self.logger.info(f"用户UID: {uid+1}{username_string} 签到结果: {result_text}")
                            
                            # 推送通知
                            if push_token and result_text == "签到成功":
                                try:
                                    push_url = f'http://www.pushplus.plus/send?token={push_token}&title=班级魔法自动签到任务&content={result_text}'
                                    requests.get(push_url, timeout=5)
                                except:
                                    pass
                        else:
                            print(f"✅ 签到请求已发送")
                    else:
                        print(f"❌ 签到请求失败，状态码: {sign_response.status_code}")
                        error_cookies.append(cookie)
                        break
                
                # 添加延迟避免请求过快
                time.sleep(2)
                
            except Exception as e:
                self.logger.error(f"用户UID: {uid+1} 签到异常: {e}")
                error_cookies.append(cookie)
        
        return error_cookies, null_cookie
    
    def job(self):
        """签到任务（增强版）"""
        current_time = datetime.now()
        print(f"\n🚀 开始执行签到任务，当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"开始执行签到任务")
        
        # 刷新Cookie有效性
        cookies = self.cookie_manager.refresh_cookies(self.config.get('cookie', []))
        
        if not cookies:
            print("❌ 没有有效的Cookie，请重新配置")
            self.logger.error("没有有效的Cookie")
            return
        
        # 执行签到
        error_cookies, null_cookie = self.qiandao(cookies)
        
        # 处理重试
        retry_count = 0
        max_retries = 2
        retry_delays = [300, 900]  # 5分钟，15分钟
        
        while error_cookies and retry_count < max_retries:
            delay = retry_delays[retry_count]
            print(f"⏳ 检测到 {len(error_cookies)} 个Cookie签到失败，{delay//60}分钟后重试...")
            self.logger.warning(f"重试队列: {len(error_cookies)} 个Cookie，等待 {delay} 秒")
            
            time.sleep(delay)
            
            print(f"🔄 开始第 {retry_count + 1} 次重试...")
            error_cookies, _ = self.qiandao(error_cookies)
            retry_count += 1
        
        # 签到结果统计
        total_cookies = len(self.config.get('cookie', []))
        success_count = total_cookies - len(error_cookies) - null_cookie
        
        if error_cookies:
            print(f"❌ 仍有 {len(error_cookies)} 个Cookie签到失败，请检查Cookie是否过期")
            self.logger.error(f"最终失败Cookie数量: {len(error_cookies)}")
        elif null_cookie > 0:
            print(f"⚠️ 有 {null_cookie} 个Cookie格式异常")
            self.logger.warning(f"异常Cookie数量: {null_cookie}")
        else:
            print("🎉 本次签到圆满成功！")
            self.logger.info("签到任务完成，全部成功")
        
        print(f"📊 签到统计: 成功 {success_count}/{total_cookies}")
        print("=" * 50)
        
        # 更新Cookie存储
        if success_count > 0:
            valid_cookies = [c for c in self.config.get('cookie', []) if c not in error_cookies]
            self.config['cookie'] = valid_cookies
            self.save_config()
    
    def run(self):
        """主运行函数"""
        try:
            # 检查和设置配置
            if not self.check_and_setup_config():
                print("❌ 配置失败，程序退出")
                return
            
            print("🎯 程序启动成功！")
            
            # 检查定时设置
            schedule_time = self.config.get('scheduletime', '')
            
            if schedule_time:
                print(f"⏰ 定时签到模式，设定时间: {schedule_time}")
                
                # 设置定时任务
                schedule.every().day.at(schedule_time).do(self.job)
                
                print(f"⏳ 等待定时时间到达...")
                
                while True:
                    schedule.run_pending()
                    time.sleep(60)  # 每分钟检查一次
            else:
                print("🚀 手动签到模式，立即执行")
                self.job()
                input("\n✅ 手动签到已完成，按回车键退出...")
        
        except KeyboardInterrupt:
            print("\n👋 程序被用户中断")
        except Exception as e:
            self.logger.error(f"程序运行异常: {e}")
            print(f"❌ 程序运行异常: {e}")
        finally:
            print("👋 程序结束")


def main():
    """主函数"""
    app = EnhancedAutoCheckBJMF()
    app.run()


if __name__ == "__main__":
    main()
