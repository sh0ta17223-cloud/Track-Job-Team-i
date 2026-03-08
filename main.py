import streamlit as st
from datetime import date, timedelta
import calendar

# ── ページ設定 ──
st.set_page_config(page_title="OfficeMeet", page_icon="🏢", layout="centered")

# ── 定数 ──
today     = date.today()
tomorrow  = today + timedelta(days=1)
day_after = today + timedelta(days=2)
DAY_JA    = ["月", "火", "水", "木", "金", "土", "日"]

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
ALL_TAGS     = list(TAG_COLORS.keys())
TIME_OPTIONS = ["08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00"]

# ── セッション初期化 ──
if "selected_date"  not in st.session_state: st.session_state.selected_date  = today
if "cal_year"       not in st.session_state: st.session_state.cal_year       = today.year
if "cal_month"      not in st.session_state: st.session_state.cal_month      = today.month
if "selected_dates" not in st.session_state: st.session_state.selected_dates = []
if "my_schedules"   not in st.session_state: st.session_state.my_schedules   = []
# プロフィール
if "profile_name"   not in st.session_state: st.session_state.profile_name   = ""
if "profile_dept"   not in st.session_state: st.session_state.profile_dept   = ""
if "profile_color"  not in st.session_state: st.session_state.profile_color  = "#D96A2B"
if "profile_tags"   not in st.session_state: st.session_state.profile_tags   = []

# ── CSS ──
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');
  html, body, [class*="css"] { font-family: 'Noto Sans JP', sans-serif; }
  .stApp { background-color: #F0F4FF; }

  .app-header {
    background: linear-gradient(135deg,#4A90D9,#5B6EE8);
    padding: 1rem 1.5rem; border-radius: 0 0 20px 20px;
    margin-bottom: 1.5rem;
    display: flex; align-items: center; justify-content: space-between;
  }
  .app-logo { font-size:1.3rem; font-weight:700; color:white; }
  .app-logo span { color:#FFE066; }
  .header-sub { font-size:0.75rem; color:rgba(255,255,255,0.8); margin-top:0.2rem; }
  .user-badge {
    border-radius:50%; width:38px; height:38px; display:inline-flex;
    align-items:center; justify-content:center;
    font-weight:700; font-size:0.85rem;
    box-shadow:0 2px 8px rgba(0,0,0,0.15);
  }

  /* ナビタブ */
  .stTabs [data-baseweb="tab-list"] {
    background-color:white; border-radius:40px;
    padding:0.3rem; gap:0.2rem; box-shadow:0 2px 8px rgba(0,0,0,0.08);
  }
  .stTabs [data-baseweb="tab"] {
    font-family:'Noto Sans JP',sans-serif; font-weight:600;
    font-size:0.85rem; color:#888; border-radius:30px; padding:0.45rem 1.1rem; border:none;
  }
  .stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#4A90D9,#5B6EE8) !important; color:white !important;
  }
  .stTabs [data-baseweb="tab-highlight"],
  .stTabs [data-baseweb="tab-border"] { display:none; }

  /* 日付ボタン共通 */
  div[data-testid="stHorizontalBlock"] button {
    border-radius:40px !important; padding:0.4rem 0.2rem !important;
    font-size:0.82rem !important; font-family:'Noto Sans JP',sans-serif !important;
    line-height:1.5 !important; white-space:pre-wrap !important;
    min-height:52px !important; border:2px solid #E0E8FF !important;
    background:white !important; color:#333 !important;
    box-shadow:0 1px 4px rgba(0,0,0,0.06) !important;
  }
  div[data-testid="stHorizontalBlock"] button:hover {
    border-color:#4A90D9 !important; background:#F0F6FF !important;
  }

  .section-title {
    font-weight:700; font-size:1rem; color:#333;
    margin:0.75rem 0; display:flex; align-items:center; gap:0.5rem;
  }
  .member-count {
    background:#4A90D9; color:white; border-radius:20px;
    padding:0.1rem 0.55rem; font-size:0.72rem; font-weight:700;
  }
  .tag-row { display:flex; flex-wrap:wrap; gap:0.3rem; margin-top:0.4rem; }
  .tag-chip { font-size:0.68rem; padding:0.18rem 0.55rem; border-radius:20px; font-weight:500; }

  .chip-wrap { display:flex; flex-wrap:wrap; gap:0.4rem; margin:0.5rem 0 1rem; min-height:32px; }
  .chip {
    display:inline-flex; align-items:center; gap:0.3rem;
    background:#1A1714; color:white; border-radius:20px;
    padding:0.25rem 0.75rem; font-size:0.75rem; font-weight:600;
  }
  .chip-hint { font-size:0.8rem; color:#aaa; font-style:italic; padding:0.25rem 0; }

  .reg-card {
    background:white; border-radius:14px; padding:0.85rem 1rem;
    margin-bottom:0.6rem; box-shadow:0 1px 6px rgba(0,0,0,0.06);
    border-left:4px solid #4A7C6F;
  }
  .reg-date { font-weight:700; font-size:0.88rem; }
  .reg-time { font-size:0.75rem; color:#888; }

  .empty-state {
    text-align:center; padding:2.5rem 1rem; color:#aaa;
    background:white; border-radius:20px; box-shadow:0 2px 10px rgba(0,0,0,0.05);
  }
  .empty-state p { font-size:0.85rem; line-height:1.7; margin-top:0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── ヘッダー（プロフィール情報を反映） ──
badge_initial = st.session_state.profile_name[0] if st.session_state.profile_name else "？"
badge_color   = st.session_state.profile_color
st.markdown(f"""
<div class="app-header">
  <div>
    <div class="app-logo">🏢 Office<span>Meet</span></div>
    <div class="header-sub">いっしょに出社マッチングサービス</div>
  </div>
  <div class="user-badge" style="background:{badge_color};color:white">{badge_initial}</div>
</div>
""", unsafe_allow_html=True)

# ── ナビタブ ──
tab_home, tab_register, tab_profile = st.tabs(["🏠 ホーム", "📅 出社登録", "👤 プロフィール"])


# ══════════════════════════════════════════
#  ホーム画面
# ══════════════════════════════════════════
with tab_home:
    dates = [today + timedelta(days=i) for i in range(14)]

    cols = st.columns(len(dates))
    for i, d in enumerate(dates):
        dow = DAY_JA[d.weekday()]
        is_active = d == st.session_state.selected_date
        if is_active:
            st.markdown(f"""<style>
            div[data-testid="stHorizontalBlock"] > div:nth-child({i+1}) button {{
                background:linear-gradient(135deg,#4A90D9,#5B6EE8) !important;
                color:white !important; border-color:transparent !important; font-weight:700 !important;
            }}</style>""", unsafe_allow_html=True)
        with cols[i]:
            if st.button(f"{d.day}\n{dow}", key=f"home_date_{i}", use_container_width=True):
                st.session_state.selected_date = d
                st.rerun()

    sel = st.session_state.selected_date
    dow_label = DAY_JA[sel.weekday()]

    my_today = [
        {"name": st.session_state.profile_name or "あなた",
         "dept": st.session_state.profile_dept or "—",
         "date": s["date"], "start": s["start"], "end": s["end"],
         "tags": s["tags"], "color": st.session_state.profile_color, "emoji": "🙋"}
        for s in st.session_state.my_schedules if s["date"] == sel
    ]
    day_members = my_today + [m for m in MEMBERS if m["date"] == sel]

    st.markdown(f"""<div class="section-title">
      {sel.month}月{sel.day}日({dow_label})の出社メンバー
      <span class="member-count">{len(day_members)}人</span>
    </div>""", unsafe_allow_html=True)

    if not day_members:
        st.markdown("""<div class="empty-state">
          <div style="font-size:2.5rem">🏢</div>
          <p>この日の出社予定者はまだいません。<br>「出社登録」タブから予定を追加しましょう！</p>
        </div>""", unsafe_allow_html=True)
    else:
        for m in day_members:
            tags_html = "".join([
                f'<span class="tag-chip" style="background:{TAG_COLORS[t]["bg"]};color:{TAG_COLORS[t]["color"]}">{t}</span>'
                for t in m["tags"] if t in TAG_COLORS
            ])
            with st.expander(f'{m["emoji"]}  {m["name"]}　{m["start"]} – {m["end"]}'):
                st.markdown(f"""<div style="padding:0.25rem 0">
                  <div style="font-size:0.82rem;color:#888;margin-bottom:0.3rem">{m["dept"]}</div>
                  <div style="font-size:0.9rem;margin-bottom:0.5rem">🕐 {m["start"]} – {m["end"]}</div>
                  <div class="tag-row">{tags_html}</div>
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════
#  出社登録画面
# ══════════════════════════════════════════
with tab_register:

    y, m = st.session_state.cal_year, st.session_state.cal_month

    c_prev, c_mid, c_next = st.columns([1, 4, 1])
    with c_prev:
        if st.button("‹", key="cal_prev"):
            if m == 1: st.session_state.cal_year -= 1; st.session_state.cal_month = 12
            else:      st.session_state.cal_month -= 1
            st.rerun()
    with c_mid:
        st.markdown(f"<div style='text-align:center;font-weight:700;font-size:1rem;padding:0.4rem'>{y}年 {m}月</div>", unsafe_allow_html=True)
    with c_next:
        if st.button("›", key="cal_next"):
            if m == 12: st.session_state.cal_year += 1; st.session_state.cal_month = 1
            else:       st.session_state.cal_month += 1
            st.rerun()

    day_names_cal = ["月", "火", "水", "木", "金", "土", "日"]
    day_cols = st.columns(7)
    for ci, dn in enumerate(day_names_cal):
        with day_cols[ci]:
            color = "#E74C3C" if dn == "日" else "#3A85C8" if dn == "土" else "#888"
            st.markdown(f"<div style='text-align:center;font-size:0.72rem;font-weight:600;color:{color};padding:0.2rem 0'>{dn}</div>", unsafe_allow_html=True)

    first_weekday, num_days = calendar.monthrange(y, m)
    cells = [""] * first_weekday + list(range(1, num_days + 1))
    while len(cells) % 7 != 0:
        cells.append("")
    weeks = [cells[i:i+7] for i in range(0, len(cells), 7)]

    for week in weeks:
        wcols = st.columns(7)
        for ci, day_num in enumerate(week):
            with wcols[ci]:
                if day_num == "":
                    st.markdown("<div style='aspect-ratio:1'></div>", unsafe_allow_html=True)
                else:
                    d = date(y, m, day_num)
                    is_past     = d < today
                    is_today    = d == today
                    is_selected = d in st.session_state.selected_dates
                    if is_past:
                        st.markdown(f"<div style='text-align:center;color:#ccc;font-size:0.85rem;padding:0.5rem 0'>{day_num}</div>", unsafe_allow_html=True)
                    else:
                        if is_selected:
                            st.markdown(f"""<style>
                            div[data-testid="stHorizontalBlock"]:has(~ *) div:nth-child({ci+1}) button {{
                                background:linear-gradient(135deg,#4A90D9,#5B6EE8) !important;
                                color:white !important; border-color:transparent !important;
                            }}</style>""", unsafe_allow_html=True)
                        elif is_today:
                            st.markdown(f"""<style>
                            div[data-testid="stHorizontalBlock"]:has(~ *) div:nth-child({ci+1}) button {{
                                border-color:#4A90D9 !important; font-weight:700 !important;
                            }}</style>""", unsafe_allow_html=True)
                        if st.button(str(day_num), key=f"cal_{y}_{m}_{day_num}", use_container_width=True):
                            if d in st.session_state.selected_dates:
                                st.session_state.selected_dates.remove(d)
                            else:
                                st.session_state.selected_dates.append(d)
                            st.rerun()

    # 選択日付チップ
    st.markdown("**選択中の日付**")
    sel_dates = sorted(st.session_state.selected_dates)
    if not sel_dates:
        st.markdown("<div class='chip-hint'>カレンダーで日付をタップして選んでください</div>", unsafe_allow_html=True)
    else:
        chips_html = "<div class='chip-wrap'>" + "".join([
            f"<span class='chip'>📅 {d.month}月{d.day}日({DAY_JA[d.weekday()]})</span>"
            for d in sel_dates
        ]) + "</div>"
        st.markdown(chips_html, unsafe_allow_html=True)

    st.markdown("---")

    # 時間帯
    st.markdown("**⏰ 時間帯を設定**")
    col_s, col_e = st.columns(2)
    with col_s:
        start_time = st.selectbox("開始時間", TIME_OPTIONS, index=1, key="reg_start")
    with col_e:
        end_time = st.selectbox("終了時間", TIME_OPTIONS, index=8, key="reg_end")

    # タグ（プロフィールのデフォルトタグを初期値に）
    st.markdown("**🏷️ 目的タグを選択**")
    selected_tags = st.multiselect(
        label="タグ（複数選択可）",
        options=ALL_TAGS,
        default=st.session_state.profile_tags,
        key="reg_tags",
        label_visibility="collapsed",
    )

    # 登録ボタン
    if st.button("✅ 出社予定を登録する", use_container_width=True, type="primary"):
        if not sel_dates:
            st.error("日付を選択してください")
        elif start_time >= end_time:
            st.error("終了時間は開始時間より後にしてください")
        else:
            for d in sel_dates:
                st.session_state.my_schedules = [
                    s for s in st.session_state.my_schedules if s["date"] != d
                ]
                st.session_state.my_schedules.append({
                    "date": d, "start": start_time, "end": end_time, "tags": selected_tags,
                })
            st.session_state.selected_dates = []
            st.success(f"{len(sel_dates)}件の出社予定を登録しました 🎉")
            st.rerun()

    # 登録済み一覧
    my = sorted(st.session_state.my_schedules, key=lambda x: x["date"])
    if my:
        st.markdown("---")
        st.markdown(f"""<div class="section-title">登録済みの出社予定
          <span class="member-count">{len(my)}件</span>
        </div>""", unsafe_allow_html=True)
        for s in my:
            tags_html = "".join([
                f'<span class="tag-chip" style="background:{TAG_COLORS[t]["bg"]};color:{TAG_COLORS[t]["color"]}">{t}</span>'
                for t in s["tags"] if t in TAG_COLORS
            ])
            d_label = f"{s['date'].month}月{s['date'].day}日({DAY_JA[s['date'].weekday()]})"
            col_info, col_del = st.columns([5, 1])
            with col_info:
                st.markdown(f"""<div class="reg-card">
                  <div class="reg-date">📅 {d_label}</div>
                  <div class="reg-time">🕐 {s['start']} – {s['end']}</div>
                  <div class="tag-row" style="margin-top:0.3rem">{tags_html}</div>
                </div>""", unsafe_allow_html=True)
            with col_del:
                if st.button("🗑️", key=f"del_{s['date']}", help="削除"):
                    st.session_state.my_schedules = [
                        x for x in st.session_state.my_schedules if x["date"] != s["date"]
                    ]
                    st.rerun()


# ══════════════════════════════════════════
#  プロフィール設定画面（ステップ4）
# ══════════════════════════════════════════
with tab_profile:

    st.title("プロフィール設定")

    left, right = st.columns([2, 1])

    # ── a･b･c･d. 入力フォーム ──
    with left:
        st.subheader("プロフィール登録")
        with st.container(border=True):
            name  = st.text_input("名前",  value=st.session_state.profile_name, placeholder="例：田中 太郎")
            dept  = st.text_input("部署",  value=st.session_state.profile_dept, placeholder="例：エンジニアリング部")
            color = st.color_picker("アバターカラー", value=st.session_state.profile_color)

            tags = st.pills(
                "デフォルトの目的タグ（出社登録時に自動選択）",
                ALL_TAGS,
                selection_mode="multi",
                default=st.session_state.profile_tags,
            )

            # ── d. 保存ボタン ──
            if st.button("💾 保存する", use_container_width=True, type="primary"):
                if not name:
                    st.error("名前を入力してください")
                else:
                    st.session_state.profile_name  = name
                    st.session_state.profile_dept  = dept
                    st.session_state.profile_color = color
                    st.session_state.profile_tags  = list(tags)
                    st.success("プロフィールを保存しました ✅")
                    st.rerun()

    # ── e. カードプレビュー ──
    avatar_initial = name[0] if name else "？"
    with right:
        st.subheader("プレビュー")
        tags_preview = ", ".join(tags) if tags else "未選択"
        st.markdown(f"""
<div style="border:1px solid #d1d5db; border-radius:16px; padding:24px; background:#f9fafb;">
  <div style="width:80px; height:80px; border-radius:50%; background:{color};
              display:flex; align-items:center; justify-content:center;
              font-size:2rem; font-weight:bold; color:white; margin:0 auto 16px auto;">
    {avatar_initial}
  </div>
  <p style="font-size:1rem; margin:8px 0"><strong>名前：</strong>{name if name else "未入力"}</p>
  <p style="font-size:0.9rem; margin:8px 0; color:#666"><strong>部署：</strong>{dept if dept else "未入力"}</p>
  <p style="font-size:0.85rem; margin:8px 0; color:#666"><strong>タグ：</strong>{tags_preview}</p>
</div>
        """, unsafe_allow_html=True)