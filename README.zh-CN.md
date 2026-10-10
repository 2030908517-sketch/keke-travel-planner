# 壳壳：旅行规划Web应用

这是《人工智能技术应用与实践》的个人课程作业。通过 DeepSeek API、Python 和 Streamlit，实现旅行建议生成、用户偏好记录和历史对话管理。

作者：葉 聖颢 / Shenghao Ye。项目为个人课程应用原型，代码开发使用了AI辅助。

## 原课程界面

![原答辩材料中的壳壳界面](docs/images/coursework-interface.png)

这张图原样提取自《壳壳-叶圣颢.pptx》第4页，是原课程应用的介绍界面，不是本次重新运行的截图，也没有展示实际行程结果。详见 [MEDIA_SOURCES.md](docs/MEDIA_SOURCES.md)。

## 已有功能

- 根据目的地、天数、预算、同行人等条件生成旅行建议。
- 用关键词规则提取偏好，保存到SQLite。
- 保存多组对话记录，支持回看、继续和删除。
- 按城市名称筛选本地示例数据，优先使用景点资料，未匹配到景点时再查餐厅，放入模型提示。
- 包含电脑和手机窄屏布局的CSS样式。

## 启动

使用 Python 3.10 或更高版本。在本仓库目录执行：

~~~powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
~~~

用文本编辑器打开 .env，在 LLM_API_KEY 后填写自己的API密钥，再运行：

~~~powershell
.venv\Scripts\python.exe run.py
~~~

打开Streamlit输出的网址，通常为 http://localhost:8501。macOS/Linux使用 .venv/bin/python，并用 cp 复制配置示例。

程序首次初始化时会创建新的 src/data/memory.db。本仓库不包含原来的用户偏好、聊天记录或真实密钥。

打开界面时会调用API生成问候语；提交问题时通常会调用意图识别和回复生成。实际使用需要网络、可用模型和API账户，可能产生API费用。运行离线检查不会调用真实API。

## 目前的边界

- 本地JSON由AI辅助搜索整理，用于课程作业；具体来源网址和采集日期未保留，价格与描述未独立核实，不能视为官方或实时文旅信息。
- 当前检索按城市名匹配，没有向量检索。回复优先参考最多4条景点记录，仅在未匹配到景点时再尝试最多3条餐厅记录；目前不会根据问题是否在问美食调整这个顺序。交通、攻略文件暂未接入这条检索路径。
- URL中的用户ID用于区分记录，不是登录或权限控制。不要把课程原型当作公开的私人数据服务。
- 生成回复使用最近对话摘要，不是完整历史消息。
- API异常当前可能返回空结果；旅行方案质量、事实准确性以及全面的真机适配尚未验证。

## 实际检查

~~~powershell
python -m unittest discover -s tests -v
~~~

离线检查使用模拟API回复和临时数据库，不代表真实模型表现。实际完成的检查见 [VERIFICATION.md](docs/VERIFICATION.md)。

## 来源与AI辅助

公开整理时的配置调整、隐私排除与检查也使用了AI辅助，详见 [PREPARATION.md](docs/PREPARATION.md)。

技术文档：[Streamlit](https://docs.streamlit.io/)、[DeepSeek API](https://api-docs.deepseek.com/)、[OpenAI Python客户端](https://github.com/openai/openai-python)。

尚未指定项目整体的开源许可证；依赖各自保留原许可证。公开分发前仍应确认数据来源。
