"""
图形化配置界面
提供用户友好的配置向导和管理界面
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import json
from typing import Dict, List, Optional, Callable
try:
    from .location_manager import LocationManager
    from .browser_cookie_extractor import BrowserCookieExtractor
    from .auto_login import AutoLogin
    from .class_detector import ClassDetector
    from .secure_storage import CookieManager
except ImportError:
    # 如果作为独立模块运行，使用绝对导入
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from modules.location_manager import LocationManager
    from modules.browser_cookie_extractor import BrowserCookieExtractor
    from modules.auto_login import AutoLogin
    from modules.class_detector import ClassDetector
    from modules.secure_storage import CookieManager


class ConfigWizard:
    """配置向导 - 引导用户完成初始配置"""
    
    def __init__(self, on_complete: Callable = None):
        self.on_complete = on_complete
        self.config_data = {}
        self.current_step = 0
        self.steps = [
            ("欢迎", self.welcome_step),
            ("位置配置", self.location_step),
            ("Cookie配置", self.cookie_step),
            ("班级选择", self.class_step),
            ("定时设置", self.schedule_step),
            ("完成配置", self.finish_step)
        ]
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("AutoCheckBJMF 配置向导")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        self.show_current_step()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        self.title_label = ttk.Label(
            self.main_frame, 
            text="", 
            font=('Arial', 16, 'bold')
        )
        self.title_label.pack(pady=(0, 20))
        
        # 进度条
        self.progress = ttk.Progressbar(
            self.main_frame, 
            length=400, 
            mode='determinate'
        )
        self.progress.pack(pady=(0, 20))
        
        # 内容框架
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 按钮框架
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 按钮
        self.prev_button = ttk.Button(
            self.button_frame, 
            text="上一步", 
            command=self.prev_step
        )
        self.prev_button.pack(side=tk.LEFT)
        
        self.next_button = ttk.Button(
            self.button_frame, 
            text="下一步", 
            command=self.next_step
        )
        self.next_button.pack(side=tk.RIGHT)
        
        self.cancel_button = ttk.Button(
            self.button_frame, 
            text="取消", 
            command=self.cancel
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=(0, 10))
    
    def show_current_step(self):
        """显示当前步骤"""
        if 0 <= self.current_step < len(self.steps):
            step_name, step_func = self.steps[self.current_step]
            
            # 更新标题和进度
            self.title_label.config(text=f"步骤 {self.current_step + 1}/{len(self.steps)}: {step_name}")
            self.progress['value'] = (self.current_step + 1) / len(self.steps) * 100
            
            # 清空内容框架
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # 显示步骤内容
            step_func()
            
            # 更新按钮状态
            self.prev_button.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
            self.next_button.config(text="完成" if self.current_step == len(self.steps) - 1 else "下一步")
    
    def welcome_step(self):
        """欢迎步骤"""
        welcome_text = """
        欢迎使用 AutoCheckBJMF 自动签到工具！
        
        本向导将帮助您完成初始配置，包括：
        
        • 📍 自动获取GPS位置信息
        • 🍪 自动提取或配置Cookie
        • 🏫 自动检测班级信息
        • ⏰ 设置定时签到任务
        
        整个过程大约需要3-5分钟。
        
        点击"下一步"开始配置。
        """
        
        text_widget = tk.Text(
            self.content_frame, 
            wrap=tk.WORD, 
            font=('Arial', 11),
            bg=self.root.cget('bg'),
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        text_widget.pack(fill=tk.BOTH, expand=True, pady=20)
        
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, welcome_text)
        text_widget.config(state=tk.DISABLED)
    
    def location_step(self):
        """位置配置步骤"""
        ttk.Label(
            self.content_frame, 
            text="正在获取您的位置信息...",
            font=('Arial', 12)
        ).pack(pady=20)
        
        self.location_status = ttk.Label(
            self.content_frame, 
            text="🌍 正在定位...",
            font=('Arial', 10)
        )
        self.location_status.pack(pady=10)
        
        # 位置信息显示框架
        self.location_info_frame = ttk.LabelFrame(
            self.content_frame, 
            text="位置信息", 
            padding="10"
        )
        self.location_info_frame.pack(fill=tk.X, pady=20)
        
        # 在后台获取位置
        threading.Thread(target=self.get_location, daemon=True).start()
    
    def get_location(self):
        """获取位置信息"""
        try:
            location_manager = LocationManager()
            location = location_manager.get_best_location()
            
            # 更新UI（需要在主线程中执行）
            self.root.after(0, self.update_location_ui, location)
            
        except Exception as e:
            self.root.after(0, self.update_location_ui, None, str(e))
    
    def update_location_ui(self, location: Dict = None, error: str = None):
        """更新位置UI"""
        if error:
            self.location_status.config(text=f"❌ 定位失败: {error}")
            return
        
        if location:
            self.config_data['location'] = location
            self.location_status.config(text="✅ 定位成功")
            
            # 显示位置信息
            info_text = f"""
            纬度: {location['lat']:.8f}
            经度: {location['lng']:.8f}
            来源: {location.get('source', '未知')}
            """
            
            if 'city' in location:
                info_text += f"\n城市: {location['city']}"
            
            ttk.Label(
                self.location_info_frame, 
                text=info_text,
                font=('Arial', 10)
            ).pack()
            
            # 添加手动调整选项
            ttk.Button(
                self.location_info_frame,
                text="手动调整位置",
                command=self.manual_adjust_location
            ).pack(pady=(10, 0))
    
    def manual_adjust_location(self):
        """手动调整位置"""
        # 创建位置调整对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("调整位置")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 当前位置
        current_location = self.config_data.get('location', {})
        
        ttk.Label(dialog, text="请输入精确的位置坐标：").pack(pady=10)
        
        # 纬度输入
        lat_frame = ttk.Frame(dialog)
        lat_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(lat_frame, text="纬度:").pack(side=tk.LEFT)
        lat_var = tk.StringVar(value=str(current_location.get('lat', '')))
        lat_entry = ttk.Entry(lat_frame, textvariable=lat_var)
        lat_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # 经度输入
        lng_frame = ttk.Frame(dialog)
        lng_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(lng_frame, text="经度:").pack(side=tk.LEFT)
        lng_var = tk.StringVar(value=str(current_location.get('lng', '')))
        lng_entry = ttk.Entry(lng_frame, textvariable=lng_var)
        lng_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # 海拔输入
        alt_frame = ttk.Frame(dialog)
        alt_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(alt_frame, text="海拔:").pack(side=tk.LEFT)
        alt_var = tk.StringVar(value="100")
        alt_entry = ttk.Entry(alt_frame, textvariable=alt_var)
        alt_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        def save_location():
            try:
                lat = float(lat_var.get())
                lng = float(lng_var.get())
                alt = float(alt_var.get())
                
                self.config_data['location'] = {
                    'lat': lat,
                    'lng': lng,
                    'alt': alt,
                    'source': '手动输入'
                }
                
                dialog.destroy()
                self.update_location_ui(self.config_data['location'])
                
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
        
        ttk.Button(button_frame, text="保存", command=save_location).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=(0, 10))
        
        # 添加地图选择按钮
        def open_map():
            import webbrowser
            webbrowser.open('https://lbs.qq.com/getPoint/')
            messagebox.showinfo("提示", "请在打开的地图中选择位置，然后复制坐标到输入框中")
        
        ttk.Button(button_frame, text="打开地图选择", command=open_map).pack(side=tk.LEFT)
    
    def cookie_step(self):
        """Cookie配置步骤"""
        ttk.Label(
            self.content_frame, 
            text="配置登录Cookie",
            font=('Arial', 12, 'bold')
        ).pack(pady=(0, 20))
        
        # Cookie获取方式选择
        method_frame = ttk.LabelFrame(self.content_frame, text="选择Cookie获取方式", padding="10")
        method_frame.pack(fill=tk.X, pady=10)
        
        self.cookie_method = tk.StringVar(value="browser")
        
        ttk.Radiobutton(
            method_frame,
            text="🌐 从浏览器自动提取（推荐）",
            variable=self.cookie_method,
            value="browser"
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            method_frame,
            text="🤖 自动登录获取",
            variable=self.cookie_method,
            value="auto_login"
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            method_frame,
            text="✋ 手动输入",
            variable=self.cookie_method,
            value="manual"
        ).pack(anchor=tk.W, pady=2)
        
        # 获取Cookie按钮
        ttk.Button(
            self.content_frame,
            text="获取Cookie",
            command=self.get_cookies
        ).pack(pady=20)
        
        # Cookie状态显示
        self.cookie_status = ttk.Label(
            self.content_frame,
            text="请选择获取方式并点击获取Cookie",
            font=('Arial', 10)
        )
        self.cookie_status.pack(pady=10)
    
    def get_cookies(self):
        """获取Cookie"""
        method = self.cookie_method.get()
        self.cookie_status.config(text="🔄 正在获取Cookie...")
        
        # 在后台执行
        threading.Thread(target=self._get_cookies_background, args=(method,), daemon=True).start()
    
    def _get_cookies_background(self, method: str):
        """后台获取Cookie"""
        try:
            cookies = []
            
            if method == "browser":
                # 从浏览器提取
                extractor = BrowserCookieExtractor()
                browser_cookies = extractor.extract_all_cookies()
                cookies = extractor.format_cookies_for_requests(browser_cookies)
                
            elif method == "auto_login":
                # 自动登录
                auto_login = AutoLogin()
                cookie = auto_login.login_and_get_cookie()
                if cookie:
                    cookies = [cookie]
                    
            elif method == "manual":
                # 手动输入
                self.root.after(0, self.manual_cookie_input)
                return
            
            # 更新UI
            self.root.after(0, self.update_cookie_ui, cookies)
            
        except Exception as e:
            self.root.after(0, self.update_cookie_ui, [], str(e))
    
    def update_cookie_ui(self, cookies: List[str], error: str = None):
        """更新Cookie UI"""
        if error:
            self.cookie_status.config(text=f"❌ 获取失败: {error}")
            return
        
        if cookies:
            self.config_data['cookies'] = cookies
            self.cookie_status.config(text=f"✅ 成功获取 {len(cookies)} 个Cookie")
        else:
            self.cookie_status.config(text="❌ 未找到有效的Cookie")
    
    def manual_cookie_input(self):
        """手动输入Cookie"""
        # 创建Cookie输入对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("手动输入Cookie")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="请输入Cookie（每行一个）：").pack(pady=10)
        
        text_widget = tk.Text(dialog, height=15, width=70)
        text_widget.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # 添加说明
        help_text = """
        Cookie格式示例：
        username=用户名;remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=cookie值
        
        获取方法：
        1. 打开浏览器访问 https://k8n.cn/student/login
        2. 登录后按F12打开开发者工具
        3. 在Network标签页中找到请求，复制Cookie值
        """
        
        ttk.Label(dialog, text=help_text, font=('Arial', 9)).pack(padx=20, pady=(0, 10))
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        def save_cookies():
            content = text_widget.get("1.0", tk.END).strip()
            if content:
                cookies = [line.strip() for line in content.split('\n') if line.strip()]
                self.config_data['cookies'] = cookies
                dialog.destroy()
                self.update_cookie_ui(cookies)
            else:
                messagebox.showwarning("警告", "请输入至少一个Cookie")
        
        ttk.Button(button_frame, text="保存", command=save_cookies).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=(0, 10))
    
    def class_step(self):
        """班级选择步骤"""
        ttk.Label(
            self.content_frame, 
            text="检测班级信息",
            font=('Arial', 12, 'bold')
        ).pack(pady=(0, 20))
        
        self.class_status = ttk.Label(
            self.content_frame,
            text="请先配置Cookie",
            font=('Arial', 10)
        )
        self.class_status.pack(pady=10)
        
        if 'cookies' in self.config_data and self.config_data['cookies']:
            self.class_status.config(text="🔍 正在检测班级...")
            threading.Thread(target=self.detect_classes, daemon=True).start()
        else:
            ttk.Button(
                self.content_frame,
                text="返回配置Cookie",
                command=lambda: self.goto_step(2)
            ).pack(pady=20)
    
    def detect_classes(self):
        """检测班级"""
        try:
            detector = ClassDetector()
            cookies = self.config_data.get('cookies', [])
            
            if cookies:
                # 使用第一个Cookie检测班级
                first_cookie = cookies[0]
                class_id = detector.get_class_id_interactive(first_cookie)
                
                self.root.after(0, self.update_class_ui, class_id)
            else:
                self.root.after(0, self.update_class_ui, None, "没有可用的Cookie")
                
        except Exception as e:
            self.root.after(0, self.update_class_ui, None, str(e))
    
    def update_class_ui(self, class_id: str = None, error: str = None):
        """更新班级UI"""
        if error:
            self.class_status.config(text=f"❌ 检测失败: {error}")
            return
        
        if class_id:
            self.config_data['class_id'] = class_id
            self.class_status.config(text=f"✅ 检测到班级ID: {class_id}")
        else:
            self.class_status.config(text="❌ 未检测到班级信息")
    
    def schedule_step(self):
        """定时设置步骤"""
        ttk.Label(
            self.content_frame, 
            text="设置定时签到",
            font=('Arial', 12, 'bold')
        ).pack(pady=(0, 20))
        
        # 定时选项
        schedule_frame = ttk.LabelFrame(self.content_frame, text="签到模式", padding="10")
        schedule_frame.pack(fill=tk.X, pady=10)
        
        self.schedule_mode = tk.StringVar(value="manual")
        
        ttk.Radiobutton(
            schedule_frame,
            text="手动签到（立即执行）",
            variable=self.schedule_mode,
            value="manual"
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            schedule_frame,
            text="定时签到",
            variable=self.schedule_mode,
            value="scheduled"
        ).pack(anchor=tk.W, pady=2)
        
        # 时间设置
        time_frame = ttk.Frame(self.content_frame)
        time_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(time_frame, text="签到时间:").pack(side=tk.LEFT)
        
        self.hour_var = tk.StringVar(value="08")
        self.minute_var = tk.StringVar(value="00")
        
        hour_spinbox = ttk.Spinbox(
            time_frame, 
            from_=0, 
            to=23, 
            width=3, 
            textvariable=self.hour_var,
            format="%02.0f"
        )
        hour_spinbox.pack(side=tk.LEFT, padx=(10, 5))
        
        ttk.Label(time_frame, text=":").pack(side=tk.LEFT)
        
        minute_spinbox = ttk.Spinbox(
            time_frame, 
            from_=0, 
            to=59, 
            width=3, 
            textvariable=self.minute_var,
            format="%02.0f"
        )
        minute_spinbox.pack(side=tk.LEFT, padx=(5, 0))
        
        # 推送设置
        push_frame = ttk.LabelFrame(self.content_frame, text="推送通知（可选）", padding="10")
        push_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(push_frame, text="PushPlus Token:").pack(anchor=tk.W)
        self.push_token_var = tk.StringVar()
        ttk.Entry(push_frame, textvariable=self.push_token_var, width=50).pack(fill=tk.X, pady=(5, 0))
    
    def finish_step(self):
        """完成配置步骤"""
        ttk.Label(
            self.content_frame, 
            text="配置完成！",
            font=('Arial', 16, 'bold')
        ).pack(pady=(0, 20))
        
        # 配置摘要
        summary_frame = ttk.LabelFrame(self.content_frame, text="配置摘要", padding="10")
        summary_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        summary_text = self.generate_summary()
        
        text_widget = tk.Text(
            summary_frame, 
            wrap=tk.WORD, 
            font=('Arial', 10),
            state=tk.DISABLED
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, summary_text)
        text_widget.config(state=tk.DISABLED)
        
        # 保存配置
        self.save_final_config()
    
    def generate_summary(self) -> str:
        """生成配置摘要"""
        summary = "配置摘要:\n\n"
        
        # 位置信息
        location = self.config_data.get('location', {})
        if location:
            summary += f"📍 位置: {location.get('lat', 'N/A'):.6f}, {location.get('lng', 'N/A'):.6f}\n"
            summary += f"   来源: {location.get('source', '未知')}\n\n"
        
        # Cookie信息
        cookies = self.config_data.get('cookies', [])
        summary += f"🍪 Cookie: {len(cookies)} 个\n\n"
        
        # 班级信息
        class_id = self.config_data.get('class_id')
        if class_id:
            summary += f"🏫 班级ID: {class_id}\n\n"
        
        # 定时信息
        mode = getattr(self, 'schedule_mode', tk.StringVar()).get()
        if mode == "scheduled":
            hour = getattr(self, 'hour_var', tk.StringVar()).get()
            minute = getattr(self, 'minute_var', tk.StringVar()).get()
            summary += f"⏰ 定时签到: 每天 {hour}:{minute}\n\n"
        else:
            summary += "⏰ 签到模式: 手动执行\n\n"
        
        # 推送信息
        push_token = getattr(self, 'push_token_var', tk.StringVar()).get()
        if push_token:
            summary += "📱 推送通知: 已配置\n\n"
        
        summary += "✅ 配置已保存，可以开始使用了！"
        
        return summary
    
    def save_final_config(self):
        """保存最终配置"""
        try:
            # 收集所有配置
            final_config = {
                'class': self.config_data.get('class_id', ''),
                'lat': str(self.config_data.get('location', {}).get('lat', '')),
                'lng': str(self.config_data.get('location', {}).get('lng', '')),
                'acc': str(self.config_data.get('location', {}).get('alt', '100')),
                'cookie': self.config_data.get('cookies', []),
                'scheduletime': '',
                'pushplus': getattr(self, 'push_token_var', tk.StringVar()).get(),
                'debug': False,
                'configLock': True
            }
            
            # 处理定时设置
            mode = getattr(self, 'schedule_mode', tk.StringVar()).get()
            if mode == "scheduled":
                hour = getattr(self, 'hour_var', tk.StringVar()).get()
                minute = getattr(self, 'minute_var', tk.StringVar()).get()
                final_config['scheduletime'] = f"{hour}:{minute}"
            
            # 保存到安全存储
            cookie_manager = CookieManager()
            cookie_manager.save_cookies(
                final_config['cookie'],
                {
                    'class_id': final_config['class'],
                    'location': self.config_data.get('location', {}),
                    'schedule': final_config['scheduletime'],
                    'push_token': final_config['pushplus']
                }
            )
            
            # 保存到传统配置文件（兼容性）
            import os
            config_path = os.path.join(os.getcwd(), "config.json")
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(final_config, f, indent=4, ensure_ascii=False)
            
            self.config_data['final_config'] = final_config
            
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")
    
    def next_step(self):
        """下一步"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()
        else:
            # 完成配置
            self.complete_wizard()
    
    def prev_step(self):
        """上一步"""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()
    
    def goto_step(self, step_index: int):
        """跳转到指定步骤"""
        if 0 <= step_index < len(self.steps):
            self.current_step = step_index
            self.show_current_step()
    
    def cancel(self):
        """取消配置"""
        if messagebox.askyesno("确认", "确定要取消配置吗？"):
            self.root.destroy()
    
    def complete_wizard(self):
        """完成向导"""
        if self.on_complete:
            self.on_complete(self.config_data.get('final_config'))
        self.root.destroy()
    
    def run(self):
        """运行向导"""
        self.root.mainloop()


def test_config_wizard():
    """测试配置向导"""
    def on_complete(config):
        print("配置完成:")
        print(json.dumps(config, indent=2, ensure_ascii=False))
    
    wizard = ConfigWizard(on_complete)
    wizard.run()


if __name__ == "__main__":
    test_config_wizard()
