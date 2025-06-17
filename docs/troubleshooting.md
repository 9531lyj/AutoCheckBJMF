# 🔧 AutoCheckBJMF 增强版故障排除指南

本指南帮助您诊断和解决使用过程中可能遇到的各种问题。

## 🚨 常见问题快速诊断

### 快速检查清单

在深入排查问题之前，请先检查以下基本项目：

- [ ] Python 版本是否为 3.7+
- [ ] 所有依赖包是否正确安装
- [ ] 网络连接是否正常
- [ ] 是否已在浏览器中登录班级魔方网站
- [ ] 系统时间是否正确
- [ ] 防火墙是否阻止了程序运行

### 一键诊断工具

```bash
# 运行内置诊断工具
python main_enhanced.py --diagnose

# 或者运行独立诊断脚本
python setup.py --diagnose
```

## 🔍 问题分类排查

### 1. 程序启动问题

#### 问题：`python: command not found`

**症状**：
```bash
$ python main_enhanced.py
bash: python: command not found
```

**解决方案**：
```bash
# 检查 Python 安装
which python3
python3 --version

# 如果 python3 可用，使用 python3
python3 main_enhanced.py

# 或创建别名
alias python=python3
```

**Windows 特殊情况**：
```cmd
# 检查 Python 是否在 PATH 中
where python

# 如果没有，重新安装 Python 并勾选 "Add Python to PATH"
# 或手动添加到环境变量
```

#### 问题：`ModuleNotFoundError`

**症状**：
```python
ModuleNotFoundError: No module named 'requests'
```

**解决方案**：
```bash
# 重新安装依赖
pip install -r requirements.txt

# 如果使用虚拟环境
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# 检查安装状态
pip list | grep requests
```

#### 问题：程序启动后立即退出

**诊断步骤**：
```bash
# 1. 查看错误日志
cat AutoCheckBJMF_enhanced.log

# 2. 启用调试模式
python main_enhanced.py --debug

# 3. 检查配置文件
python -c "import json; print(json.load(open('config.json')))" 2>/dev/null || echo "配置文件不存在或损坏"
```

### 2. Cookie 相关问题

#### 问题：Cookie 提取失败

**症状**：
```
❌ 从 chrome 未找到目标Cookie
❌ 从 edge 未找到目标Cookie
❌ 未找到任何Cookie
```

**解决方案**：

1. **确认浏览器登录状态**：
   ```bash
   # 打开浏览器访问
   https://k8n.cn/student/login
   
   # 确保已成功登录并能看到课程列表
   ```

2. **检查浏览器数据库权限**：
   ```bash
   # Windows - 关闭所有浏览器实例
   taskkill /f /im chrome.exe
   taskkill /f /im msedge.exe
   
   # 然后重新运行程序
   ```

3. **手动提取Cookie**：
   ```bash
   # 按 F12 打开开发者工具
   # Network 标签页 -> 刷新页面 -> 找到请求
   # 复制 Cookie 值
   ```

#### 问题：Cookie 过期

**症状**：
```
❌ 登录状态异常，将本Cookie加入重试队列
❌ Cookie验证失败
```

**解决方案**：
```bash
# 1. 清除过期Cookie
python -c "from modules.secure_storage import CookieManager; CookieManager().clear_all_data()"

# 2. 重新获取Cookie
python main_enhanced.py

# 3. 选择"快速自动配置"重新提取
```

#### 问题：多用户Cookie冲突

**症状**：
```
!!! 本次签到存在异常，请检查Cookie是否均已正常配置 !!!
```

**解决方案**：
```bash
# 1. 检查Cookie格式
python -c "
import json
config = json.load(open('config.json'))
for i, cookie in enumerate(config['cookie']):
    print(f'Cookie {i+1}: {cookie[:50]}...')
    if 'remember_student_' not in cookie:
        print(f'  ❌ Cookie {i+1} 格式错误')
    else:
        print(f'  ✅ Cookie {i+1} 格式正确')
"

# 2. 重新配置问题Cookie
```

### 3. 定位相关问题

#### 问题：GPS定位失败

**症状**：
```
❌ 定位失败: 网络连接超时
❌ 系统GPS定位失败
```

**解决方案**：

1. **检查网络连接**：
   ```bash
   # 测试网络连接
   ping ip-api.com
   ping ipinfo.io
   
   # 测试目标网站
   ping k8n.cn
   ```

2. **使用备用定位方式**：
   ```bash
   # 手动输入坐标
   # 访问 https://lbs.qq.com/getPoint/
   # 选择位置并复制坐标
   ```

3. **检查系统权限**：
   ```bash
   # Windows: 设置 -> 隐私 -> 位置 -> 允许应用访问位置
   # macOS: 系统偏好设置 -> 安全性与隐私 -> 位置服务
   # Linux: 检查 geoclue 服务状态
   systemctl status geoclue
   ```

#### 问题：坐标精度不够

**症状**：
```
⚠️ 位置精度可能不够，建议手动调整
```

**解决方案**：
```bash
# 1. 使用腾讯地图坐标拾取器
# https://lbs.qq.com/getPoint/

# 2. 确保坐标精度至少8位小数
# 正确格式：39.90469700, 116.40717800
# 错误格式：39.9, 116.4

# 3. 在配置向导中选择"手动调整位置"
```

### 4. 签到功能问题

#### 问题：未找到签到任务

**症状**：
```
ℹ️ 未找到进行中的签到任务
```

**可能原因**：
1. 当前时间没有签到任务
2. 班级ID错误
3. Cookie已过期
4. 网络连接问题

**解决方案**：
```bash
# 1. 确认签到时间
# 联系老师确认签到任务发布时间

# 2. 验证班级ID
python -c "
import requests
class_id = input('请输入班级ID: ')
url = f'http://k8n.cn/student/course/{class_id}'
response = requests.get(url)
print(f'状态码: {response.status_code}')
print(f'URL: {response.url}')
"

# 3. 手动测试签到页面
# 浏览器访问: http://k8n.cn/student/course/你的班级ID/punchs
```

#### 问题：签到请求失败

**症状**：
```
❌ 请求失败，状态码: 403
❌ 签到请求失败，状态码: 500
```

**解决方案**：

1. **检查请求频率**：
   ```bash
   # 程序内置了请求间隔，但如果手动频繁测试可能被限制
   # 等待 5-10 分钟后重试
   ```

2. **检查User-Agent**：
   ```python
   # 程序使用的User-Agent
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
   
   # 如果被检测，可以更新为最新版本
   ```

3. **检查网络环境**：
   ```bash
   # 如果在校园网环境，可能有特殊限制
   # 尝试使用手机热点或其他网络
   ```

### 5. 定时任务问题

#### 问题：定时任务不执行

**症状**：
```
⏰ 定时签到模式，设定时间: 08:30
# 但到了时间没有执行
```

**解决方案**：

1. **检查系统时间**：
   ```bash
   # 确保系统时间正确
   date  # Linux/macOS
   time  # Windows
   
   # 如果时间不对，同步时间
   sudo ntpdate -s time.nist.gov  # Linux
   w32tm /resync  # Windows
   ```

2. **检查程序运行状态**：
   ```bash
   # 确保程序持续运行
   ps aux | grep python  # Linux/macOS
   tasklist | findstr python  # Windows
   ```

3. **检查时间格式**：
   ```json
   {
     "scheduletime": "08:30"  // 正确格式
     // "scheduletime": "8:30"   // 错误格式，需要补零
   }
   ```

#### 问题：定时任务执行多次

**症状**：
```
# 同一时间执行了多次签到
```

**解决方案**：
```bash
# 1. 确保只运行一个程序实例
pkill -f main_enhanced.py  # 杀死所有实例
python main_enhanced.py    # 重新启动

# 2. 检查是否有多个定时任务
crontab -l  # Linux/macOS
# Windows: 任务计划程序
```

### 6. 安全存储问题

#### 问题：加密存储失败

**症状**：
```
❌ 保存数据失败: [Errno 13] Permission denied
❌ 加载数据失败: Invalid token
```

**解决方案**：

1. **检查文件权限**：
   ```bash
   # Linux/macOS
   ls -la ~/.config/AutoCheckBJMF/
   chmod 600 ~/.config/AutoCheckBJMF/*
   
   # Windows
   # 右键文件 -> 属性 -> 安全 -> 编辑权限
   ```

2. **重置安全存储**：
   ```bash
   # 清除损坏的存储文件
   python -c "
   from modules.secure_storage import SecureStorage
   storage = SecureStorage()
   storage.clear_data()
   print('安全存储已重置')
   "
   ```

3. **检查磁盘空间**：
   ```bash
   df -h  # Linux/macOS
   dir   # Windows
   ```

## 🔧 高级诊断工具

### 网络连接测试

```bash
# 创建网络测试脚本
cat > network_test.py << 'EOF'
import requests
import time

def test_connection():
    urls = [
        'http://k8n.cn',
        'http://k8n.cn/student/login',
        'http://ip-api.com/json/',
        'https://ipinfo.io/json'
    ]
    
    for url in urls:
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            end_time = time.time()
            
            print(f"✅ {url}")
            print(f"   状态码: {response.status_code}")
            print(f"   响应时间: {end_time - start_time:.2f}s")
        except Exception as e:
            print(f"❌ {url}")
            print(f"   错误: {e}")
        print()

if __name__ == "__main__":
    test_connection()
EOF

python network_test.py
```

### 配置文件验证

```bash
# 创建配置验证脚本
cat > config_validator.py << 'EOF'
import json
import re

def validate_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("📋 配置文件验证结果:")
        print("=" * 40)
        
        # 检查必需字段
        required_fields = ['class', 'lat', 'lng', 'acc', 'cookie']
        for field in required_fields:
            if field in config and config[field]:
                print(f"✅ {field}: 已配置")
            else:
                print(f"❌ {field}: 缺失或为空")
        
        # 检查坐标格式
        try:
            lat = float(config.get('lat', 0))
            lng = float(config.get('lng', 0))
            if -90 <= lat <= 90 and -180 <= lng <= 180:
                print(f"✅ 坐标格式: 正确 ({lat}, {lng})")
            else:
                print(f"❌ 坐标格式: 超出范围")
        except:
            print(f"❌ 坐标格式: 无效")
        
        # 检查Cookie格式
        cookies = config.get('cookie', [])
        if isinstance(cookies, list):
            valid_cookies = 0
            for i, cookie in enumerate(cookies):
                if 'remember_student_' in cookie:
                    valid_cookies += 1
                    print(f"✅ Cookie {i+1}: 格式正确")
                else:
                    print(f"❌ Cookie {i+1}: 格式错误")
            print(f"📊 有效Cookie: {valid_cookies}/{len(cookies)}")
        else:
            print(f"❌ Cookie格式: 应为列表")
        
        # 检查定时格式
        schedule_time = config.get('scheduletime', '')
        if schedule_time:
            if re.match(r'^\d{2}:\d{2}$', schedule_time):
                print(f"✅ 定时格式: 正确 ({schedule_time})")
            else:
                print(f"❌ 定时格式: 错误，应为 HH:MM")
        else:
            print(f"ℹ️ 定时设置: 未配置（手动模式）")
        
    except FileNotFoundError:
        print("❌ 配置文件不存在")
    except json.JSONDecodeError:
        print("❌ 配置文件格式错误")
    except Exception as e:
        print(f"❌ 验证失败: {e}")

if __name__ == "__main__":
    validate_config()
EOF

python config_validator.py
```

### 系统环境检查

```bash
# 创建环境检查脚本
cat > env_check.py << 'EOF'
import sys
import platform
import subprocess
import importlib

def check_environment():
    print("🖥️ 系统环境检查")
    print("=" * 40)
    
    # Python版本
    print(f"Python版本: {sys.version}")
    if sys.version_info >= (3, 7):
        print("✅ Python版本符合要求")
    else:
        print("❌ Python版本过低，需要3.7+")
    
    # 操作系统
    print(f"操作系统: {platform.system()} {platform.release()}")
    
    # 依赖包检查
    required_packages = [
        'requests', 'beautifulsoup4', 'schedule', 
        'cryptography', 'selenium', 'keyring'
    ]
    
    print("\n📦 依赖包检查:")
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (未安装)")
    
    # 浏览器检查
    print("\n🌐 浏览器检查:")
    browsers = {
        'chrome': ['google-chrome', 'chrome', 'chromium'],
        'firefox': ['firefox'],
        'edge': ['msedge', 'microsoft-edge']
    }
    
    for browser, commands in browsers.items():
        found = False
        for cmd in commands:
            try:
                subprocess.run([cmd, '--version'], 
                             capture_output=True, check=True)
                print(f"✅ {browser}")
                found = True
                break
            except:
                continue
        if not found:
            print(f"❌ {browser} (未找到)")

if __name__ == "__main__":
    check_environment()
EOF

python env_check.py
```

## 📞 获取帮助

### 自助排查步骤

1. **查看日志文件**：
   ```bash
   tail -f AutoCheckBJMF_enhanced.log
   ```

2. **运行诊断工具**：
   ```bash
   python main_enhanced.py --diagnose
   ```

3. **重置配置**：
   ```bash
   rm config.json
   python -c "from modules.secure_storage import CookieManager; CookieManager().clear_all_data()"
   ```

4. **重新安装**：
   ```bash
   pip uninstall -y -r requirements.txt
   pip install -r requirements.txt
   ```

### 寻求帮助

如果问题仍未解决，请：

1. **收集信息**：
   - 操作系统版本
   - Python版本
   - 错误日志
   - 复现步骤

2. **提交Issue**：
   - 访问 [GitHub Issues](https://github.com/JasonYANG170/AutoCheckBJMF/issues)
   - 使用问题模板
   - 提供详细信息

3. **参与讨论**：
   - 访问 [GitHub Discussions](https://github.com/JasonYANG170/AutoCheckBJMF/discussions)
   - 搜索相似问题
   - 参与社区讨论

---

**相关文档**: [安装指南](installation-guide.md) | [用户指南](user-guide.md) | [配置指南](configuration-guide.md)
