import streamlit as st

st.title("プロフィール設定")

left, right = st.columns([2, 1])

with left:
    with st.form("プロフィール登録"):
        name = st.text_input("名前")
        dept = st.text_input("部署")
        color = st.color_picker("アバターカラー", "#D96A2B")
        tags = st.multiselect("デフォルトタグ", ["会議", "雑談", "相談", "ランチ"])
        submitted = st.form_submit_button("保存")

        if submitted:
            st.success("保存しました")

# 名前の先頭1文字をアイコン文字にする
avatar_text = name[0] if name else "？"

with right:
    st.subheader("プレビュー")

    st.markdown(
        f"""
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
            margin-bottom: 16px;
        ">
            {avatar_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("名前:", name if name else "未入力")
    st.write("部署:", dept if dept else "未入力")
    st.write("タグ:", ", ".join(tags) if tags else "未選択")