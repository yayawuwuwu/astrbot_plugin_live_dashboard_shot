# 📸 Live-Dashboard Screenshot for AstrBot

[![AstrBot Plugin](https://img.shields.io/badge/AstrBot-插件商店-blue)](https://plugins.astrbot.app)

一个 AstrBot 插件，用于截取 [Live-Dashboard](https://github.com/Monika-Dream/live-dashboard) 的实时设备状态，并分设备发送到群聊。  
**支持通过 AstrBot 插件商店一键安装。**

> 💡 **为什么做这个插件？**  
> 原本的 [Live Dashboard 插件](https://github.com/DBJD-CR/astrbot_plugin_live_dashboard) 只能返回文字状态信息，不支持图片发送。为了让群友更直观地看到设备实时截图，我做了这个能分设备截图并发送图片的插件。

---

## ✨ 特性

- 🖼️ **图片发送**：弥补原版插件无法发送图片的遗憾，直接截图仪表盘发送到群聊
- 🖥️ **多设备分别截图**：依次点击每个设备，截取各自的详情页，条理清晰
- 📱 **自适应布局**：窄视口触发移动端适配，截图内容清晰、排版自然
- ⚡ **高清输出**：2 倍 Retina 分辨率，文字与图表边缘锐利
- 🔧 **双命令支持**：`/仪表盘` 和 `/视奸` 均可触发

---

## 📋 前置条件

使用本插件前，你需要：

### 1. 部署 Live-Dashboard 服务端
- 项目地址：https://github.com/Monika-Dream/live-dashboard
- 推荐使用 Docker 一键部署，部署后你会获得一个仪表盘访问地址（如 `http://你的IP:7283`）和设备的 `token`。
- 详细部署教程见官方 Wiki：[快速部署](https://github.com/Monika-Dream/live-dashboard/wiki/%E5%BF%AB%E9%80%9F%E9%83%A8%E7%BD%B2)

### 2. 安装 AstrBot 框架
- AstrBot 是一个多平台的 QQ 机器人框架，本插件运行在 AstrBot 之上。
- 部署教程：https://astrbot.app

### 3. 在 AstrBot 容器/环境中安装浏览器依赖
截图功能基于 Playwright 无头浏览器，需要安装 Chromium 及系统库。执行以下命令：
```bash
pip install playwright Pillow --break-system-packages
playwright install chromium
playwright install-deps chromium   # 如果容器内缺少系统库
```

---

🚀 安装插件

方式一：通过 AstrBot 插件商店安装（推荐）

1. 在 AstrBot WebUI 中进入 插件管理 → 插件商店。
2. 搜索 Live-Dashboard 截图 或 live-dashboard-shot。
3. 点击 安装，插件会自动下载并安装到 data/plugins/ 目录。
4. 重启 AstrBot。

方式二：手动安装

1. 将本仓库克隆或下载到 AstrBot 的 data/plugins/ 目录下：
   ```bash
   cd AstrBot/data/plugins
   git clone https://github.com/yayawuwuwu/astrbot_plugin_live_dashboard_shot.git
   ```
2. 安装所需依赖（如果未安装）：
   ```bash
   pip install playwright Pillow --break-system-packages
   playwright install chromium
   ```
3. 重启 AstrBot。

---

## ⚙️ 配置

一.本插件支持在 AstrBot WebUI 中进行可视化配置，无需编辑代码。

1. 安装插件后，在面板左侧进入 **插件管理**。
2. 找到 `Live-Dashboard 截图`，点击 **配置** 按钮。
3. 根据页面提示填写你的仪表盘地址和设备列表（每行一个设备名称）。
4. 点击 **保存** 并重载插件，配置即刻生效。

> 设备名称必须与 Live-Dashboard 页面左侧列表中的文字完全一致。

二.如设置不生效，需要=需要修改 main.py 中的几个变量，以匹配你的实际环境：

· url：你的 Live-Dashboard 访问地址，例如 "http://172.17.0.1:7283"（AstrBot 容器内请用宿主机内网 IP）
· device_names：仪表盘上需要截图的设备显示名称，必须与页面文本完全一致，例如 ["芽芽的拯救者y7000", "芽芽的一加ace5至尊版"]
· viewport：截图视口大小，宽 600 高 1000 可触发移动端自适应
· device_scale_factor：清晰度倍数，2 表示 Retina 高清

📌 如何获取设备名称？
打开你的 Live-Dashboard 页面，左侧设备列表中的文字就是设备名称。

---

🎮 使用方法

在群聊中发送以下任一命令，机器人会依次返回每台设备的实时截图：

· /仪表盘
· /视奸

每张截图包含对应设备的完整状态信息（CPU、内存、温度等）。

---

🐛 常见问题

截图黑屏或空白
检查 url 是否正确，AstrBot 在 Docker 容器内时需使用宿主机内网 IP（如 172.17.0.1），而非 127.0.0.1。

提示 playwright 未安装
在容器/宿主环境执行 pip install playwright --break-system-packages 和 playwright install chromium。

点击设备名称无效
确保 device_names 里的文字与仪表盘页面上的完全一致（包括大小写、空格）。

图片模糊
增大 device_scale_factor（例如 3）或调大视口宽度。

插件加载失败
查看 AstrBot 日志 docker logs astrbot，检查 metadata.yaml 是否完整，以及 Python 依赖是否已安装。

---

🔗 相关项目

· Live-Dashboard - 多设备实时状态监测面板
· 原版 Live Dashboard 插件 - 文字版设备状态查询
· AstrBot - 多平台 QQ 机器人框架

---

📄 许可

MIT License
