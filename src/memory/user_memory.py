"""用户记忆模块 — SQLite 持久化存储用户偏好和对话历史"""

import json, sqlite3, os, uuid, re
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

class UserMemory:
    def __init__(self, db_path=None):
        if db_path is None:
            os.makedirs(DB_DIR, exist_ok=True)
            db_path = os.path.join(DB_DIR, "memory.db")
        self.db_path = db_path
        self._user_id = None
        self._conversation_id = None
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            preferences TEXT DEFAULT '{}',
            created_at TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            conversation_id TEXT NOT NULL DEFAULT '',
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )""")
        # 兼容旧数据：如果表没有 conversation_id 列则添加
        try:
            c.execute("ALTER TABLE chat_history ADD COLUMN conversation_id TEXT NOT NULL DEFAULT ''")
        except:
            pass
        conn.commit()
        conn.close()

        # 确保默认用户存在
        self._ensure_default_user()

    def _ensure_default_user(self):
        """确保本地默认用户记录存在，避免重复 UUID 导致偏好丢失"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""INSERT OR IGNORE INTO users (user_id, preferences, created_at)
                      VALUES (?, ?, ?)""",
                  ("default", "{}", datetime.now().isoformat()))
        conn.commit()
        conn.close()

    @property
    def user_id(self):
        if not self._user_id:
            self._user_id = "default"
        return self._user_id

    @user_id.setter
    def user_id(self, value: str):
        self._user_id = value

    @property
    def conversation_id(self) -> str:
        """当前对话窗口 ID，没有则自动生成"""
        if not self._conversation_id:
            self._conversation_id = uuid.uuid4().hex[:12]
        return self._conversation_id

    @conversation_id.setter
    def conversation_id(self, value: str):
        self._conversation_id = value

    def new_conversation(self) -> str:
        """开启一个新的对话窗口，返回新 ID"""
        self._conversation_id = uuid.uuid4().hex[:12]
        return self._conversation_id

    def get_preferences(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT preferences FROM users WHERE user_id=?", (self.user_id,))
        row = c.fetchone()
        if not row:
            # 首次访问此用户，自动创建记录
            c.execute("INSERT OR IGNORE INTO users (user_id, preferences, created_at) VALUES (?,?,?)",
                      (self.user_id, "{}", datetime.now().isoformat()))
            conn.commit()
            conn.close()
            return {}
        conn.close()
        return json.loads(row[0]) if row else {}

    def save_preferences(self, updates: dict):
        prefs = self.get_preferences()
        prefs.update(updates)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO users (user_id, preferences, created_at) VALUES (?,?,?)",
                  (self.user_id, json.dumps(prefs, ensure_ascii=False), datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def extract_preferences(self, text: str) -> dict:
        prefs = {}
        cities = ["成都", "重庆", "西安", "北京", "上海", "广州", "深圳",
                  "杭州", "南京", "武汉", "长沙", "昆明", "大理", "丽江",
                  "桂林", "厦门", "青岛", "三亚", "哈尔滨", "乌鲁木齐"]
        for c in cities:
            if c in text: prefs["destination"] = c; break
        if any(w in text for w in ["带父母","带爸妈","带老人","带长辈"]):
            prefs["companions"] = "父母/老人"
        elif any(w in text for w in ["带小孩","带娃","带孩子","亲子"]):
            prefs["companions"] = "亲子"
        elif any(w in text for w in ["一个人","独自","单人"]):
            prefs["companions"] = "独自"
        elif any(w in text for w in ["情侣","对象","女朋友","男朋友"]):
            prefs["companions"] = "情侣"
        if any(w in text for w in ["不吃辣","不能吃辣","不辣","微辣","不喜欢吃辣"]):
            prefs["taste"] = "不吃辣/微辣"
        elif any(w in text for w in ["吃辣","喜辣","麻辣","无辣不欢","喜欢吃辣"]):
            prefs["taste"] = "喜辣"
        if "省" in text or "便宜" in text or "穷游" in text:
            prefs["budget"] = "节省"
        m = re.search(r'预算[约]?(\d+)', text)
        if m: prefs["budget_amount"] = int(m.group(1))
        m = re.search(r'(\d+)\s*天', text)
        if m: prefs["days"] = int(m.group(1))
        if any(w in text for w in ["自然","风景","山水"]):
            prefs["interest"] = "自然风光"
        elif any(w in text for w in ["历史","文化","古迹","博物馆"]):
            prefs["interest"] = "历史文化"
        elif any(w in text for w in ["美食","吃"]):
            prefs["interest"] = "美食"
        return prefs

    def add_message(self, role: str, content: str):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO chat_history (user_id, conversation_id, role, content, timestamp) VALUES (?,?,?,?,?)",
            (self.user_id, self.conversation_id, role, content, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def get_history(self, limit=20):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "SELECT role, content FROM chat_history WHERE user_id=? AND conversation_id=? ORDER BY timestamp DESC LIMIT ?",
            (self.user_id, self.conversation_id, limit)
        )
        rows = c.fetchall()
        conn.close()
        history = []
        for role, content in reversed(rows):
            history.append({"role": role, "content": content})
        return history

    def get_raw_connection(self):
        """返回原始 SQLite 连接，供外部使用"""
        return sqlite3.connect(self.db_path)

    def get_conversations(self):
        """获取所有对话窗口列表，按对话窗口和轮次分组

        返回: [(conversation_id, [
            {"user": "...", "assistant": "...", "time": "..."},
            ...
        ])]
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("""SELECT conversation_id, role, content, timestamp FROM chat_history
                      WHERE user_id=? ORDER BY timestamp ASC""", (self.user_id,))
        rows = c.fetchall()
        conn.close()

        # 按 conversation_id 分组
        groups = {}
        for row in rows:
            cid = row["conversation_id"] or "default"
            if cid not in groups:
                groups[cid] = []
            groups[cid].append(row)

        result = []
        for cid, msgs in groups.items():
            turns = []
            current = {"user": None, "assistant": None, "time": None}
            for msg in msgs:
                if msg["role"] == "user":
                    if current["user"] is not None and current["assistant"] is not None:
                        turns.append(current)
                    current = {"user": msg["content"], "assistant": None, "time": msg["timestamp"]}
                elif msg["role"] == "assistant" and current["user"] is not None:
                    current["assistant"] = msg["content"]
            if current["user"] is not None:
                turns.append(current)
            result.append((cid, turns))

        return result

    def delete_conversation(self, conversation_id: str):
        """删除某个对话窗口的所有消息"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "DELETE FROM chat_history WHERE user_id=? AND conversation_id=?",
            (self.user_id, conversation_id)
        )
        conn.commit()
        conn.close()

    def get_conversation_messages(self, conversation_id: str):
        """获取某个对话窗口的完整消息列表（用于回看）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(
            """SELECT role, content, timestamp FROM chat_history
                  WHERE user_id=? AND conversation_id=? ORDER BY timestamp ASC""",
            (self.user_id, conversation_id)
        )
        rows = c.fetchall()
        conn.close()
        return [{"role": r["role"], "content": r["content"]} for r in rows]

    def get_history_summary(self, limit=10):
        history = self.get_history(limit)
        if not history: return ""
        parts = []
        for msg in history:
            label = "用户" if msg["role"]=="user" else "助手"
            content = msg["content"][:150]
            parts.append(f"{label}: {content}")
        return "\n".join(parts)
