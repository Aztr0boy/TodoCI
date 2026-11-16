# TodoCI — ระบบจดงาน (Mini-Project DevOps: GitHub + Jenkins CI/CD)

ระบบจดงานที่ใช้งานได้จริง 2 แบบ: **เว็บ (REST API + หน้าเว็บ)** และ **CLI** เขียนด้วย Python ล้วน (ไม่ต้องติดตั้งไลบรารีเพิ่ม ยกเว้น `pytest` ตอนเทสต์)

## ฟีเจอร์
- เพิ่ม / แก้ไข / ลบงาน, กำหนดส่ง, ความสำคัญ (high/medium/low), แท็ก
- สถานะ `todo → doing → done` (บันทึกวันที่เสร็จ)
- ค้นหา, กรอง (สถานะ/ความสำคัญ/แท็ก), เรียง (ลำดับ/กำหนดส่ง/ความสำคัญ/ชื่อ)
- งานเลยกำหนด, สถิติ + % ความคืบหน้า, ล้างงานที่เสร็จแล้ว
- เก็บข้อมูลลงไฟล์ JSON (เขียนแบบ atomic), รองรับภาษาไทย

## โครงสร้าง
| ไฟล์ | หน้าที่ |
|---|---|
| `todo.py` | logic หลัก (TodoList, Task) |
| `storage.py` | อ่าน/เขียนไฟล์ JSON |
| `server.py` | เว็บเซิร์ฟเวอร์ + REST API |
| `static/index.html` | หน้าเว็บ (single page) |
| `app.py` | CLI |
| `tests/` | unit test, CLI test, API test (38 เทสต์) |
| `Jenkinsfile` | pipeline Build → Test → Deploy |

## วิธีรัน
```bash
# เว็บ  -> เปิด http://localhost:3002
python3 server.py --port 3002

# CLI
python3 app.py add "ส่งรายงาน" --due 2026-12-31 --priority high --tags uni,report
python3 app.py list --sort due
python3 app.py start 1
python3 app.py done 1
python3 app.py search รายงาน
python3 app.py stats
```

## REST API
| Method | Path | ความหมาย |
|---|---|---|
| GET | `/health` | ตรวจสถานะเซิร์ฟเวอร์ |
| GET | `/api/tasks?status=&priority=&tag=&q=&sort=` | รายการงาน |
| POST | `/api/tasks` | เพิ่มงาน `{title, due, priority, tags}` |
| GET/PATCH/DELETE | `/api/tasks/<id>` | ดู / แก้ (รวมเปลี่ยน `status`) / ลบ |
| GET | `/api/stats` | สถิติ |
| POST | `/api/clear-done` | ลบงานที่เสร็จทั้งหมด |

## เทสต์
```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

## CI/CD
### 1) GitHub — รวมโค้ดด้วย branch + Pull Request
สร้าง repository บน GitHub แล้ว push โปรเจกต์ขึ้นไป สมาชิกแต่ละคนทำงานบน branch ของตัวเอง และเปิด Pull Request เพื่อ review ก่อน merge เข้า `main`

```bash
git init -b main
git add .
git commit -m "Initial TodoCI project"
git remote add origin https://github.com/<account>/<repository>.git
git push -u origin main

git checkout -b feature/<ชื่อฟีเจอร์>
# แก้ไขและทดสอบงาน
git add .
git commit -m "feat: <สรุปการเปลี่ยนแปลง>"
git push -u origin feature/<ชื่อฟีเจอร์>
# เปิด Pull Request บน GitHub แล้ว review/merge เข้า main
```

### 2) Jenkins — Pipeline from SCM (`Jenkinsfile`)
Jenkins agent ใช้ได้ทั้ง Windows และ Linux/macOS โดยต้องมี Python 3 และเชื่อมต่ออินเทอร์เน็ตเพื่อติดตั้งแพ็กเกจได้ ต้องติดตั้ง Jenkins plugins สำหรับ Pipeline, Git และ JUnit ก่อน

1. เลือก **New Item → Pipeline** ตั้งชื่อ `TodoCI`
2. เลือก **Pipeline script from SCM** และ SCM เป็น **Git**
3. ใส่ URL repository `https://github.com/Aztr0boy/TodoCI.git`, branch `*/main` และ Script Path `Jenkinsfile`
4. ตั้ง **Poll SCM** เป็น `H/5 * * * *` หรือใช้ GitHub webhook หากตั้งค่า webhook ไว้แล้ว
5. กด **Save → Build Now** แล้วตรวจ Console Output และผล JUnit

> Stage `Deploy` ในโปรเจกต์นี้เป็นการ deploy จำลองใน Jenkins workspace: จัดแพ็กไฟล์ไปยัง `deploy/`, เปิดเว็บชั่วคราวเพื่อตรวจ health/API และเก็บ `todo-app.tar.gz` เป็น Jenkins artifact ไม่ได้เผยแพร่เว็บขึ้น public hosting

| Stage | ทำอะไร |
|---|---|
| **Build** | สร้าง venv, ติดตั้ง dependency, ตรวจ syntax |
| **Test** | รัน pytest ทั้ง 38 เทสต์ + รายงาน JUnit |
| **Deploy** | จัดเตรียมแอปใน temporary directory, ตรวจ health/API (smoke test), แพ็ก `todo-app.tar.gz` เป็น artifact |

### สถานะส่งงาน
- ระบบ TodoCI, unit/API/CLI tests และ Jenkins pipeline มีอยู่แล้ว
- ตรวจในเครื่องแล้ว: `python -m pytest -q` ได้ **38 passed**
- GitHub repository `Aztr0boy/TodoCI` มีอยู่แล้ว แต่ตอนตรวจยังว่าง ต้อง push โค้ดขึ้นไปก่อนตั้ง Jenkins SCM
- Jenkins ในเครื่องทำงานบน Windows; pipeline รองรับ Windows และ Linux/macOS
- ยังต้องทำ: push โค้ด, ตั้ง Jenkins ให้ชี้ repository, รัน pipeline จริง และจับภาพผลสำเร็จ
- สไลด์และรายการตรวจส่งงานอยู่ที่ [`docs/todoci-presentation.html`](docs/todoci-presentation.html) และ [`docs/DELIVERY_CHECKLIST.md`](docs/DELIVERY_CHECKLIST.md)

ดูการแบ่งงานและลำดับสาธิตได้ในสไลด์ หรือเปิด checklist ก่อนนำเสนอ
