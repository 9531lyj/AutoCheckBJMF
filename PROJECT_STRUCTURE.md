# 📁 AutoCheckBJMF 增强版项目结构

本文档详细说明了项目的文件结构和各个组件的作用。

## 🏗️ 项目架构

```
AutoCheckBJMF/
├── 📁 .github/                    # GitHub 配置
│   └── 📁 workflows/              # GitHub Actions 工作流
│       ├── ci.yml                 # CI/CD 流水线
│       └── pages.yml              # GitHub Pages 部署
├── 📁 docs/                       # 文档和网站
│   ├── _config.yml                # Jekyll 配置
│   ├── Gemfile                    # Ruby 依赖
│   ├── index.md                   # 主页
│   ├── installation-guide.md     # 安装指南
│   ├── user-guide.md             # 使用教程
│   └── troubleshooting.md        # 故障排除
├── 📁 modules/                    # 核心功能模块
│   ├── auto_login.py              # 自动登录模块
│   ├── browser_cookie_extractor.py # 浏览器Cookie提取
│   ├── class_detector.py         # 班级检测模块
│   ├── gui_config.py             # 图形配置界面
│   ├── location_manager.py       # 位置管理模块
│   └── secure_storage.py         # 安全存储模块
├── 📁 tests/                      # 测试文件
│   ├── test_main_enhanced.py     # 主程序测试
│   └── test_modules.py           # 模块测试
├── 📄 main_enhanced.py            # 增强版主程序
├── 📄 main.py                     # 原版主程序（兼容性）
├── 📄 setup.py                    # 自动安装脚本
├── 📄 run_tests.py               # 测试运行器
├── 📄 verify_functionality.py    # 功能验证脚本
├── 📄 demo.py                     # 功能演示脚本
├── 📄 requirements.txt           # Python 依赖
├── 📄 .gitignore                 # Git 忽略文件
├── 📄 README.md                  # 项目说明
└── 📄 PROJECT_STRUCTURE.md       # 本文件
```

## 🔧 核心模块说明

### 主程序文件

| 文件 | 描述 | 用途 |
|------|------|------|
| `main_enhanced.py` | 增强版主程序 | 集成所有新功能的主入口 |
| `main.py` | 原版主程序 | 保持与原项目的兼容性 |

### 功能模块 (`modules/`)

| 模块 | 功能 | 主要类/函数 |
|------|------|-------------|
| `secure_storage.py` | 安全存储 | `SecureStorage`, `CookieManager` |
| `location_manager.py` | 位置管理 | `LocationManager` |
| `browser_cookie_extractor.py` | Cookie提取 | `BrowserCookieExtractor` |
| `auto_login.py` | 自动登录 | `AutoLogin` |
| `class_detector.py` | 班级检测 | `ClassDetector` |
| `gui_config.py` | 图形界面 | `ConfigWizard` |

### 工具脚本

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `setup.py` | 自动安装 | 首次安装和环境配置 |
| `run_tests.py` | 测试运行 | 开发和CI/CD |
| `verify_functionality.py` | 功能验证 | 部署后验证 |
| `demo.py` | 功能演示 | 展示和教学 |

## 📚 文档结构 (`docs/`)

### 用户文档

| 文档 | 内容 | 目标用户 |
|------|------|----------|
| `index.md` | 项目主页 | 所有用户 |
| `installation-guide.md` | 安装指南 | 新用户 |
| `user-guide.md` | 使用教程 | 普通用户 |
| `troubleshooting.md` | 故障排除 | 遇到问题的用户 |

### 网站配置

| 文件 | 用途 |
|------|------|
| `_config.yml` | Jekyll 网站配置 |
| `Gemfile` | Ruby 依赖管理 |

## 🧪 测试结构 (`tests/`)

### 测试文件

| 测试文件 | 测试内容 | 覆盖范围 |
|----------|----------|----------|
| `test_main_enhanced.py` | 主程序测试 | 配置验证、签到逻辑 |
| `test_modules.py` | 模块测试 | 各功能模块单元测试 |

### 测试工具

| 工具 | 功能 |
|------|------|
| `run_tests.py` | 统一测试入口，支持多种运行模式 |
| `verify_functionality.py` | 端到端功能验证 |

## 🔄 CI/CD 流程 (`.github/workflows/`)

### 工作流文件

| 工作流 | 触发条件 | 功能 |
|--------|----------|------|
| `ci.yml` | Push/PR | 完整的CI/CD流水线 |
| `pages.yml` | Push to main | GitHub Pages部署 |

### CI/CD 阶段

1. **测试阶段**
   - 多平台测试 (Windows/macOS/Linux)
   - 多Python版本测试 (3.7-3.11)
   - 代码质量检查 (flake8)
   - 安全扫描 (bandit, safety)

2. **构建阶段**
   - 文档构建 (Jekyll)
   - 可执行文件打包 (PyInstaller)

3. **部署阶段**
   - GitHub Pages 部署
   - Release 创建
   - 构件上传

## 📦 依赖管理

### Python 依赖 (`requirements.txt`)

| 类别 | 包名 | 用途 |
|------|------|------|
| 核心依赖 | `requests`, `beautifulsoup4`, `schedule` | 基础功能 |
| 安全依赖 | `cryptography`, `keyring` | 数据加密 |
| 自动化依赖 | `selenium`, `webdriver-manager` | 浏览器自动化 |
| 平台依赖 | `pywin32`, `winrt` | Windows特定功能 |

### Ruby 依赖 (`docs/Gemfile`)

| 包名 | 用途 |
|------|------|
| `github-pages` | GitHub Pages 兼容 |
| `jekyll-*` | Jekyll 插件 |

## 🔒 安全考虑

### 敏感文件保护

通过 `.gitignore` 保护的文件类型：
- 配置文件 (`config.json`)
- 日志文件 (`*.log`)
- 加密存储文件 (`*.enc`, `*.key`)
- 临时文件和缓存

### 数据加密

- 使用 `cryptography` 库进行数据加密
- 跨平台密钥管理
- 安全的临时文件处理

## 🚀 部署流程

### 开发环境

1. 克隆仓库
2. 运行 `python setup.py`
3. 执行 `python main_enhanced.py`

### 生产环境

1. GitHub Actions 自动构建
2. 自动测试验证
3. GitHub Pages 自动部署
4. Release 自动创建

## 📈 扩展指南

### 添加新功能模块

1. 在 `modules/` 目录创建新模块
2. 在 `tests/` 目录添加对应测试
3. 更新 `requirements.txt` 如需新依赖
4. 更新文档

### 添加新文档

1. 在 `docs/` 目录创建 Markdown 文件
2. 更新 `_config.yml` 导航配置
3. 提交后自动部署到 GitHub Pages

## 🤝 贡献指南

### 代码贡献

1. Fork 项目
2. 创建功能分支
3. 编写测试
4. 提交 Pull Request

### 文档贡献

1. 编辑 `docs/` 目录下的文件
2. 本地预览：`cd docs && bundle exec jekyll serve`
3. 提交更改

## 📞 支持

如有问题，请通过以下方式获取帮助：

- 📖 查看在线文档：https://9531lyj.github.io/AutoCheckBJMF/
- 🐛 提交 Issue：https://github.com/9531lyj/AutoCheckBJMF/issues
- 💬 参与讨论：https://github.com/9531lyj/AutoCheckBJMF/discussions
- 📧 邮件联系：2233613389@qq.com

---

**感谢使用 AutoCheckBJMF 增强版！** 🎉
