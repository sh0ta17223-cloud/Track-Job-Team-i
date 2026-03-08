import streamlit as st
from home import render_home
from register import render_register
from profile import render_profile

# ── ページ設定 ──
st.set_page_config(
    page_title="OfficeMeet",
    page_icon="🏢",
    layout="centered",
)

# ── カスタムCSS ──
st.markdown("""
<style>
  /* フォント */
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Noto Sans JP', sans-serif;
  }

  /* 背景 */
  .stApp {
    background-color: #F0F4FF;
  }

  /* 日付ボタンの改行を有効化 */
  div[data-testid="stHorizontalBlock"] button {
    white-space: pre-line !important;
    line-height: 1.4 !important;
    word-break: keep-all !important;
    overflow-wrap: normal !important;
  }

  div[data-testid="stHorizontalBlock"] button p {
    white-space: pre-line !important;
    word-break: keep-all !important;
    overflow-wrap: normal !important;
    margin: 0 !important;
  }

  /* ヘッダー */
  .app-header {
    background: linear-gradient(135deg, #4A90D9 0%, #5B6EE8 100%);
    padding: 1rem 1.5rem;
    border-radius: 0 0 20px 20px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .app-logo {
    font-size: 1.3rem;
    font-weight: 700;
    color: white;
    letter-spacing: 0.02em;
  }
  .app-logo span { color: #FFE066; }
  .header-sub {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.8);
    margin-top: 0.2rem;
  }
  .user-badge {
    background: white;
    color: #4A90D9;
    border-radius: 50%;
    width: 38px;
    height: 38px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }

  /* タブ */
  .stTabs [data-baseweb="tab-list"] {
    background-color: white;
    border-radius: 40px;
    padding: 0.3rem;
    gap: 0.2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }
  .stTabs [data-baseweb="tab"] {
    font-family: 'Noto Sans JP', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    color: #888;
    border-radius: 30px;
    padding: 0.45rem 1.1rem;
    border: none;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4A90D9, #5B6EE8) !important;
    color: white !important;
  }
  .stTabs [data-baseweb="tab-highlight"] { display: none; }
  .stTabs [data-baseweb="tab-border"]    { display: none; }

  /* 共通 */
  .section-title {
    font-weight: 700;
    font-size: 1rem;
    color: #333;
    margin: 0.75rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .member-count {
    background: #4A90D9;
    color: white;
    border-radius: 20px;
    padding: 0.1rem 0.55rem;
    font-size: 0.72rem;
    font-weight: 700;
  }
  .tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    margin-top: 0.4rem;
  }
  .tag-chip {
    font-size: 0.68rem;
    padding: 0.18rem 0.55rem;
    border-radius: 20px;
    font-weight: 500;
  }
  .empty-state {
    text-align: center;
    padding: 2.5rem 1rem;
    color: #aaa;
    background: white;
    border-radius: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  }
  .empty-state p {
    font-size: 0.85rem;
    line-height: 1.7;
    margin-top: 0.5rem;
  }
  .placeholder {
    background: white;
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    color: #999;
    margin-top: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  }
  .placeholder h2 {
    color: #333;
    margin: 0.75rem 0 0.5rem;
    font-size: 1.1rem;
  }
  .placeholder p {
    font-size: 0.85rem;
    line-height: 1.7;
  }
</style>
""", unsafe_allow_html=True)

# ── ヘッダー ──
st.markdown("""
<div class="app-header">
  <div>
    <div class="app-logo">🏢 Office<span>Meet</span></div>
    <div class="header-sub">いっしょに出社マッチングサービス</div>
  </div>
  <div class="user-badge">田</div>
</div>
""", unsafe_allow_html=True)

# ── ナビゲーションタブ ──
tab_home, tab_register, tab_profile = st.tabs([
    "🏠 ホーム",
    "📅 出社登録",
    "👤 プロフィール",
])

with tab_home:
    render_home()

with tab_register:
    render_register()

with tab_profile:
    render_profile()