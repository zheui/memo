# 桌面备忘录 (Desktop Memo)
一个现代化、轻量级的桌面备忘录应用，支持日历管理、倒计时提醒、备忘录记录和个性化设置，帮助用户高效管理日常事务。
---
#功能特性

# 核心功能
- 日历视图: 提供现代风格的日历组件，支持月份切换，直观查看日期。
- 倒计时提醒: 自动计算未来日期的天数，并在界面上显示倒计时信息。
- 备忘录管理:
  - 支持按日期记录备忘事项。
  - 备忘录内容可标记为完成状态（勾选框）。
  - 支持置顶重要备忘事项，优先显示。
- 个性化设置:
  - 背景颜色和字体颜色自定义。
  - 字体大小和透明度调节。
  - 开机自动启动选项。
- 数据导出: 支持将备忘录数据导出为 CSV 文件，方便备份或迁移。
- 全局拖动: 支持通过鼠标拖动窗口任意位置移动。
---
#截图预览

#主界面
![image](https://github.com/user-attachments/assets/9d7f9a07-314e-4ad5-9994-5e13ddd36b03)

#设置界面
![image](https://github.com/user-attachments/assets/65c47f28-37ed-4a1c-a9cc-b3b3c222ee15)

#安装与运行

#前置条件
- 操作系统: Windows / macOS / Linux
- Python 版本: Python 3.8 或更高版本
- 依赖项: PyQt5, 其他依赖项会自动安装

#安装步骤
1. 克隆本仓库：
2. 安装依赖项：
3. 运行应用：


# 打包为可执行文件
如果需要生成独立的可执行文件，请参考以下步骤：

1. 安装 PyInstaller：

2. 准备图标文件：
app.ico(32*32)
memo.ico(256*256)
   
3. 使用打包脚本生成单文件可执行程序：
运行build.py

4. 打包后的文件将位于 `dist` 目录下。

---

#使用指南

#添加备忘
1. 点击“📝 添加”按钮，在当天的备忘列表中新增一条记录。
2. 输入备忘内容并保存。

#标记完成
- 点击备忘事项左侧的复选框，标记为已完成或未完成。

#置顶备忘
- 右键点击备忘事项，选择“📌 置顶”以将其置顶显示。

#导出数据
- 点击“📤 导出”按钮，选择保存路径，将备忘录数据导出为 CSV 文件。

#设置个性化选项
- 点击右上角的“⚙”按钮，打开设置界面，调整背景颜色、字体大小等。

---

#配置文件说明

桌面备忘录使用以下配置文件存储用户数据和设置：

- **`memos.json`**: 存储用户的备忘录数据，按日期组织。
- **`config.ini`**: 存储用户的个性化设置（如背景颜色、字体大小等）。

> 注意: 如果删除这些文件，应用将在下次启动时重新生成默认配置。

---

# 贡献指南

我们非常欢迎任何形式的贡献！如果你有兴趣改进这个项目，请遵循以下步骤：

1. Fork 本仓库:
   点击页面右上角的 "Fork" 按钮，创建你自己的副本。

2. 克隆你的 Fork:

3. 创建新分支:

4. 提交更改:
   完成修改后，提交代码并推送到你的远程仓库：

5. 创建 Pull Request:
   在 GitHub 上打开你的分支，点击 "Compare & pull request" 按钮，描述你的更改并提交。

---

# 联系方式

如有任何问题或建议，请通过以下方式联系我们：

- 邮箱: 859165641@qq.com
- GitHub Issues: (https://github.com/zheui/memo/issues)
---
感谢您的支持！希望这款桌面备忘录能为您的日常工作和生活带来便利 😊
--- 
