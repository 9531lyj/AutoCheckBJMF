# 📦 AutoCheckBJMF 增强版安装指南

本指南将详细介绍如何在不同操作系统上安装和配置 AutoCheckBJMF 增强版。

## 📋 系统要求

### 最低要求
- **Python**: 3.7 或更高版本
- **内存**: 512MB RAM
- **存储**: 100MB 可用空间
- **网络**: 稳定的互联网连接

### 推荐配置
- **Python**: 3.9+ 
- **内存**: 1GB+ RAM
- **存储**: 500MB+ 可用空间
- **浏览器**: Chrome/Edge/Firefox 最新版本

## 🖥️ Windows 安装指南

### 方法一：一键安装脚本（推荐）

1. **下载项目**
   ```cmd
   # 使用 Git（推荐）
   git clone https://github.com/JasonYANG170/AutoCheckBJMF.git
   cd AutoCheckBJMF
   
   # 或直接下载 ZIP 文件并解压
   ```

2. **运行安装脚本**
   ```cmd
   # 右键以管理员身份运行 PowerShell
   python setup.py
   ```

3. **启动程序**
   ```cmd
   # 方式1：双击批处理文件
   启动AutoCheckBJMF.bat
   
   # 方式2：命令行启动
   python main_enhanced.py
   
   # 方式3：双击桌面快捷方式
   ```

### 方法二：手动安装

1. **安装 Python**
   - 访问 [Python官网](https://www.python.org/downloads/)
   - 下载 Python 3.7+ 版本
   - 安装时勾选 "Add Python to PATH"

2. **验证安装**
   ```cmd
   python --version
   pip --version
   ```

3. **安装依赖**
   ```cmd
   pip install -r requirements.txt
   ```

4. **安装浏览器驱动（可选）**
   ```cmd
   pip install webdriver-manager
   ```

### Windows 特殊配置

#### 启用长路径支持
```cmd
# 以管理员身份运行
reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1
```

#### 防火墙配置
- 允许 Python 通过 Windows 防火墙
- 添加例外：`python.exe` 和 `pythonw.exe`

## 🍎 macOS 安装指南

### 方法一：使用 Homebrew（推荐）

1. **安装 Homebrew**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **安装 Python**
   ```bash
   brew install python@3.9
   ```

3. **下载项目**
   ```bash
   git clone https://github.com/JasonYANG170/AutoCheckBJMF.git
   cd AutoCheckBJMF
   ```

4. **运行安装脚本**
   ```bash
   python3 setup.py
   ```

5. **启动程序**
   ```bash
   # 方式1：使用脚本
   ./start_autocheckbjmf.sh
   
   # 方式2：直接运行
   python3 main_enhanced.py
   ```

### 方法二：手动安装

1. **安装 Python**
   - 访问 [Python官网](https://www.python.org/downloads/macos/)
   - 下载 macOS 版本并安装

2. **安装依赖**
   ```bash
   pip3 install -r requirements.txt
   ```

### macOS 特殊配置

#### 权限设置
```bash
# 给脚本执行权限
chmod +x start_autocheckbjmf.sh
chmod +x config_autocheckbjmf.sh

# 允许访问位置服务（系统偏好设置 > 安全性与隐私 > 位置服务）
```

#### 安装 Xcode 命令行工具
```bash
xcode-select --install
```

## 🐧 Linux 安装指南

### Ubuntu/Debian 系统

1. **更新系统**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **安装 Python 和依赖**
   ```bash
   sudo apt install python3 python3-pip python3-venv git -y
   ```

3. **下载项目**
   ```bash
   git clone https://github.com/JasonYANG170/AutoCheckBJMF.git
   cd AutoCheckBJMF
   ```

4. **创建虚拟环境（推荐）**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

6. **运行程序**
   ```bash
   python3 main_enhanced.py
   ```

### CentOS/RHEL 系统

1. **安装 EPEL 仓库**
   ```bash
   sudo yum install epel-release -y
   ```

2. **安装 Python**
   ```bash
   sudo yum install python3 python3-pip git -y
   ```

3. **后续步骤同 Ubuntu**

### Arch Linux 系统

1. **安装依赖**
   ```bash
   sudo pacman -S python python-pip git
   ```

2. **后续步骤同 Ubuntu**

## 🔧 依赖包详解

### 核心依赖
```txt
requests>=2.28.0          # HTTP 请求库
beautifulsoup4>=4.11.0    # HTML 解析库
schedule>=1.2.0           # 定时任务库
cryptography>=3.4.8      # 加密库
```

### 可选依赖
```txt
selenium>=4.0.0           # 自动化浏览器
webdriver-manager>=3.8.0  # 浏览器驱动管理
keyring>=23.0.0          # 系统密钥环
```

### 平台特定依赖
```txt
# Windows
pywin32>=304             # Windows API
winrt>=1.0.0            # Windows Runtime

# macOS
pyobjc-framework-CoreLocation  # 位置服务

# Linux
python3-dbus            # D-Bus 接口
```

## 🚀 验证安装

### 基本功能测试
```bash
# 测试 Python 环境
python --version

# 测试依赖包
python -c "import requests, bs4, schedule, cryptography; print('✅ 基础依赖正常')"

# 测试程序启动
python main_enhanced.py --test
```

### 高级功能测试
```bash
# 测试浏览器驱动
python -c "from modules.auto_login import AutoLogin; print('✅ 浏览器功能正常')"

# 测试安全存储
python -c "from modules.secure_storage import SecureStorage; print('✅ 安全存储正常')"

# 测试位置服务
python -c "from modules.location_manager import LocationManager; print('✅ 位置服务正常')"
```

## 🔍 常见安装问题

### Python 相关

**问题**: `python: command not found`
```bash
# 解决方案
# Windows: 重新安装 Python 并勾选 "Add to PATH"
# macOS: 使用 python3 命令
# Linux: sudo apt install python3
```

**问题**: `pip: command not found`
```bash
# 解决方案
python -m ensurepip --upgrade
# 或
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### 依赖安装问题

**问题**: `Microsoft Visual C++ 14.0 is required`
```bash
# Windows 解决方案
# 1. 安装 Visual Studio Build Tools
# 2. 或安装 Microsoft C++ Build Tools
# 3. 或使用预编译包：pip install --only-binary=all cryptography
```

**问题**: `Failed building wheel for cryptography`
```bash
# Linux 解决方案
sudo apt install build-essential libssl-dev libffi-dev python3-dev
# macOS 解决方案
xcode-select --install
```

### 权限问题

**问题**: `Permission denied`
```bash
# 解决方案
# 1. 使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 2. 或使用用户安装
pip install --user -r requirements.txt
```

## 🎯 安装后配置

### 首次运行检查清单

- [ ] Python 版本 3.7+
- [ ] 所有依赖包已安装
- [ ] 网络连接正常
- [ ] 浏览器已安装并能正常访问班级魔方网站
- [ ] 已在浏览器中登录过班级魔方（用于Cookie提取）

### 推荐配置

1. **创建桌面快捷方式**（Windows）
2. **添加到系统 PATH**（便于命令行调用）
3. **配置开机自启**（用于定时签到）
4. **设置防火墙例外**（避免网络问题）

## 📞 获取帮助

如果在安装过程中遇到问题：

1. **查看日志文件**: `AutoCheckBJMF_enhanced.log`
2. **运行诊断脚本**: `python setup.py --diagnose`
3. **提交 Issue**: [GitHub Issues](https://github.com/JasonYANG170/AutoCheckBJMF/issues)
4. **查看文档**: [在线文档](https://9531lyj.github.io/AutoCheckBJMF/)

---

**下一步**: [使用教程](user-guide.md) | [配置指南](configuration-guide.md) | [故障排除](troubleshooting.md)
