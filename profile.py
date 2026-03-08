import streamlit as st


def render_profile():
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