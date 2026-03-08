import streamlit as st
import calendar
from datetime import date


def render_register():
    today = date.today()
    year = today.year
    month = today.month

    if "selected_dates" not in st.session_state:
        st.session_state.selected_dates = []

    if "attendance_list" not in st.session_state:
        st.session_state.attendance_list = []

    time_options = [f"{h:02d}:00" for h in range(9, 22)]

    if "start_time" not in st.session_state:
        st.session_state.start_time = "09:00"

    if "end_time" not in st.session_state:
        st.session_state.end_time = "17:00"

    if "tags_widget_key" not in st.session_state:
        st.session_state.tags_widget_key = 0

    def toggle_date(d):
        if d in st.session_state.selected_dates:
            st.session_state.selected_dates.remove(d)
        else:
            st.session_state.selected_dates.append(d)
        st.session_state.selected_dates.sort()

    def register_attendance(start_time, end_time, tags):
        for d in st.session_state.selected_dates:
            st.session_state.attendance_list.append({
                "date": d,
                "start": start_time,
                "end": end_time,
                "tags": tags
            })
        st.session_state.selected_dates = []
        st.session_state.tags_widget_key += 1

    def delete_attendance(index):
        del st.session_state.attendance_list[index]

    st.title("出社登録")

    with st.container(border=True):
        st.subheader("📅 出社日を選ぶ")
        st.markdown(f"### {year}年 {month}月")
        st.caption("複数日選択可")

        weekdays = ["日", "月", "火", "水", "木", "金", "土"]
        cols = st.columns(7)
        for i, w in enumerate(weekdays):
            cols[i].markdown(
                f"<div style='text-align:center; font-weight:bold;'>{w}</div>",
                unsafe_allow_html=True
            )

        cal = calendar.Calendar(firstweekday=6)
        weeks = cal.monthdatescalendar(year, month)

        for week in weeks:
            cols = st.columns(7)
            for i, d in enumerate(week):
                in_month = d.month == month
                selected = d in st.session_state.selected_dates

                with cols[i]:
                    if in_month:
                        if st.button(
                            str(d.day),
                            key=f"day_{d}",
                            use_container_width=True,
                            type="primary" if selected else "secondary"
                        ):
                            toggle_date(d)
                            st.rerun()
                    else:
                        st.markdown("<div style='height:38px;'></div>", unsafe_allow_html=True)

        st.markdown("### 選択中の日付")
        if st.session_state.selected_dates:
            selected_text = " / ".join(
                [f"{d.month}月{d.day}日" for d in st.session_state.selected_dates]
            )
            st.write(selected_text)
        else:
            st.info("日付を選択してください")

        st.divider()

        st.subheader("⏰ 時間帯・目的タグを設定")

        col1, col2 = st.columns(2)

        with col1:
            start_time = st.selectbox(
                "開始時間",
                time_options,
                key="start_time"
            )

        start_index = time_options.index(start_time)
        end_options = time_options[start_index + 1:]

        if st.session_state.end_time not in end_options:
            st.session_state.end_time = end_options[0]

        with col2:
            end_time = st.selectbox(
                "終了時間",
                end_options,
                key="end_time"
            )

        tags = st.pills(
            "目的タグ",
            ["📦 ランチ可能", "💬 雑談歓迎", "🎯 作業メイン", "☕ コーヒー休憩"],
            selection_mode="multi",
            key=f"tags_{st.session_state.tags_widget_key}"
        )

        if st.button("登録する", type="primary"):
            if not st.session_state.selected_dates:
                st.warning("日付を選択してください")
            elif start_time >= end_time:
                st.warning("終了時間は開始時間より後にしてください")
            else:
                register_attendance(start_time, end_time, tags)
                st.success("登録しました")
                st.rerun()

    st.markdown("## 登録済み予定")

    if st.session_state.attendance_list:
        for i, item in enumerate(st.session_state.attendance_list):
            tags_text = " / ".join(item["tags"]) if item["tags"] else "タグなし"

            col1, col2 = st.columns([8, 1])

            with col1:
                st.write(
                    f"{item['date'].strftime('%Y/%m/%d')}　{item['start']} - {item['end']}　{tags_text}"
                )

            with col2:
                if st.button("削除", key=f"delete_{i}"):
                    delete_attendance(i)
                    st.rerun()
    else:
        st.info("まだ予定はありません")