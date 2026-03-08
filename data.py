from __future__ import annotations

import streamlit as st

TAG_OPTIONS = ["🍱 ランチ可能", "💬 雑談歓迎", "🎯 作業メイン", "☕ コーヒー休憩"]


def init_data() -> None:
    if "profile" not in st.session_state:
        st.session_state.profile = {
            "name": "",
            "dept": "",
            "color": "#D96A2B",
            "tags": ["💬 雑談歓迎"],
        }

    if "attendance_list" not in st.session_state:
        st.session_state.attendance_list = []


def save_profile(name: str, dept: str, color: str, tags: list[str]) -> None:
    st.session_state.profile = {
        "name": name.strip(),
        "dept": dept.strip(),
        "color": color,
        "tags": list(tags),
    }


def get_profile() -> dict:
    init_data()
    return st.session_state.profile


def add_attendance(attendance_date, start_time: str, end_time: str, tags: list[str]) -> None:
    init_data()
    profile = get_profile()
    st.session_state.attendance_list.append(
        {
            "date": attendance_date,
            "start": start_time,
            "end": end_time,
            "tags": list(tags),
            "name": profile["name"],
            "dept": profile["dept"],
            "color": profile["color"],
            "profile_tags": list(profile["tags"]),
        }
    )


def delete_attendance(index: int) -> None:
    init_data()
    del st.session_state.attendance_list[index]


def get_attendance_list() -> list[dict]:
    init_data()
    return st.session_state.attendance_list
