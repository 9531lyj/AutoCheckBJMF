"""
班级ID自动检测模块
通过多种方式自动获取班级ID，减少用户手动输入
"""
import requests
import re
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class ClassDetector:
    """班级ID检测器 - 自动检测和获取班级ID"""
    
    def __init__(self):
        self.base_url = "http://k8n.cn"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def extract_classes_from_cookie(self, cookie: str) -> List[Dict]:
        """从Cookie中提取用户的班级信息"""
        try:
            # 提取remember_student_xxx Cookie
            pattern = r'remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=([^;]+)'
            match = re.search(pattern, cookie)
            
            if not match:
                return []
            
            # 设置Cookie并访问学生主页
            self.session.cookies.clear()
            self.session.cookies.set(
                'remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d',
                match.group(1)
            )
            
            # 访问学生课程页面
            response = self.session.get(f"{self.base_url}/student")
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            classes = []
            
            # 查找课程链接
            course_links = soup.find_all('a', href=re.compile(r'/student/course/\d+'))
            
            for link in course_links:
                href = link.get('href')
                class_id_match = re.search(r'/student/course/(\d+)', href)
                
                if class_id_match:
                    class_id = class_id_match.group(1)
                    class_name = link.get_text(strip=True)
                    
                    # 获取更多课程信息
                    class_info = self._get_class_details(class_id)
                    
                    classes.append({
                        'id': class_id,
                        'name': class_name,
                        'url': href,
                        'details': class_info
                    })
            
            return classes
            
        except Exception as e:
            print(f"从Cookie提取班级信息失败: {e}")
            return []
    
    def _get_class_details(self, class_id: str) -> Dict:
        """获取班级详细信息"""
        try:
            response = self.session.get(f"{self.base_url}/student/course/{class_id}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取班级详细信息
                details = {
                    'teacher': '',
                    'students_count': 0,
                    'has_checkin': False
                }
                
                # 查找教师信息
                teacher_elem = soup.find('span', text=re.compile(r'教师|老师'))
                if teacher_elem:
                    details['teacher'] = teacher_elem.find_next().get_text(strip=True)
                
                # 查找学生数量
                students_elem = soup.find('span', text=re.compile(r'学生|人数'))
                if students_elem:
                    students_text = students_elem.find_next().get_text(strip=True)
                    students_match = re.search(r'(\d+)', students_text)
                    if students_match:
                        details['students_count'] = int(students_match.group(1))
                
                # 检查是否有签到功能
                checkin_elem = soup.find('a', href=re.compile(r'/punchs'))
                details['has_checkin'] = checkin_elem is not None
                
                return details
                
        except Exception as e:
            print(f"获取班级详情失败: {e}")
        
        return {}
    
    def search_classes_by_keyword(self, keyword: str, cookie: str) -> List[Dict]:
        """通过关键词搜索班级"""
        try:
            # 设置Cookie
            pattern = r'remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=([^;]+)'
            match = re.search(pattern, cookie)
            
            if not match:
                return []
            
            self.session.cookies.clear()
            self.session.cookies.set(
                'remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d',
                match.group(1)
            )
            
            # 搜索课程
            search_url = f"{self.base_url}/student/search"
            response = self.session.post(search_url, data={'keyword': keyword})
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                classes = []
                
                # 解析搜索结果
                course_items = soup.find_all('div', class_='course-item')
                for item in course_items:
                    link = item.find('a', href=re.compile(r'/student/course/\d+'))
                    if link:
                        href = link.get('href')
                        class_id_match = re.search(r'/student/course/(\d+)', href)
                        
                        if class_id_match:
                            class_id = class_id_match.group(1)
                            class_name = link.get_text(strip=True)
                            
                            classes.append({
                                'id': class_id,
                                'name': class_name,
                                'url': href,
                                'source': '搜索结果'
                            })
                
                return classes
                
        except Exception as e:
            print(f"搜索班级失败: {e}")
        
        return []
    
    def show_class_selector(self, classes: List[Dict]) -> Optional[str]:
        """显示班级选择器GUI"""
        if not classes:
            return None
        
        try:
            root = tk.Tk()
            root.title("选择班级")
            root.geometry("600x400")
            
            # 创建表格
            frame = ttk.Frame(root)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 表格标题
            ttk.Label(frame, text="请选择要签到的班级：", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
            
            # 创建Treeview
            columns = ('ID', '班级名称', '教师', '学生数', '签到功能')
            tree = ttk.Treeview(frame, columns=columns, show='headings', height=10)
            
            # 设置列标题
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            
            # 添加数据
            for cls in classes:
                details = cls.get('details', {})
                tree.insert('', tk.END, values=(
                    cls['id'],
                    cls['name'][:30] + '...' if len(cls['name']) > 30 else cls['name'],
                    details.get('teacher', '未知'),
                    details.get('students_count', 0),
                    '是' if details.get('has_checkin', False) else '否'
                ))
            
            tree.pack(fill=tk.BOTH, expand=True)
            
            # 按钮框架
            button_frame = ttk.Frame(frame)
            button_frame.pack(fill=tk.X, pady=(10, 0))
            
            selected_class_id = None
            
            def on_select():
                nonlocal selected_class_id
                selection = tree.selection()
                if selection:
                    item = tree.item(selection[0])
                    selected_class_id = item['values'][0]
                    root.quit()
                else:
                    messagebox.showwarning("警告", "请选择一个班级")
            
            def on_cancel():
                nonlocal selected_class_id
                selected_class_id = None
                root.quit()
            
            ttk.Button(button_frame, text="确定", command=on_select).pack(side=tk.RIGHT, padx=(5, 0))
            ttk.Button(button_frame, text="取消", command=on_cancel).pack(side=tk.RIGHT)
            
            # 双击选择
            def on_double_click(event):
                on_select()
            
            tree.bind('<Double-1>', on_double_click)
            
            root.mainloop()
            root.destroy()
            
            return selected_class_id
            
        except Exception as e:
            print(f"显示班级选择器失败: {e}")
            return None
    
    def get_class_id_interactive(self, cookie: str) -> Optional[str]:
        """交互式获取班级ID"""
        print("🔍 正在检测班级信息...")
        
        # 1. 从Cookie中提取班级列表
        classes = self.extract_classes_from_cookie(cookie)
        
        if classes:
            print(f"✅ 检测到 {len(classes)} 个班级")
            
            # 过滤有签到功能的班级
            checkin_classes = [cls for cls in classes if cls.get('details', {}).get('has_checkin', False)]
            
            if checkin_classes:
                print(f"📝 其中 {len(checkin_classes)} 个班级支持签到功能")
                
                if len(checkin_classes) == 1:
                    # 只有一个班级，直接使用
                    class_info = checkin_classes[0]
                    print(f"🎯 自动选择班级: {class_info['name']} (ID: {class_info['id']})")
                    return class_info['id']
                else:
                    # 多个班级，让用户选择
                    return self.show_class_selector(checkin_classes)
            else:
                print("⚠️ 未找到支持签到的班级")
                return self.show_class_selector(classes)
        
        # 2. 如果没有找到班级，提供手动输入选项
        try:
            root = tk.Tk()
            root.withdraw()
            
            choice = messagebox.askyesnocancel(
                "班级检测",
                "未能自动检测到班级信息。\n\n"
                "是 - 手动输入班级ID\n"
                "否 - 通过关键词搜索\n"
                "取消 - 跳过"
            )
            
            if choice is True:
                # 手动输入
                class_id = simpledialog.askstring("班级ID", "请输入班级ID:")
                return class_id
            elif choice is False:
                # 关键词搜索
                keyword = simpledialog.askstring("搜索班级", "请输入班级名称关键词:")
                if keyword:
                    search_results = self.search_classes_by_keyword(keyword, cookie)
                    if search_results:
                        return self.show_class_selector(search_results)
            
            root.destroy()
            
        except Exception as e:
            print(f"交互式获取班级ID失败: {e}")
        
        return None


def test_class_detector():
    """测试班级检测器"""
    detector = ClassDetector()
    
    # 这里需要一个有效的Cookie进行测试
    test_cookie = "remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=test_value"
    
    class_id = detector.get_class_id_interactive(test_cookie)
    print(f"检测到的班级ID: {class_id}")


if __name__ == "__main__":
    test_class_detector()
