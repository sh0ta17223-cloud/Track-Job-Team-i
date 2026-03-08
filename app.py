import streamlit as st

# ── ページ設定 ──
st.set_page_config(
    page_title="OfficeMeet",
    page_icon="🏢",
    layout="centered",
)

# ── カスタムCSS ──
st.markdown("""
<style>
  /*フォントの設定*/ 
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Noto Sans JP', sans-serif;
  }

  /* 背景 */
  .stApp {
    background-color: #F0F4FF;
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
    width: 38px; height: 38px;
    display: inline-flex;
    align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.85rem;
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

  /* プレースホルダー */
  .placeholder {
    background: white;
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    color: #999;
    margin-top: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  }
  .placeholder h2 { color: #333; margin: 0.75rem 0 0.5rem; font-size: 1.1rem; }
  .placeholder p  { font-size: 0.85rem; line-height: 1.7; }
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

# ── 各画面（中身はこれから作る） ──

with tab_home:
    st.markdown("""
    <div class="placeholder">
      <div style="font-size:2.5rem">🏠</div>
      <h2>ホーム画面</h2>
      <p>ステップ2で作成します。<br>出社メンバーの一覧がここに表示されます。</p>
    </div>
    """, unsafe_allow_html=True)

with tab_register:
    st.markdown("""
    <div class="placeholder">
      <div style="font-size:2.5rem">📅</div>
      <h2>出社登録画面</h2>
      <p>ステップ3で作成します。<br>カレンダーで複数日を選んで出社予定を登録できます。</p>
    </div>
    """, unsafe_allow_html=True)

with tab_profile:
    st.title("プロフィール設定")

    left, right = st.columns([2, 1])

    with left:
        st.subheader("プロフィール登録")

        with st.container(border=True):
            name = st.text_input("名前")
            dept = st.text_input("部署")
            color = st.color_picker("アバターカラー", "#D96A2B")

            tags = st.pills(
                "デフォルトの目的タグ（出社登録時に自動選択）",
                ["📦 ランチ可能", "💬 雑談歓迎", "🎯 作業メイン", "☕ コーヒー休憩"],
                selection_mode="multi",
                default=["💬 雑談歓迎"]
            )

            if st.button("保存", width="stretch"):
                st.success("保存しました")

    avatar_text = name[0] if name else "？"

    with right:
        st.subheader("プレビュー")

        html = f"""
<div style="
    border: 1px solid #d1d5db;
    border-radius: 16px;
    padding: 24px;
    background-color: #f9fafb;
">
    <div style="
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background-color: {color};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 56px;
        font-weight: bold;
        color: white;
        margin: 0 auto 24px auto;
    ">
        {avatar_text}
    </div>
    <p style="font-size: 18px; margin: 12px 0;">
        <strong>名前:</strong> {name if name else "未入力"}
    </p>
    <p style="font-size: 18px; margin: 12px 0;">
        <strong>部署:</strong> {dept if dept else "未入力"}
    </p>
    <p style="font-size: 18px; margin: 12px 0;">
        <strong>タグ:</strong> {", ".join(tags) if tags else "未選択"}
    </p>
</div>
"""
        st.markdown(html, unsafe_allow_html=True)
