import streamlit as st

# 基本設定
st.set_page_config(
    page_title="OfficeMeet",
    page_icon="🏢",
    layout="wide"
)

if "prifile" not in st.session_state:
    st.session_state.profile={
        "neme":"あなた",
        "department":"営業部",
        "avatar_color":
    }