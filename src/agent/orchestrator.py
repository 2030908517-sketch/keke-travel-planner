"""Agent 中枢 — LLM 驱动 + 偏好记忆 + RAG 增强"""

from typing import Optional, Dict, Any

from src.llm.llm_service import get_llm
from src.memory.user_memory import UserMemory


class TravelAgent:
    def __init__(self, memory=None, llm=None):
        self.memory = memory or UserMemory()
        self.llm = llm or get_llm()

    def process(self, user_input: str) -> Dict[str, Any]:
        """处理用户输入完整流程"""
        # 保存用户输入
        self.memory.add_message("user", user_input)

        # 获取偏好
        prefs = self.memory.get_preferences()

        # LLM 意图识别
        try:
            intent_data = self.llm.classify_intent(user_input)
            intent = intent_data.get("intent", "unknown")
            info = intent_data.get("info", {})
            desc = intent_data.get("description", "")
        except:
            intent = "unknown"
            info = {}
            desc = ""

        # 提取并保存偏好
        extracted = self.memory.extract_preferences(user_input)
        if extracted:
            self.memory.save_preferences(extracted)
            prefs = self.memory.get_preferences()

        # RAG 上下文（简化，只用知识库）
        rag_context = self._build_rag_context(user_input, info, prefs)

        # 历史对话
        history = self.memory.get_history_summary()

        # 构建 system extra
        pref_lines = "\n".join(f"  - {k}: {v}" for k, v in prefs.items()) if prefs else "  （暂无）"
        system_extra = f"""## 用户偏好
{pref_lines}

## 最近对话
{history[:600]}

### 偏好规则
- 用户说"记住/记录/保存/我喜欢"，提取并记录
- 方案必须参考已有偏好
- 用户问偏好时展示已记录内容"""

        if rag_context:
            system_extra += f"\n\n## 本地知识参考\n{rag_context[:2000]}"

        # LLM 生成
        response = self.llm.quick_chat(user_input, system_extra=system_extra)

        # 保存回复
        self.memory.add_message("assistant", response)

        # 如果用户明确要记录偏好，再次确保保存
        save_keywords = ["记住", "记录", "保存", "我喜欢", "我偏好", "我不吃", "我不能", "我不喜欢"]
        if any(kw in user_input for kw in save_keywords):
            extra_extract = self.memory.extract_preferences(user_input)
            if info.get("destination"): extra_extract["destination"] = info["destination"]
            if info.get("taste"): extra_extract["taste"] = info["taste"]
            if info.get("companion"): extra_extract["companions"] = info["companion"]
            if extra_extract:
                self.memory.save_preferences(extra_extract)
            prefs = self.memory.get_preferences()

        return {
            "intent": intent,
            "intent_label": self._label(intent),
            "description": desc,
            "response": response,
            "preferences": prefs,
        }

    def _build_rag_context(self, query: str, info: dict, prefs: dict) -> str:
        dest = info.get("destination") or prefs.get("destination", "")
        if not dest:
            return ""
        # 尝试从本地知识库加载
        try:
            import os, json
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
            spots_file = os.path.join(data_dir, "scenic_spots.json")
            if os.path.exists(spots_file):
                with open(spots_file, "r", encoding="utf-8") as f:
                    spots = json.load(f)
                city_spots = [s for s in spots if s.get("city","") == dest]
                if city_spots:
                    lines = ["【景点】"]
                    for s in city_spots[:4]:
                        lines.append(f"- {s['name']}（{s.get('description','')[:80]}）")
                    return "\n".join(lines)
            foods_file = os.path.join(data_dir, "restaurants.json")
            if os.path.exists(foods_file):
                with open(foods_file, "r", encoding="utf-8") as f:
                    foods = json.load(f)
                city_foods = [f for f in foods if f.get("city","") == dest]
                if city_foods:
                    lines = ["\n【美食】"]
                    for f in city_foods[:3]:
                        lines.append(f"- {f['name']}（人均{f.get('avg_cost',0)}元）")
                    return "\n".join(lines)
            return ""
        except:
            return ""

    def _label(self, intent: str) -> str:
        labels = {
            "trip_planning": "行程规划", "spot_inquiry": "景点咨询",
            "food_recommend": "美食推荐", "transport_inquiry": "交通咨询",
            "guide_inquiry": "攻略查询", "budget_evaluation": "预算评估",
            "plan_adjustment": "方案调整", "general_chat": "对话",
            "unknown": "其他",
        }
        return labels.get(intent, "文旅咨询")

    @staticmethod
    def create_default():
        return TravelAgent(memory=UserMemory(), llm=get_llm())
