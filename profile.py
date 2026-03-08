import streamlit as st
from storage import save_profile
from db import save_profile


def render_profile():
    st.title("プロフィール設定")

    profile = st.session_state.profile

    left, right = st.columns([2, 1])

    with left:
        st.subheader("プロフィール登録")

        with st.container(border=True):
            name = st.text_input("名前", value=profile["name"])
            dept = st.text_input("部署", value=profile["dept"])
            color = st.color_picker("アバターカラー", profile["color"])

            tags = st.pills(
                "デフォルトの目的タグ（出社登録時に自動選択）",
                ["📦 ランチ可能", "💬 雑談歓迎", "🎯 作業メイン", "☕ コーヒー休憩"],
                selection_mode="multi",
                default=profile["tags"]
            )

            if st.button("保存", use_container_width=True):
                st.session_state.profile = {
                    "name": name,
                    "dept": dept,
                    "color": color,
                    "tags": tags
                }
                save_profile(st.session_state.profile)
                st.success("保存しました")
                st.rerun()

    current = st.session_state.profile
    avatar_text = current["name"][0] if current["name"] else "？"

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
        background-color: {current["color"]};
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
        <strong>名前:</strong> {current["name"] if current["name"] else "未入力"}
    </p>
    <p style="font-size: 18px; margin: 12px 0;">
        <strong>部署:</strong> {current["dept"] if current["dept"] else "未入力"}
    </p>
    <p style="font-size: 18px; margin: 12px 0;">
        <strong>タグ:</strong> {", ".join(current["tags"]) if current["tags"] else "未選択"}
    </p>
</div>
"""
        st.markdown(html, unsafe_allow_html=True)