import streamlit as st
from data import TAG_OPTIONS, get_profile, init_data, save_profile


def render_profile():
    init_data()
    profile = get_profile()

    st.title("プロフィール設定")

    left, right = st.columns([2, 1])

    with left:
        st.subheader("プロフィール登録")

        with st.container(border=True):
            name = st.text_input("名前", value=profile["name"])
            dept = st.text_input("部署", value=profile["dept"])
            color = st.color_picker("アバターカラー", value=profile["color"])

            tags = st.pills(
                "デフォルトの目的タグ（出社登録時に自動選択）",
                TAG_OPTIONS,
                selection_mode="multi",
                default=profile["tags"],
            )

            if st.button("保存", width="stretch"):
                if not name.strip() or not dept.strip() or not tags:
                    st.warning("すべての項目を入力してから保存してください。")
                else:
                    save_profile(name, dept, color, tags)
                    st.success("プロフィールを保存しました")

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
