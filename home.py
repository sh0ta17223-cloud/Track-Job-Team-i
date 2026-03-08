import streamlit as st
from datetime import date, timedelta
from db import get_attendances


def render_home():
    today = date.today()

    TAG_COLORS = {
        "📦 ランチ可能":   {"bg": "#FFF0E6", "color": "#C05A20"},
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

    # DBから最新の出社予定を取得
    attendance_list = get_attendances()
    day_members = [m for m in attendance_list if m["date"] == sel]
    dow_label = DAY_JA[sel.weekday()]

    st.markdown(
        f"""
        <div class="section-title">
          {sel.month}月{sel.day}日({dow_label})の出社メンバー
          <span class="member-count">{len(day_members)}人</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not day_members:
        st.markdown(
            """
            <div class="empty-state">
              <div style="font-size:2.5rem">🏢</div>
              <p>この日の出社予定者はまだいません。<br>「出社登録」タブから予定を追加しましょう！</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for m in day_members:
            tags_html = "".join([
                f'<span class="tag-chip" style="background:{TAG_COLORS[t]["bg"]};color:{TAG_COLORS[t]["color"]}">{t}</span>'
                for t in m["tags"] if t in TAG_COLORS
            ])

            avatar_text = m["name"][0] if m["name"] else "？"
            avatar_color = m.get("color", "#4A90D9")

            with st.expander(f'{avatar_text}  {m["name"]}　{m["start"]} – {m["end"]}'):
                st.markdown(
                    f"""
                    <div style="padding:0.25rem 0">
                      <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.5rem;">
                        <div style="
                            width:40px;
                            height:40px;
                            border-radius:50%;
                            background:{avatar_color};
                            color:white;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            font-weight:700;
                            font-size:1rem;
                            flex-shrink:0;
                        ">
                            {avatar_text}
                        </div>
                        <div>
                          <div style="font-size:0.95rem; font-weight:700; color:#222;">{m["name"]}</div>
                          <div style="font-size:0.82rem; color:#888;">{m["dept"]}</div>
                        </div>
                      </div>
                      <div style="font-size:0.9rem; margin-bottom:0.5rem;">🕐 {m["start"]} – {m["end"]}</div>
                      <div class="tag-row">{tags_html}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )