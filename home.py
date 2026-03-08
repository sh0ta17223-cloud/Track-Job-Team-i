import streamlit as st
from datetime import date, timedelta


def render_home():
    # ── サンプルデータ ──
    today = date.today()
    tomorrow = today + timedelta(days=1)
    day_after = today + timedelta(days=2)

    MEMBERS = [
        {"id": 1, "name": "山田 優子", "dept": "マーケティング部", "date": today,     "start": "10:00", "end": "18:00", "tags": ["🍱 ランチ可能", "💬 雑談歓迎"],    "color": "#4A90D9", "emoji": "👩"},
        {"id": 2, "name": "鈴木 健太", "dept": "エンジニアリング", "date": today,     "start": "09:00", "end": "17:00", "tags": ["🎯 作業メイン"],                   "color": "#4A7C6F", "emoji": "👨"},
        {"id": 3, "name": "高橋 美咲", "dept": "デザイン部",       "date": today,     "start": "11:00", "end": "19:00", "tags": ["🍱 ランチ可能", "☕ コーヒー休憩"], "color": "#7B5EA7", "emoji": "👩"},
        {"id": 4, "name": "中村 大輔", "dept": "営業部",           "date": today,     "start": "09:00", "end": "16:00", "tags": ["💬 雑談歓迎"],                    "color": "#C8873A", "emoji": "👨"},
        {"id": 5, "name": "佐藤 花子", "dept": "人事部",           "date": tomorrow,  "start": "10:00", "end": "17:00", "tags": ["☕ コーヒー休憩", "💬 雑談歓迎"],  "color": "#2E6E8A", "emoji": "👩"},
        {"id": 6, "name": "伊藤 誠",   "dept": "経営企画",         "date": day_after, "start": "09:00", "end": "18:00", "tags": ["🎯 作業メイン", "🍱 ランチ可能"],  "color": "#8A4F4F", "emoji": "👨"},
    ]

    TAG_COLORS = {
        "🍱 ランチ可能":   {"bg": "#FFF0E6", "color": "#C05A20"},
        "💬 雑談歓迎":    {"bg": "#E8F4F0", "color": "#2E6E5F"},
        "🎯 作業メイン":  {"bg": "#F0EDF8", "color": "#5A4A88"},
        "☕ コーヒー休憩": {"bg": "#FFF8E6", "color": "#8B6914"},
    }

    DAY_JA = ["月", "火", "水", "木", "金", "土", "日"]

    if "selected_date" not in st.session_state:
        st.session_state.selected_date = today

    dates = [today + timedelta(days=i) for i in range(7)]

    cols = st.columns(7)
    for i, d in enumerate(dates):
        dow = DAY_JA[d.weekday()]
        is_active = d == st.session_state.selected_date

        with cols[i]:
            if st.button(
                f"{d.day}\n{dow}",
                key=f"date_{i}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.selected_date = d
                st.rerun()

    sel = st.session_state.selected_date
    day_members = [m for m in MEMBERS if m["date"] == sel]
    dow_label = DAY_JA[sel.weekday()]

    st.markdown(f"""
    <div class="section-title">
      {sel.month}月{sel.day}日({dow_label})の出社メンバー
      <span class="member-count">{len(day_members)}人</span>
    </div>
    """, unsafe_allow_html=True)

    if not day_members:
        st.markdown("""
        <div class="empty-state">
          <div style="font-size:2.5rem">🏢</div>
          <p>この日の出社予定者はまだいません。<br>「出社登録」タブから予定を追加しましょう！</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for m in day_members:
            tags_html = "".join([
                f'<span class="tag-chip" style="background:{TAG_COLORS[t]["bg"]};color:{TAG_COLORS[t]["color"]}">{t}</span>'
                for t in m["tags"] if t in TAG_COLORS
            ])

            with st.expander(f'{m["emoji"]}  {m["name"]}　{m["start"]} – {m["end"]}'):
                st.markdown(f"""
                <div style="padding:0.25rem 0">
                  <div style="font-size:0.82rem;color:#888;margin-bottom:0.3rem">{m["dept"]}</div>
                  <div style="font-size:0.9rem;margin-bottom:0.5rem">🕐 {m["start"]} – {m["end"]}</div>
                  <div class="tag-row">{tags_html}</div>
                </div>
                """, unsafe_allow_html=True)
