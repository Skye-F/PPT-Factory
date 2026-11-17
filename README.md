# PPT-Factory

面向 Windows 与 Codex 的演示文稿工作区。支持内容策划、HTML 预览、可编辑 PowerPoint 制作与交付检查。每次任务的资料与产物存放在本地 `projects/`。

1. 下载 ZIP 或克隆本仓库，在 Codex 中打开解压或克隆后的目录。
2. 确认已安装 Python 3.14，并在项目目录运行 `python install.py`。也可以让 Codex 在你确认后运行。安装会从 GitHub 拉取 8 个固定版本的 Skills，并从 PyPI 安装项目虚拟环境依赖。
3. 在这个目录开启新的 Codex 对话，描述受众、用途、演示时长和交付格式。例：“做一份 10 分钟的培训演示，先给大纲和两个视觉方向，确认后输出可编辑 PPTX。”
4. 如需验证原生导出，运行 `.\.venv\Scripts\python.exe smoke.py`，再用 PowerPoint 打开 `tests/smoke/output/sample.pptx`。完整 PowerPoint 渲染验收需要本机安装 PowerPoint。PptxGenJS 路线需要另外准备 Node.js 与项目级 PptxGenJS 或可用的 Codex 随附运行库。

阅读 [项目规则](AGENTS.md)、[工作流](config/workflow-rules.md) 和 [技能清单](config/skills-registry.md)。

本仓库原创内容采用 MIT 许可证。安装器独立下载的第三方组件适用各自的许可证，详见 [第三方声明](THIRD_PARTY_NOTICES.md)。
