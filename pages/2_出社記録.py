import json
import urllib.parse
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer

# ── データ ──
COLORS = ['#D4622A','#4A7C6F','#7B5EA7','#C8873A','#2E6E8A','#8A4F4F','#3A7ABF','#6B7A3A']

today_str  = date.today().isoformat()
my_schedules = []

# ── HTML ──
HTML = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OfficeMeet — 出社登録</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">
<style>
  :root{--bg:#F5F0E8;--surface:#FFFDF7;--ink:#1A1714;--muted:#7A7268;--accent:#D4622A;--accent2:#4A7C6F;--accent3:#C8A951;--border:#E0D9CC;--card-shadow:0 2px 16px rgba(26,23,20,0.09);}
  *{margin:0;padding:0;box-sizing:border-box;}
  body{font-family:'Noto Sans JP',sans-serif;background:var(--bg);color:var(--ink);min-height:100vh;}

  header{background:var(--ink);padding:0 1.5rem;display:flex;align-items:center;height:60px;}
  .logo{font-family:'DM Serif Display',serif;font-size:1.5rem;color:var(--bg);}
  .logo span{color:var(--accent3);font-style:italic;}

  main{max-width:680px;margin:0 auto;padding:2rem 1.5rem 5rem;}

  /* ── MY BOX ── */
  .my-box{background:var(--surface);border:1.5px solid var(--border);border-radius:20px;padding:1.5rem;margin-bottom:2rem;}
  .my-box-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:1.1rem;}
  .my-box-header h3{font-weight:700;font-size:0.95rem;}

  /* ── CALENDAR ── */
  .calendar-wrap{margin-bottom:1.25rem;}
  .cal-nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:0.75rem;}
  .cal-nav span{font-weight:700;font-size:0.95rem;}
  .cal-nav-btn{background:none;border:1.5px solid var(--border);border-radius:8px;width:30px;height:30px;cursor:pointer;font-size:1rem;display:flex;align-items:center;justify-content:center;transition:border-color 0.15s;}
  .cal-nav-btn:hover{border-color:var(--muted);}
  .cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;}
  .cal-day-name{text-align:center;font-size:0.68rem;color:var(--muted);font-weight:600;padding:0.25rem 0;}
  .cal-cell{aspect-ratio:1;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:0.82rem;cursor:pointer;border:1.5px solid transparent;transition:all 0.14s;position:relative;}
  .cal-cell:hover:not(.cal-empty):not(.cal-past){border-color:var(--accent2);background:#EAF4F1;}
  .cal-cell.cal-empty{cursor:default;}
  .cal-cell.cal-past{color:var(--border);cursor:default;}
  .cal-cell.cal-today{font-weight:700;border-color:var(--accent3);}
  .cal-cell.cal-selected{background:var(--ink);color:var(--bg);border-color:var(--ink);font-weight:700;}
  .cal-cell.cal-selected::after{content:'✓';position:absolute;top:1px;right:2px;font-size:0.5rem;color:var(--accent3);}

  /* ── SELECTED CHIPS ── */
  .sel-dates-wrap{margin-bottom:1rem;}
  .sel-dates-label{font-size:0.72rem;color:var(--muted);font-weight:500;letter-spacing:0.04em;text-transform:uppercase;margin-bottom:0.5rem;}
  .sel-dates-chips{display:flex;flex-wrap:wrap;gap:0.35rem;min-height:28px;}
  .sel-chip{display:flex;align-items:center;gap:0.3rem;padding:0.25rem 0.65rem;background:var(--ink);color:var(--bg);border-radius:20px;font-size:0.75rem;font-weight:600;}
  .sel-chip-remove{cursor:pointer;opacity:0.6;font-size:0.8rem;}
  .sel-chip-remove:hover{opacity:1;}
  .no-dates-hint{font-size:0.8rem;color:var(--muted);font-style:italic;}

  hr{border:none;border-top:1px solid var(--border);margin:1.5rem 0;}

  /* ── FORM ── */
  .form-row{display:flex;flex-wrap:wrap;gap:0.75rem;margin-bottom:1rem;}
  .form-group{display:flex;flex-direction:column;gap:0.3rem;flex:1;min-width:130px;}
  .form-group label{font-size:0.72rem;color:var(--muted);font-weight:500;letter-spacing:0.04em;text-transform:uppercase;}
  .form-group select{border:1.5px solid var(--border);border-radius:10px;padding:0.55rem 0.75rem;font-family:'Noto Sans JP',sans-serif;font-size:0.88rem;background:var(--bg);color:var(--ink);outline:none;transition:border-color 0.15s;}
  .form-group select:focus{border-color:var(--accent2);}

  /* ── TAG SELECTOR ── */
  .tag-selector{display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:1.1rem;}
  .tag-btn{padding:0.35rem 0.85rem;border-radius:20px;border:1.5px solid var(--border);font-family:'Noto Sans JP',sans-serif;font-size:0.8rem;cursor:pointer;background:var(--bg);color:var(--ink);transition:all 0.15s;font-weight:500;}
  .tag-btn.selected{background:var(--ink);color:var(--bg);border-color:var(--ink);}
  .tag-btn:hover:not(.selected){border-color:var(--muted);}

  /* ── BUTTON ── */
  .btn-primary{background:var(--accent);color:white;border:none;padding:0.65rem 1.8rem;border-radius:12px;font-family:'Noto Sans JP',sans-serif;font-weight:700;font-size:0.9rem;cursor:pointer;transition:opacity 0.15s,transform 0.1s;}
  .btn-primary:hover{opacity:0.88;}
  .btn-primary:active{transform:scale(0.97);}

  /* ── REGISTERED LIST ── */
  .section-head{display:flex;align-items:baseline;gap:0.75rem;margin-bottom:1.25rem;}
  .section-head h2{font-family:'DM Serif Display',serif;font-size:1.3rem;}
  .reg-list{display:flex;flex-direction:column;gap:0.6rem;margin-top:1rem;}
  .reg-item{display:flex;align-items:center;gap:0.85rem;padding:0.7rem 0.9rem;background:var(--bg);border-radius:12px;border:1.5px solid var(--border);}
  .reg-item-dot{width:8px;height:8px;border-radius:50%;background:var(--accent2);flex-shrink:0;}
  .reg-item-info{flex:1;}
  .reg-item-date{font-weight:700;font-size:0.88rem;}
  .reg-item-time{font-size:0.75rem;color:var(--muted);}
  .reg-item-tags{display:flex;flex-wrap:wrap;gap:0.25rem;margin-top:0.3rem;}
  .tag{font-size:0.68rem;padding:0.2rem 0.5rem;border-radius:20px;font-weight:500;}
  .tag.lunch{background:#FFF0E6;color:#C05A20;border:1px solid #F5C9B0;}
  .tag.chat{background:#E8F4F0;color:#2E6E5F;border:1px solid #A8D4C8;}
  .tag.focus{background:#F0EDF8;color:#5A4A88;border:1px solid #C8C0E8;}
  .tag.coffee{background:#FFF8E6;color:#8B6914;border:1px solid #E8D898;}
  .reg-del{background:none;border:1.5px solid var(--border);border-radius:8px;padding:0.25rem 0.6rem;font-size:0.75rem;cursor:pointer;color:var(--muted);transition:all 0.15s;font-family:'Noto Sans JP',sans-serif;}
  .reg-del:hover{border-color:#C05A20;color:#C05A20;}

  /* ── TOAST ── */
  .toast{position:fixed;bottom:1.5rem;left:50%;transform:translateX(-50%) translateY(80px);background:var(--ink);color:var(--bg);padding:0.75rem 1.5rem;border-radius:40px;font-size:0.88rem;font-weight:500;transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1);z-index:300;white-space:nowrap;}
  .toast.show{transform:translateX(-50%) translateY(0);}

  @media(max-width:600px){.form-row{flex-direction:column;}}
</style>
</head>
<body>

<header>
  <div class="logo">Office<span>Meet</span> <span style="font-family:'Noto Sans JP',sans-serif;font-size:0.9rem;color:var(--muted);font-style:normal;margin-left:0.5rem;">出社登録</span></div>
</header>

<main>
  <!-- 登録フォーム -->
  <div class="my-box">
    <div class="my-box-header">
      <h3>出社日を選ぶ</h3>
      <span style="font-size:0.78rem;color:var(--muted);">複数日選択可</span>
    </div>

    <div class="calendar-wrap">
      <div class="cal-nav">
        <button class="cal-nav-btn" onclick="calPrev()">‹</button>
        <span id="calMonthLabel"></span>
        <button class="cal-nav-btn" onclick="calNext()">›</button>
      </div>
      <div class="cal-grid" id="calGrid"></div>
    </div>

    <div class="sel-dates-wrap">
      <div class="sel-dates-label">選択中の日付</div>
      <div class="sel-dates-chips" id="selChips">
        <span class="no-dates-hint">カレンダーで日付をタップして選んでください</span>
      </div>
    </div>

    <hr>

    <div style="margin-bottom:0.8rem;font-size:0.88rem;font-weight:600;">時間帯・目的タグを設定</div>
    <div class="form-row">
      <div class="form-group">
        <label>開始時刻</label>
        <select id="inputStart">
          <option value="06:00">6:00</option>
          <option value="07:00">7:00</option>
          <option value="08:00">8:00</option>
          <option value="09:00" selected>9:00</option>
          <option value="10:00">10:00</option>
          <option value="11:00">11:00</option>
          <option value="12:00">12:00</option>
          <option value="13:00">13:00</option>
          <option value="14:00">14:00</option>
          <option value="15:00">15:00</option>
          <option value="16:00">16:00</option>
          <option value="17:00">17:00</option>
          <option value="18:00">18:00</option>
          <option value="19:00">19:00</option>
          <option value="20:00">20:00</option>
          <option value="21:00">21:00</option>
          <option value="22:00">22:00</option>
          <option value="23:00">23:00</option>
        </select>
      </div>
      <div class="form-group">
        <label>終了時刻</label>
        <select id="inputEnd">
          <option value="07:00">7:00</option>
          <option value="08:00">8:00</option>
          <option value="09:00">9:00</option>
          <option value="10:00">10:00</option>
          <option value="11:00">11:00</option>
          <option value="12:00">12:00</option>
          <option value="13:00">13:00</option>
          <option value="14:00">14:00</option>
          <option value="15:00">15:00</option>
          <option value="16:00">16:00</option>
          <option value="17:00" selected>17:00</option>
          <option value="18:00">18:00</option>
          <option value="19:00">19:00</option>
          <option value="20:00">20:00</option>
          <option value="21:00">21:00</option>
          <option value="22:00">22:00</option>
          <option value="23:00">23:00</option>
          <option value="24:00">24:00</option>
        </select>
      </div>
    </div>

    <div style="margin-bottom:0.55rem;font-size:0.72rem;color:var(--muted);font-weight:500;letter-spacing:0.04em;text-transform:uppercase;">目的タグ</div>
    <div class="tag-selector" id="tagSelector">
      <button class="tag-btn" data-tag="lunch"  onclick="toggleTag(this)">🍱 ランチ可能</button>
      <button class="tag-btn" data-tag="chat"   onclick="toggleTag(this)">💬 雑談歓迎</button>
      <button class="tag-btn" data-tag="focus"  onclick="toggleTag(this)">🎯 作業メイン</button>
      <button class="tag-btn" data-tag="coffee" onclick="toggleTag(this)">☕ コーヒー休憩</button>
    </div>

    <button class="btn-primary" onclick="registerSchedule()">登録する</button>
  </div>

  <!-- 登録済みリスト -->
  <div id="myRegisteredWrap" style="display:none">
    <div class="section-head">
      <h2>登録済みの出社予定</h2>
    </div>
    <div class="reg-list" id="regList"></div>
  </div>
</main>

<div class="toast" id="toast"></div>

<script>
const TAG_LABELS = {lunch:'🍱 ランチ可能', chat:'💬 雑談歓迎', focus:'🎯 作業メイン', coffee:'☕ コーヒー休憩'};
const today     = new Date(); today.setHours(0,0,0,0);
const todayStr  = today.toISOString().slice(0,10);
const disp = d => { const x=new Date(d+'T00:00:00'); return `${x.getMonth()+1}月${x.getDate()}日(${'日月火水木金土'[x.getDay()]})`; };

let selectedDates = [];
let selectedTags  = [];
let calYear  = today.getFullYear();
let calMonth = today.getMonth();

// ── カレンダー ──
function renderCalendar() {
  document.getElementById('calMonthLabel').textContent = `${calYear}年 ${calMonth+1}月`;
  const grid = document.getElementById('calGrid');
  grid.innerHTML = '';
  '日月火水木金土'.split('').forEach(n => {
    const el = document.createElement('div');
    el.className = 'cal-day-name'; el.textContent = n; grid.appendChild(el);
  });
  const first = new Date(calYear, calMonth, 1).getDay();
  const days  = new Date(calYear, calMonth+1, 0).getDate();
  for (let i=0; i<first; i++) {
    const el = document.createElement('div'); el.className='cal-cell cal-empty'; grid.appendChild(el);
  }
  for (let d=1; d<=days; d++) {
    const ds = `${calYear}-${String(calMonth+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    const isPast  = ds < todayStr;
    const isToday = ds === todayStr;
    const isSel   = selectedDates.includes(ds);
    let cls = 'cal-cell';
    if (isPast)  cls += ' cal-past';
    if (isToday) cls += ' cal-today';
    if (isSel)   cls += ' cal-selected';
    const el = document.createElement('div'); el.className=cls; el.textContent=d;
    if (!isPast) el.onclick = () => toggleCalDate(ds);
    grid.appendChild(el);
  }
}
function toggleCalDate(ds) {
  selectedDates = selectedDates.includes(ds)
    ? selectedDates.filter(d => d !== ds)
    : [...selectedDates, ds].sort();
  renderCalendar(); renderSelChips();
}
function calPrev() { calMonth--; if (calMonth<0){ calMonth=11; calYear--; } renderCalendar(); }
function calNext() { calMonth++; if (calMonth>11){ calMonth=0; calYear++; } renderCalendar(); }

// ── 選択日チップ ──
function renderSelChips() {
  const wrap = document.getElementById('selChips');
  if (!selectedDates.length) {
    wrap.innerHTML = '<span class="no-dates-hint">カレンダーで日付をタップして選んでください</span>';
    return;
  }
  wrap.innerHTML = selectedDates.map(d =>
    `<span class="sel-chip">${disp(d)}<span class="sel-chip-remove" onclick="removeSelDate('${d}')">✕</span></span>`
  ).join('');
}
function removeSelDate(d) { selectedDates = selectedDates.filter(x => x!==d); renderCalendar(); renderSelChips(); }

// ── タグ ──
function toggleTag(btn) {
  btn.classList.toggle('selected');
  const t = btn.dataset.tag;
  selectedTags = selectedTags.includes(t) ? selectedTags.filter(x=>x!==t) : [...selectedTags, t];
}

// ── 登録 ──
async function registerSchedule() {
  if (!selectedDates.length) { showToast('日付を選択してください'); return; }
  const start = document.getElementById('inputStart').value;
  const end   = document.getElementById('inputEnd').value;
  const res   = await fetch('/api/my_schedules', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({dates: selectedDates, start, end, tags: selectedTags})
  });
  const data = await res.json();
  if (data.error) { showToast(data.error); return; }
  selectedDates = []; renderCalendar(); renderSelChips(); loadRegList();
  showToast(`${data.count}件の出社予定を登録しました 🎉`);
}

// ── 登録済みリスト ──
async function loadRegList() {
  const res  = await fetch('/api/my_schedules');
  const list = await res.json();
  const wrap    = document.getElementById('myRegisteredWrap');
  const regList = document.getElementById('regList');
  if (!list.length) { wrap.style.display='none'; return; }
  wrap.style.display = 'block';
  regList.innerHTML = list.map(s => `
    <div class="reg-item">
      <div class="reg-item-dot"></div>
      <div class="reg-item-info">
        <div class="reg-item-date">${disp(s.date)}</div>
        <div class="reg-item-time">${s.start} – ${s.end}</div>
        <div class="reg-item-tags">${s.tags.map(t=>`<span class="tag ${t}">${TAG_LABELS[t]}</span>`).join('')}</div>
      </div>
      <button class="reg-del" onclick="deleteReg('${s.date}')">削除</button>
    </div>`).join('');
}
async function deleteReg(d) {
  await fetch(`/api/my_schedules/${d}`, {method: 'DELETE'});
  loadRegList(); showToast('登録を削除しました');
}

// ── トースト ──
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2500);
}

// ── 初期化 ──
// 開始時間が変わったら終了時間の選択肢を絞る
document.getElementById('inputStart').addEventListener('change', function () {
  const startVal = this.value;
  const endSel   = document.getElementById('inputEnd');
  Array.from(endSel.options).forEach(opt => {
    opt.disabled = opt.value <= startVal;
  });
  // 現在選択中の終了時間が無効になった場合、次の有効な選択肢に移動
  if (endSel.value <= startVal) {
    const next = Array.from(endSel.options).find(opt => opt.value > startVal);
    if (next) endSel.value = next.value;
  }
});
renderCalendar(); renderSelChips(); loadRegList();
</script>
</body>
</html>"""


# ── HTTPハンドラー ──
class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"  {self.command} {self.path}")

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, body: str):
        data = body.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)

    def _read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path   = parsed.path

        if path == '/':
            self._html(HTML)
        elif path == '/api/my_schedules':
            self._json(my_schedules)
        else:
            self.send_error(404)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        data = self._read_body()

        if path == '/api/my_schedules':
            dates = data.get('dates', [])
            start = data.get('start', '09:00')
            end   = data.get('end',   '17:00')
            tags  = data.get('tags',  [])
            if not dates:
                return self._json({'error': '日付を選択してください'}, 400)
            if start >= end:
                return self._json({'error': '終了時間は開始時間より後にしてください'}, 400)
            for d in dates:
                existing = next((s for s in my_schedules if s['date'] == d), None)
                if existing:
                    existing.update({'start': start, 'end': end, 'tags': tags})
                else:
                    my_schedules.append({'date': d, 'start': start, 'end': end, 'tags': tags})
            my_schedules.sort(key=lambda x: x['date'])
            self._json({'count': len(my_schedules)})
        else:
            self.send_error(404)

    def do_DELETE(self):
        path = urllib.parse.urlparse(self.path).path
        if path.startswith('/api/my_schedules/'):
            date_str = path.split('/')[-1]
            my_schedules[:] = [s for s in my_schedules if s['date'] != date_str]
            self._json({'ok': True})
        else:
            self.send_error(404)


# ── 起動 ──
if __name__ == '__main__':
    import webbrowser, threading
    PORT   = 8000
    server = HTTPServer(('localhost', PORT), Handler)
    url    = f'http://localhost:{PORT}'
    print(f'✅ OfficeMeet 出社登録 起動中 → {url}')
    print('   停止: Ctrl+C')
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n停止しました')