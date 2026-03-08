import json
import os
from datetime import date

PROFILE_FILE = "profile.json"
ATTENDANCE_FILE = "attendance.json"


def load_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "name": "",
        "dept": "",
        "color": "#D96A2B",
        "tags": ["💬 雑談歓迎"]
    }


def save_profile(profile):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def load_attendance():
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 文字列の日付を date 型に戻す
        for item in data:
            item["date"] = date.fromisoformat(item["date"])
        return data

    return []


def save_attendance(attendance_list):
    serializable = []
    for item in attendance_list:
        serializable.append({
            **item,
            "date": item["date"].isoformat()
        })

    with open(ATTENDANCE_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)