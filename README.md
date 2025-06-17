<div align="center">
    <h1>🚀 AutoCheckBJMF 增强版</h1>
    <h3>智能化班级魔方自动签到解决方案</h3>

    <p>
        <img src="https://img.shields.io/badge/Python-3.7+-blue.svg?style=for-the-badge">
        <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=for-the-badge">
        <img src="https://img.shields.io/github/license/9531lyj/AutoCheckBJMF?label=License&style=for-the-badge">
        <img src="https://img.shields.io/github/commit-activity/w/9531lyj/AutoCheckBJMF?style=for-the-badge">
        <img src="https://img.shields.io/github/stars/9531lyj/AutoCheckBJMF?style=for-the-badge">
    </p>

    <p>
        <a href="https://9531lyj.github.io/AutoCheckBJMF/">📖 在线文档</a> •
        <a href="#-快速开始">🚀 快速开始</a> •
        <a href="#-功能特性">✨ 功能特性</a> •
        <a href="#-使用教程">📚 使用教程</a> •
        <a href="#-常见问题">❓ 常见问题</a>
    </p>

    <img src="https://github.com/JasonYANG170/AutoCheckBJMF/assets/39414350/7400a5d2-1031-4e31-b189-4cbfa2df51e6" width="600">

    <p><strong>从繁琐的手动配置到一键智能设置，让签到变得简单高效！</strong></p>

    <p>
        <strong>🙏 基于 <a href="https://github.com/JasonYANG170/AutoCheckBJMF">JasonYANG170/AutoCheckBJMF</a> 项目开发</strong><br>
        <em>感谢原作者 JasonYANG170 提供的优秀基础框架</em>
    </p>

</div>

## ⚠️ 免责声明

**请遵守相关法律法规，本程序仅供学习交流使用。严禁将本程序用于违法用途，如有违背平台利益请联系作者。**

## ✨ 功能特性

### 🎯 增强版新特性
- **🚀 一键智能配置**: 3分钟完成全部设置，告别繁琐的手动配置
- **🍪 智能Cookie管理**: 自动从浏览器提取Cookie，支持多用户管理
- **📍 自动位置获取**: 智能GPS定位，支持IP定位、系统GPS、手动选择
- **🏫 智能班级检测**: 自动识别班级信息，支持多班级选择
- **🔒 企业级安全**: 跨平台加密存储，保护用户隐私数据
- **🎨 现代化界面**: 图形化配置向导，用户体验友好

### 📱 支持平台
- **Windows** 10/11 (完全支持)
- **macOS** 10.15+ (完全支持)
- **Linux** Ubuntu/Debian/CentOS (完全支持)

### 📝 支持的签到模式
- ✅ **GPS定位签到** (智能坐标偏移)
- ✅ **二维码签到** (自动识别处理)
- ✅ **GPS+拍照签到** (组合模式)
- 🚧 **密码签到** (开发中)

### 🔧 核心功能
- ✅ **定时自动签到** - 支持每日定时执行
- ✅ **24小时无人值守** - 稳定可靠的后台运行
- ✅ **多用户批量签到** - 支持多个账号同时管理
- ✅ **智能重试机制** - 失败自动重试，提高成功率
- ✅ **实时状态监控** - 详细的签到日志和状态反馈
- ✅ **推送通知支持** - 签到结果实时推送到手机
- ✅ **配置热更新** - 无需重启即可更新配置
- ✅ **安全数据存储** - 本地加密存储，保护隐私

## 🚀 快速开始

### 方法一：一键安装（推荐新手）

```bash
# 1. 下载项目
git clone https://github.com/9531lyj/AutoCheckBJMF.git
cd AutoCheckBJMF

# 2. 运行自动安装脚本
python setup.py

# 3. 启动增强版程序
python main_enhanced.py
```

### 方法二：手动安装（推荐开发者）

```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 安装浏览器驱动（可选，用于自动登录）
pip install webdriver-manager

# 3. 启动程序
python main_enhanced.py
```

### Windows用户专享

安装完成后，您可以通过以下便捷方式启动：

- 🖱️ **双击启动**: `启动AutoCheckBJMF.bat`
- ⚙️ **重新配置**: `配置AutoCheckBJMF.bat`
- 🖥️ **桌面快捷方式**: 自动创建的桌面图标

## 📚 使用教程

### 🎯 首次使用指南

1. **启动程序**
   ```bash
   python main_enhanced.py
   ```

2. **选择配置方式**

   程序会自动弹出配置选择对话框：

   - **🚀 快速自动配置**（推荐）: 程序自动完成所有配置
   - **🧙‍♂️ 详细配置向导**: 逐步自定义每个配置项
   - **❌ 取消**: 退出程序

3. **快速配置流程**（约3分钟）

   ```
   🔍 自动检测浏览器Cookie
   ↓
   🏫 智能识别班级信息
   ↓
   📍 自动获取GPS位置
   ↓
   ✅ 配置完成，开始签到
   ```

4. **开始使用**

   - **手动模式**: 立即执行一次签到
   - **定时模式**: 每日自动签到（可设置具体时间）

### 🔧 详细配置说明

#### Cookie配置选项

| 方式 | 描述 | 适用场景 | 难度 |
|------|------|----------|------|
| 🌐 浏览器自动提取 | 从已登录的浏览器自动获取 | 已在浏览器登录过 | ⭐ |
| 🤖 自动登录获取 | 输入账号密码自动登录 | 记得账号密码 | ⭐⭐ |
| ✋ 手动输入 | 手动复制粘贴Cookie | 熟悉抓包操作 | ⭐⭐⭐ |

#### 位置配置选项

| 方式 | 精度 | 描述 | 推荐度 |
|------|------|------|--------|
| 🌐 IP自动定位 | 城市级 | 基于网络IP自动获取 | ⭐⭐⭐ |
| 📱 系统GPS | 米级 | 使用设备GPS精确定位 | ⭐⭐⭐⭐ |
| 🗺️ 地图选择 | 米级 | 通过地图手动选择位置 | ⭐⭐⭐⭐⭐ |

## 🔍 常见问题

<details>
<summary><strong>❓ Cookie相关问题</strong></summary>

**Q: 提示"Cookie提取失败"怎么办？**

A: 请按以下步骤排查：
1. 确保浏览器已登录班级魔方网站
2. 尝试重新登录后再次提取
3. 如仍失败，选择"手动输入"方式

**Q: Cookie多久会过期？**

A: 通常7-30天，程序会自动检测有效性并提醒更新

**Q: 支持哪些浏览器？**

A: Chrome、Edge、Firefox、Safari、Opera等主流浏览器

</details>

<details>
<summary><strong>📍 定位相关问题</strong></summary>

**Q: GPS定位不准确怎么办？**

A: 建议使用"地图选择"方式，通过腾讯地图精确选择位置

**Q: 提示"定位失败"？**

A: 可能是网络问题，建议：
1. 检查网络连接
2. 尝试使用手动输入坐标
3. 使用VPN后重试

</details>

<details>
<summary><strong>🔧 程序运行问题</strong></summary>

**Q: 程序启动失败？**

A: 请检查：
1. Python版本是否为3.7+
2. 是否正确安装了依赖包
3. 运行 `python setup.py` 重新安装

**Q: 定时签到不工作？**

A: 请确认：
1. 计算机在设定时间是否开机
2. 程序是否正常运行
3. 检查系统时间是否正确

</details>

## 🛠️ 故障排除

### 环境检查

```bash
# 检查Python版本
python --version  # 需要3.7+

# 检查依赖安装
pip list | grep -E "(requests|beautifulsoup4|selenium|cryptography)"

# 测试网络连接
ping k8n.cn
```

### 日志分析

```bash
# 查看详细日志
tail -f AutoCheckBJMF_enhanced.log

# 启用调试模式
python main_enhanced.py --debug
```

### 重置配置

```bash
# 清除所有配置（重新开始）
python -c "from modules.secure_storage import CookieManager; CookieManager().clear_all_data()"
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork** 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 **Pull Request**

### 开发环境

```bash
# 克隆项目
git clone https://github.com/JasonYANG170/AutoCheckBJMF.git
cd AutoCheckBJMF

# 安装开发依赖
pip install -r requirements.txt
pip install pytest black flake8

# 运行测试
pytest tests/

# 代码格式化
black modules/
flake8 modules/
```

## 📄 许可证

本项目采用 [GPL-3.0](LICENSE) 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

### 特别感谢
- 🎯 **原作者 [JasonYANG170](https://github.com/JasonYANG170)**: 感谢提供优秀的 [AutoCheckBJMF](https://github.com/JasonYANG170/AutoCheckBJMF) 基础框架
- 🌟 **开源社区**: 感谢提供的各种优秀工具和库
- 💝 **所有贡献者**: 感谢大家的辛勤付出和宝贵建议

### 项目关系
本项目是基于 [JasonYANG170/AutoCheckBJMF](https://github.com/JasonYANG170/AutoCheckBJMF) 的增强版本，在原有功能基础上添加了：
- 🎯 一键智能配置向导
- 🍪 智能Cookie管理系统
- 🔒 企业级安全存储
- 🎨 现代化用户界面
- 🌍 完整的跨平台支持

## 📞 联系我们

- 🌐 **项目主页**: [GitHub](https://github.com/9531lyj/AutoCheckBJMF)
- 📖 **在线文档**: [GitHub Pages](https://9531lyj.github.io/AutoCheckBJMF/)
- 🐛 **问题反馈**: [Issues](https://github.com/9531lyj/AutoCheckBJMF/issues)
- 💬 **讨论交流**: [Discussions](https://github.com/9531lyj/AutoCheckBJMF/discussions)
- 📧 **邮件联系**: [2233613389@qq.com](mailto:2233613389@qq.com)

### 原项目链接
- 🔗 **原项目**: [JasonYANG170/AutoCheckBJMF](https://github.com/JasonYANG170/AutoCheckBJMF)
- 📚 **原项目文档**: [原项目Wiki](https://github.com/JasonYANG170/AutoCheckBJMF/wiki)

---

<div align="center">
    <h3>⭐ 如果这个项目对您有帮助，请给我们一个Star！</h3>
    <p>
        <a href="https://github.com/9531lyj/AutoCheckBJMF/stargazers">
            <img src="https://img.shields.io/github/stars/9531lyj/AutoCheckBJMF?style=social" alt="GitHub stars">
        </a>
        <a href="https://github.com/9531lyj/AutoCheckBJMF/network/members">
            <img src="https://img.shields.io/github/forks/9531lyj/AutoCheckBJMF?style=social" alt="GitHub forks">
        </a>
    </p>

    [![Star History Chart](https://api.star-history.com/svg?repos=9531lyj/AutoCheckBJMF&type=Date)](https://star-history.com/#9531lyj/AutoCheckBJMF&Date)

    <p><strong>Made with ❤️ by AutoCheckBJMF Team</strong></p>
</div>
