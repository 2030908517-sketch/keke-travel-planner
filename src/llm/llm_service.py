"""
LLM 服务模块
对接 DeepSeek API
"""

import os, json, re
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=False)


DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-flash"

class LLMService:
    def __init__(self, api_key=None, base_url=None, model=None):
        key = api_key or os.environ.get("LLM_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
        if not key:
            raise ValueError("请在 .env 中配置 LLM_API_KEY，或设置对应环境变量。")
        self.client = OpenAI(
            api_key=key,
            base_url=base_url or os.environ.get("LLM_BASE_URL") or DEFAULT_BASE_URL,
        )
        self.model = model or os.environ.get("LLM_MODEL") or DEFAULT_MODEL
        self.system_prompt = """你是一个专业的智慧旅行规划助手，名字叫"壳壳"。

## 核心能力
1. 行程规划 —— 根据目的地、天数、预算、旅伴等规划完整行程
2. 景点咨询 —— 介绍景点特色、门票、开放时间等
3. 美食推荐 —— 推荐当地美食和餐厅
4. 交通指南 —— 推荐出行方式和路线
5. 攻略查询 —— 旅行贴士和注意事项
6. 预算评估 —— 估算旅行花费

## 输出规范
- 回答详细、实用、结构化，使用 Markdown
- 包含景点名、餐厅名、价格
- 考虑用户口味偏好（不吃辣/喜辣等）
- 考虑旅伴需求（老人/小孩/情侣等）
- 给出预算明细

## 偏好使用规则
- 用户说"记住/记录/保存/我喜欢/我偏好"，主动提取并确认记录
- 方案中必须参考已有偏好
- 用户问"我的偏好"，直接展示已记录内容"""

    def chat(self, messages, temperature=0.7, max_tokens=2048):
        try:
            r = self.client.chat.completions.create(
                model=self.model, messages=messages,
                temperature=temperature, max_tokens=max_tokens)
            return r.choices[0].message.content or ""
        except:
            return ""

    def quick_chat(self, user_message, context=None, system_extra=None, temperature=0.7):
        system = self.system_prompt
        if system_extra: system += "\n\n" + system_extra
        if context: system += f"\n\n## 可参考的知识\n{context}"
        return self.chat([
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ], temperature=temperature)

    def classify_intent(self, user_input):
        prompt = f"""分析以下用户输入在文旅场景下的意图，只输出 JSON。

用户输入：{user_input}

{{
    "intent": "trip_planning|spot_inquiry|food_recommend|transport_inquiry|guide_inquiry|budget_evaluation|plan_adjustment|general_chat",
    "description": "简短中文描述",
    "info": {{
        "destination": "目的地，无则为空",
        "days": 0,
        "people": 0,
        "budget": 0,
        "companion": "旅伴类型，无则为空",
        "taste": "口味偏好，无则为空",
        "interest": "兴趣，无则为空",
        "time": "出行时间，无则为空"
    }}
}}"""
        messages = [
            {"role": "system", "content": "你是一个文旅意图分析助手。只输出 JSON。"},
            {"role": "user", "content": prompt},
        ]
        result = self.chat(messages, temperature=0.1, max_tokens=500)
        try:
            m = re.search(r'\{.*\}', result, re.DOTALL)
            return json.loads(m.group()) if m else json.loads(result)
        except:
            return {"intent": "unknown", "description": "无法识别", "info": {}}

_llm = None
def get_llm():
    global _llm
    if _llm is None: _llm = LLMService()
    return _llm
