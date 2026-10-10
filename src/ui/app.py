"""
壳壳 — 智能旅行规划
"""

import streamlit as st
import sys
import os
import html

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agent.orchestrator import TravelAgent


st.set_page_config(
    page_title="壳壳 — 智能旅行规划",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Noto+Serif+SC:wght@500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg: #f7f1e8;
    --paper: #fffdfa;
    --paper-soft: rgba(255, 255, 255, 0.72);
    --ink: #111827;
    --ink-soft: #4b5563;
    --muted: #9a8f83;
    --line: rgba(17, 24, 39, 0.08);
    --gold: #b8894d;
    --gold-soft: rgba(184, 137, 77, 0.14);
    --navy: #111827;
    --shadow: 0 28px 80px rgba(17, 24, 39, 0.11);
    --shadow-soft: 0 14px 36px rgba(17, 24, 39, 0.08);
}

* {
    box-sizing: border-box;
}

html {
    font-size: 16px;
}

.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
    color: var(--ink);
    background:
        radial-gradient(circle at 12% 12%, rgba(184, 137, 77, 0.16), transparent 28%),
        radial-gradient(circle at 86% 8%, rgba(132, 92, 255, 0.09), transparent 30%),
        linear-gradient(135deg, #f8f2e9 0%, #fffaf2 44%, #f2e7d8 100%);
    -webkit-font-smoothing: antialiased;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(255,255,255,0.32) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.32) 1px, transparent 1px);
    background-size: 44px 44px;
    opacity: 0.34;
    mask-image: radial-gradient(circle at center, black, transparent 76%);
}

.stApp > header {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}

.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
}

.main > div {
    max-width: 980px;
    margin: 0 auto;
    padding: 0 1.5rem 2rem;
}

/* =========================
 Hero
 全部居中对齐，压缩顶部高度
========================= */
.hero {
 width: 100%;
 max-width: 860px;
 margin: 0 auto;
 padding: 2rem 0 0.75rem;

 display: flex;
 flex-direction: column;
 align-items: center;
 justify-content: center;

 text-align: center;
}

.hero h1 {
 width: 100%;
 margin: 0;
 padding-left: 0.06em;

 font-family: 'DM Serif Display', 'Noto Serif SC', Georgia, serif;
 font-size: clamp(1.95rem, 3.4vw, 2.65rem);
 font-weight: 400;
 line-height: 1;
 letter-spacing: -0.052em;
 color: var(--navy);

 text-align: center;
}

.brand-kicker {
 display: inline-flex;
 align-items: center;
 justify-content: center;
 gap: 0.42rem;

 width: fit-content;
 max-width: calc(100vw - 48px);
 margin: 0.56rem auto 0;
 padding: 0.27rem 0.64rem;

 border-radius: 999px;
 border: 1px solid rgba(184, 137, 77, 0.18);
 background: rgba(255, 255, 255, 0.48);
 backdrop-filter: blur(16px);

 color: var(--gold);
 font-size: 0.56rem;
 font-weight: 800;
 letter-spacing: 0.13em;
 text-transform: uppercase;
 white-space: nowrap;

 box-shadow:
 0 8px 20px rgba(184, 137, 77, 0.055),
 inset 0 1px 0 rgba(255, 255, 255, 0.82);
}

.brand-dot {
 flex: 0 0 auto;
 width: 5px;
 height: 5px;
 border-radius: 999px;
 background: var(--gold);
 box-shadow: 0 0 0 3px rgba(184, 137, 77, 0.12);
}

.hero .sub {
 width: 100%;
 max-width: 640px;

 margin: 0.56rem auto 0;

 color: rgba(17, 24, 39, 0.56);
 font-size: 0.86rem;
 line-height: 1.65;
 text-align: center;
}

.hero .sub strong {
 color: var(--navy);
 font-weight: 750;
}

.hero-line {
 width: 58px;
 height: 1px;
 margin: 0.55rem auto 0;
 background: linear-gradient(90deg, transparent, rgba(184,137,77,0.68), transparent);
}

/* =========================
 Chat Card
 降低输出框高度，保证输入区同屏展示
========================= */
.vessel-wrap {
 position: relative;
 max-width: 860px;
 margin: 0 auto;
}

.vessel {
 position: relative;

 min-height: 430px;
 height: 46vh;
 max-height: 500px;

 overflow-y: auto;
 padding: 1.65rem 1.85rem;

 border-radius: 30px;
 border: 1px solid rgba(184, 137, 77, 0.18);
 background: rgba(255, 255, 255, 0.76);
 backdrop-filter: blur(30px);

 box-shadow:
 0 26px 76px rgba(17, 24, 39, 0.11),
 inset 0 1px 0 rgba(255,255,255,0.82);
}

.vessel::before {
 content: "";
 position: absolute;
 inset: 0;
 border-radius: 30px;
 pointer-events: none;
 background: linear-gradient(180deg, rgba(255,255,255,0.66), transparent 38%);
}

.vessel::-webkit-scrollbar {
    width: 6px;
}

.vessel::-webkit-scrollbar-track {
    background: transparent;
}

.vessel::-webkit-scrollbar-thumb {
    background: rgba(184, 137, 77, 0.32);
    border-radius: 999px;
}

/* =========================
   Messages
========================= */
.msg {
    position: relative;
    z-index: 1;
    margin-bottom: 1.1rem;
}

.msg:last-child {
    margin-bottom: 0;
}

.msg-user {
    display: flex;
    justify-content: flex-end;
}

.msg-user .bbl {
    max-width: min(78%, 600px);
    padding: 0.78rem 1.05rem;
    border-radius: 20px 20px 6px 20px;
    background: linear-gradient(135deg, #111827 0%, #263044 100%);
    color: #ffffff;
    font-size: 0.96rem;
    line-height: 1.75;
    font-weight: 450;
    box-shadow: 0 16px 38px rgba(17, 24, 39, 0.18);
}

.msg-assist {
    display: grid;
    grid-template-columns: 36px 1fr;
    gap: 0.78rem;
    align-items: start;
}

.assist-avatar {
    width: 36px;
    height: 36px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    color: var(--gold);
    background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(247,241,232,0.92));
    border: 1px solid rgba(184, 137, 77, 0.24);
    box-shadow: 0 10px 24px rgba(184, 137, 77, 0.12);
    font-family: 'DM Serif Display', serif;
    font-size: 1.05rem;
}

.msg-assist .meta {
    display: flex;
    align-items: center;
    gap: 0.52rem;
    margin-bottom: 0.24rem;
    color: var(--gold);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.msg-assist .meta::after {
    content: "";
    width: 72px;
    height: 1px;
    background: linear-gradient(90deg, rgba(184,137,77,0.38), transparent);
}

.msg-assist .bbl {
    color: var(--ink);
    font-size: 0.98rem;
    line-height: 1.9;
    font-weight: 400;
}

.msg-assist .bbl p {
    margin: 0.35rem 0;
}

.msg-assist .bbl strong {
    color: var(--navy);
    font-weight: 750;
}

.msg-assist .bbl h1,
.msg-assist .bbl h2,
.msg-assist .bbl h3 {
    font-family: 'DM Serif Display', 'Noto Serif SC', Georgia, serif;
    color: var(--navy);
    font-weight: 400;
    letter-spacing: -0.025em;
}

.msg-assist .bbl h1 {
    font-size: 1.55rem;
    margin: 1rem 0 0.35rem;
}

.msg-assist .bbl h2 {
    font-size: 1.32rem;
    margin: 0.9rem 0 0.3rem;
}

.msg-assist .bbl h3 {
    font-size: 1.12rem;
    margin: 0.8rem 0 0.25rem;
}

.msg-assist .bbl ul,
.msg-assist .bbl ol {
    padding-left: 1.2rem;
    margin: 0.35rem 0;
}

.msg-assist .bbl li {
    margin: 0.2rem 0;
}

.msg-assist .bbl table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 0.8rem 0;
    overflow: hidden;
    border-radius: 16px;
    border: 1px solid rgba(17, 24, 39, 0.08);
    background: rgba(255,255,255,0.72);
    font-size: 0.88rem;
}

.msg-assist .bbl th,
.msg-assist .bbl td {
    padding: 0.55rem 0.7rem;
    text-align: left;
    border-bottom: 1px solid rgba(17, 24, 39, 0.07);
}

.msg-assist .bbl tr:last-child td {
    border-bottom: none;
}

.msg-assist .bbl th {
    background: rgba(184, 137, 77, 0.11);
    color: var(--navy);
    font-weight: 700;
}

.msg-assist .bbl code {
    padding: 0.12rem 0.34rem;
    border-radius: 8px;
    background: rgba(184, 137, 77, 0.12);
    color: #8a5a28;
    font-size: 0.88rem;
}

/* =========================
   Empty State
========================= */
.empty-mute {
    position: relative;
    z-index: 1;
    display: grid;
    place-items: center;
    min-height: 340px;
    color: rgba(17, 24, 39, 0.38);
    text-align: center;
}

.empty-card {
    max-width: 420px;
}

.empty-icon {
    width: 52px;
    height: 52px;
    display: grid;
    place-items: center;
    margin: 0 auto 1rem;
    border-radius: 50%;
    color: var(--gold);
    background: rgba(184, 137, 77, 0.12);
    border: 1px solid rgba(184,137,77,0.18);
    font-size: 1.3rem;
}

.empty-title {
    margin-bottom: 0.35rem;
    color: var(--navy);
    font-family: 'DM Serif Display', 'Noto Serif SC', Georgia, serif;
    font-size: 1.45rem;
}

.empty-desc {
    font-size: 0.92rem;
    line-height: 1.75;
}

/* 聊天框和输入区之间的真实间距 */
.input-gap {
 height: 14px;
 max-width: 860px;
 margin: 0 auto;
}

/* =========================
 Input Area
 缩小输入框与按钮间距
========================= */
.main div[data-testid="stHorizontalBlock"] {
 max-width: 860px;
 margin: 0 auto !important;
 column-gap: 0.45rem !important;
 gap: 0.45rem !important;
 align-items: center;
}

/* 清理 TextInput 外层默认间距和背景 */
.main .stTextInput {
 margin: 0 !important;
}

.main .stTextInput > div {
 margin: 0 !important;
 padding: 0 !important;
 background: transparent !important;
 border: none !important;
}

.main .stTextInput > div > div {
 margin: 0 !important;
 padding: 0 !important;
 background: transparent !important;
 border: none !important;
 box-shadow: none !important;
}

/* 兼容 Streamlit / BaseWeb 输入框容器 */
.main .stTextInput div[data-baseweb="input"] {
 background: transparent !important;
 border: none !important;
 box-shadow: none !important;
}

/* 输入框本体 */
.main .stTextInput input {
 width: 100% !important;
 height: 48px !important;

 border-radius: 13px !important;
 border: 1px solid rgba(17, 24, 39, 0.09) !important;
 outline: none !important;

 background: rgba(255, 255, 255, 0.9) !important;
 color: var(--navy) !important;

 padding: 0.72rem 1rem !important;
 font-size: 0.94rem !important;
 font-weight: 430 !important;

 box-shadow:
 0 10px 24px rgba(17, 24, 39, 0.05),
 inset 0 1px 0 rgba(255,255,255,0.9) !important;

 transition:
 border-color 160ms ease,
 box-shadow 160ms ease,
 background 160ms ease;
}

.main .stTextInput input:focus {
 border-color: rgba(184, 137, 77, 0.52) !important;
 background: rgba(255, 255, 255, 0.98) !important;
 box-shadow:
 0 0 0 4px rgba(184,137,77,0.11),
 0 14px 32px rgba(17,24,39,0.065),
 inset 0 1px 0 rgba(255,255,255,0.96) !important;
}

.main .stTextInput input::placeholder {
 color: rgba(17, 24, 39, 0.36) !important;
}

/* 发送按钮 */
.main .stButton > button {
 width: 100% !important;
 height: 48px !important;

 border-radius: 13px !important;
 border: 1px solid rgba(17, 24, 39, 0.08) !important;

 background: rgba(255, 255, 255, 0.88) !important;
 color: var(--navy) !important;

 font-size: 0.94rem !important;
 font-weight: 700 !important;
 letter-spacing: 0.02em;

 box-shadow:
 0 10px 24px rgba(17, 24, 39, 0.065),
 inset 0 1px 0 rgba(255,255,255,0.9) !important;

 transition:
 transform 160ms ease,
 box-shadow 160ms ease,
 background 160ms ease,
 border-color 160ms ease;
}

.main .stButton > button:hover {
 transform: translateY(-1px);
 background: #ffffff !important;
 border-color: rgba(184, 137, 77, 0.28) !important;
 box-shadow:
 0 16px 36px rgba(17, 24, 39, 0.10),
 inset 0 1px 0 rgba(255,255,255,0.95) !important;
}

.main .stButton > button:active {
 transform: translateY(0);
}

/* =========================
   Sidebar
========================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(250,246,238,0.94));
    border-right: 1px solid rgba(17, 24, 39, 0.08);
    box-shadow: 10px 0 44px rgba(17, 24, 39, 0.04);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.25rem;
}

.sidebar-brand {
    padding: 0.6rem 0.2rem 0.9rem;
}

.sidebar-title {
    font-family: 'DM Serif Display', 'Noto Serif SC', Georgia, serif;
    font-size: 1.7rem;
    font-weight: 400;
    line-height: 1;
    color: var(--navy);
    letter-spacing: -0.04em;
}

.sidebar-label {
    margin-top: 0.36rem;
    color: var(--gold);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.sidebar-section {
    margin: 0.9rem 0 0.35rem;
    color: rgba(17, 24, 39, 0.42);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

section[data-testid="stSidebar"] .stButton > button {
    min-height: 44px !important;
    height: auto !important;

    padding: 0.68rem 0.78rem !important;
    border-radius: 16px !important;

    background: rgba(255, 255, 255, 0.62) !important;
    border: 1px solid rgba(184, 137, 77, 0.13) !important;

    color: rgba(17, 24, 39, 0.76) !important;

    box-shadow:
        0 8px 22px rgba(17, 24, 39, 0.035),
        inset 0 1px 0 rgba(255,255,255,0.82) !important;

    font-size: 0.8rem !important;
    font-weight: 580 !important;
    line-height: 1.45 !important;
    text-align: left !important;

    transition:
        transform 160ms ease,
        background 160ms ease,
        border-color 160ms ease,
        box-shadow 160ms ease,
        color 160ms ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(184, 137, 77, 0.10) !important;
    border-color: rgba(184, 137, 77, 0.32) !important;
    color: var(--navy) !important;

    transform: translateY(-1px);
    box-shadow:
        0 12px 26px rgba(17, 24, 39, 0.055),
        inset 0 1px 0 rgba(255,255,255,0.86) !important;
}

section[data-testid="stSidebar"] hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(17,24,39,0.12), transparent);
    margin: 1rem 0;
}

/* 侧边栏删除按钮（X）文本居中 */
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] div:last-child .stButton > button {
    text-align: center !important;
    padding: 0.68rem 0.2rem !important;
}

/* =========================
   Spinner
========================= */
.stSpinner > div {
    border-color: var(--gold) !important;
    border-top-color: transparent !important;
}

/* =========================
   Mobile
========================= */
@media (max-width: 768px) {
 .main > div {
 padding: 0 1rem 1.2rem;
 }

 .hero {
 max-width: 100%;
 padding: 1.7rem 0 0.65rem;
 }

 .hero h1 {
 font-size: 2.25rem;
 text-align: center;
 }

 .brand-kicker {
 margin: 0.45rem auto 0;
 padding: 0.25rem 0.56rem;
 font-size: 0.5rem;
 letter-spacing: 0.1em;
 }

 .hero .sub {
 max-width: 92%;
 margin: 0.5rem auto 0;
 font-size: 0.82rem;
 line-height: 1.52;
 text-align: center;
 }

 .hero-line {
 margin: 0.5rem auto 0;
 }

 .vessel-wrap {
 max-width: 100%;
 }

 .vessel {
 min-height: 390px;
 height: 48vh;
 max-height: 480px;
 padding: 1.1rem;
 border-radius: 24px;
 }

 .vessel::before {
 border-radius: 24px;
 }

 .input-gap {
 height: 12px;
 }

 .msg-assist {
 grid-template-columns: 30px 1fr;
 gap: 0.58rem;
 }

 .assist-avatar {
 width: 30px;
 height: 30px;
 font-size: 0.95rem;
 }

 .msg-user .bbl {
 max-width: 88%;
 }

 .main div[data-testid="stHorizontalBlock"] {
 gap: 0.35rem !important;
 column-gap: 0.35rem !important;
 margin: 0 auto !important;
 }

 .main .stTextInput input {
 height: 46px !important;
 border-radius: 12px !important;
 font-size: 0.9rem !important;
 }

 .main .stButton > button {
 height: 46px !important;
 border-radius: 12px !important;
 font-size: 0.9rem !important;
 }
}
</style>
""", unsafe_allow_html=True)


def safe_html(text: str) -> str:
    """
    防止用户输入或模型输出中的 HTML 破坏页面结构。
    同时保留换行，去除 Markdown 符号。
    """
    import re

    if text is None:
        return ""

    # 先去除 Markdown 符号：加粗、斜体、标题、列表、分隔线
    cleaned = str(text)
    cleaned = re.sub(r'\*\*\*|\*\*|\*', '', cleaned)
    cleaned = re.sub(r'#{1,6}\s*', '', cleaned)
    cleaned = re.sub(r'```|`', '', cleaned)
    cleaned = re.sub(r'~~', '', cleaned)
    cleaned = re.sub(r'^[-*+]{1,3}\s', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'^\d+\.\s', '', cleaned, flags=re.MULTILINE)

    escaped = html.escape(cleaned)
    escaped = escaped.replace("\n", "<br>")

    return escaped


def init():
    if "agent" not in st.session_state:
        with st.spinner("正在唤醒壳壳..."):
            try:
                st.session_state.agent = TravelAgent.create_default()
            except ValueError as exc:
                st.error(str(exc))
                st.stop()
            st.session_state.messages = []
            st.session_state.queries = 0
            st.session_state.show_history = False
            st.session_state.viewing_conversation = None

            # URL 参数 ?user=xxx 区分用户，无参数则自动分配随机 ID
            query_params = st.query_params
            user_param = query_params.get("user", "")
            if user_param:
                st.session_state.agent.memory.user_id = user_param
            else:
                # 没传 ?user=，自动分配并跳转
                import uuid
                auto_id = uuid.uuid4().hex[:8]
                st.session_state.agent.memory.user_id = auto_id
                # 重定向到带用户 ID 的 URL
                current_url = st.query_params.to_dict()
                current_url["user"] = auto_id
                st.query_params.update(current_url)

            # 初始化时默认开一个新对话窗口
            st.session_state.agent.memory.new_conversation()

            greeting = (
                st.session_state.agent.llm.quick_chat(
                    "用一句话介绍你是旅行规划助手壳壳，语气高级、温柔、简洁",
                    temperature=0.5
                )
                or "你好，我是壳壳。把目的地、时间、预算和偏好告诉我，我会为你整理一份从容而好用的旅行计划。"
            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": greeting
            })

            # 首次进入时显示用户 ID 提示
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"✦ 你的用户ID: **{st.session_state.agent.memory.user_id}**  \n请收藏此链接以便后续继续使用。你也可以在地址栏把 `user=` 后面的 ID 改成你喜欢的名字。"
            })


def sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-title">壳壳</div>
            <div class="sidebar-label">Travel Atelier</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="sidebar-section">精选灵感</div>',
            unsafe_allow_html=True
        )

        examples = [
            {
                "label": "成都｜父母同行的松弛三日",
                "prompt": "我想带父母去成都玩3天，预算3000左右，不吃辣，希望行程轻松、少走路，住宿和交通也请一起建议。"
            },
            {
                "label": "京都｜初秋庭院与町家漫游",
                "prompt": "请帮我规划一份京都初秋4日旅行，偏好庭院、寺院、町家小店和安静咖啡馆，希望节奏从容、不赶景点。"
            },
            {
                "label": "大理｜洱海边的慢生活周末",
                "prompt": "我想去大理过一个3天2晚的周末，偏好洱海、古城、咖啡、日落和轻松拍照，请安排一份不特种兵的路线。"
            },
            {
                "label": "上海｜艺术馆、街区与餐酒馆",
                "prompt": "请规划一份上海2日城市漫游路线，偏好艺术馆、老街区、独立书店、咖啡馆和有氛围的餐酒馆。"
            },
            {
                "label": "香港｜复古街景与海风夜色",
                "prompt": "我想去香港玩3天，喜欢复古街景、海边散步、地道美食、夜景和小众拍照点，请帮我规划路线。"
            },
        ]

        for i, item in enumerate(examples):
            if st.button(
                item["label"],
                use_container_width=True,
                key=f"sidebar_example_{i}"
            ):
                st.session_state.pending = item["prompt"]

        st.markdown("---")

        st.markdown(
            '<div class="sidebar-section">个人化</div>',
            unsafe_allow_html=True
        )

        if st.button("查看我的旅行偏好", use_container_width=True, key="sidebar_prefs"):
            st.session_state.pending = (
                "请总结一下目前你记住的我的旅行偏好，包括目的地偏好、预算、饮食、同行人和旅行节奏。"
            )

        if st.button("开启新对话", use_container_width=True, key="sidebar_new"):
            st.session_state.agent.memory.new_conversation()
            st.session_state.messages = []
            st.session_state.queries = 0
            st.session_state.viewing_conversation = None
            st.session_state.show_history = False

            greeting = (
                st.session_state.agent.llm.quick_chat(
                    "用一句话介绍你是壳壳，语气高级、温柔、简洁",
                    temperature=0.5
                )
                or "你好，我是壳壳。告诉我你想去哪里，我来帮你把旅程安排妥帖。"
            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": greeting
            })

            st.rerun()

        # 对话记录 —— 点击切换展开/收起
        if st.button("对话记录", use_container_width=True, key="sidebar_history"):
            st.session_state.show_history = not st.session_state.get("show_history", False)
            st.rerun()

        # 展开时在侧边栏显示历史对话列表
        if st.session_state.get("show_history", False):
            st.markdown(
                '<div class="sidebar-section">历史对话</div>',
                unsafe_allow_html=True
            )
            convos = st.session_state.agent.memory.get_conversations()
            if convos:
                for i, (cid, turns) in enumerate(reversed(convos)):
                    if turns:
                        first_msg = turns[0]["user"] or "不知道去哪"
                        summary = first_msg[:24] + "..." if len(first_msg) > 24 else first_msg
                        turn_count = len(turns)
                        
                        col_a, col_b = st.columns([4.2, 1])
                        with col_a:
                            if st.button(f"{summary}", use_container_width=True, key=f"hist_{cid}"):
                                _resume_conversation(cid)
                                st.rerun()
                        with col_b:
                            if st.button("✕", use_container_width=True, key=f"del_{cid}"):
                                _delete_conversation(cid)
                                st.rerun()
            else:
                st.markdown(
                    '<div style="font-size:0.78rem;color:rgba(17,24,39,0.4);padding:0.4rem 0;">暂无历史对话</div>',
                    unsafe_allow_html=True
                )


def _resume_conversation(cid: str):
    """恢复某个历史对话窗口，加载其完整消息历史作为上下文"""
    st.session_state.viewing_conversation = cid
    st.session_state.show_history = False

    # 设置 agent 的当前对话 ID 为该历史窗口
    st.session_state.agent.memory.conversation_id = cid

    # 从数据库加载完整历史
    msgs = st.session_state.agent.memory.get_conversation_messages(cid)
    st.session_state.messages = []
    st.session_state.queries = len([m for m in msgs if m["role"] == "user"])

    # 给首个助手消息换成一个友好的恢复提示
    found_greeting = False
    for msg in msgs:
        if msg["role"] == "assistant" and not found_greeting:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"*已恢复对话，继续上次的讨论吧 ✦*"
            })
            found_greeting = True
        st.session_state.messages.append(msg)


def _delete_conversation(cid: str):
    """删除某个历史对话窗口"""
    st.session_state.agent.memory.delete_conversation(cid)
    # 如果当前正在查看/继续的就是被删的对话，清空界面
    if st.session_state.get("viewing_conversation") == cid:
        st.session_state.messages = []
        st.session_state.viewing_conversation = None
        st.session_state.queries = 0


def process_input(text: str):
    if not text or not text.strip():
        return

    cleaned_text = text.strip()

    st.session_state.messages.append({
        "role": "user",
        "content": cleaned_text
    })

    with st.spinner("壳壳正在整理路线、节奏与细节..."):
        result = st.session_state.agent.process(cleaned_text)

    response = result.get(
        "response",
        "抱歉，我刚刚没有整理出有效结果。你可以换一种方式描述你的旅行需求。"
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.session_state.queries += 1


def render_chat():
    parts = []

    parts.append('<div class="vessel-wrap"><div class="vessel">')

    if not st.session_state.messages:
        parts.append(
            '<div class="empty-mute"><div class="empty-card">'
            '<div class="empty-icon">✦</div>'
            '<div class="empty-title">开始一场有质感的旅行</div>'
            '<div class="empty-desc">告诉我目的地、天数、预算、同行人和偏好，壳壳会为你整理一份清晰、松弛、可执行的旅行方案。</div>'
            '</div></div>'
        )
    else:
        for msg in st.session_state.messages:
            role = msg.get("role", "")
            content = safe_html(msg.get("content", ""))

            if role == "user":
                parts.append(
                    f'<div class="msg msg-user"><div class="bbl">{content}</div></div>'
                )
            else:
                parts.append(
                    f'<div class="msg msg-assist"><div class="assist-avatar">✦</div><div><div class="meta">壳壳</div><div class="bbl">{content}</div></div></div>'
                )

    parts.append('</div></div>')

    st.html("".join(parts))


def main():
    init()
    sidebar()

    st.markdown("""
    <div class="hero">
        <h1>壳壳</h1>
        <div class="brand-kicker">
            <span class="brand-dot"></span>
            Intelligent Travel Planning
        </div>
        <p class="sub">
            一位懂审美、懂预算、也懂节奏的私人旅行顾问，
            为你规划<strong>更从容、更精致、更好执行</strong>的旅程。
        </p>
        <div class="hero-line"></div>
    </div>
    """, unsafe_allow_html=True)

    render_chat()

    st.markdown('<div class="input-gap"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([6.2, 0.9], gap="small")

    with col1:
        user_input = st.text_input(
            "输入",
            placeholder="例如：成都三日，父母同行，预算3000，不吃辣...",
            label_visibility="collapsed",
            key="input_box"
        )

    with col2:
        send = st.button("发送", use_container_width=True)

    if send and user_input:
        process_input(user_input)
        st.rerun()

    if "pending" in st.session_state and st.session_state.pending:
        pending_text = st.session_state.pending
        st.session_state.pending = ""
        process_input(pending_text)
        st.rerun()


if __name__ == "__main__":
    main()
