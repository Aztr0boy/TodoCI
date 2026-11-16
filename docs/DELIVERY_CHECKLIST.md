# TodoCI — รายการตรวจส่ง Mini-Project

## ข้อกำหนดและสถานะ

| ข้อกำหนด | สถานะ | หลักฐาน/สิ่งที่ต้องทำ |
|---|---|---|
| เลือกระบบหนึ่งระบบ | ทำแล้ว | TodoCI เป็นระบบจัดการรายการงาน |
| จำลอง source code ที่รันได้ | ทำแล้ว | เว็บ, REST API และ CLI อยู่ในโปรเจกต์ |
| ใช้ GitHub ร่วมกัน | Repository พร้อมแล้ว | https://github.com/Aztr0boy/TodoCI; สมาชิกต้องทำ branch/Pull Request ของตนเอง |
| Jenkins Build | ผ่านแล้ว | Jenkins job `TodoCI` ดึง `main` และผ่าน Build |
| Jenkins Test | ผ่านแล้ว | JUnit แสดง 38 passed, 0 failed |
| Jenkins Deploy | ผ่านแล้ว | Smoke test health/API ผ่านและเก็บ `todo-app.tar.gz` เป็น artifact |
| ลิงก์ GitHub | ทำแล้ว | https://github.com/Aztr0boy/TodoCI |
| ภาพหน้าจอ Jenkins | จับภาพแล้ว | Pipeline Overview ของ Build #1 แสดงทุก stage เป็นสีเขียวในบทสนทนานี้ |
| สไลด์นำเสนอ | ทำแล้ว | เปิด `todoci-presentation.html` ใน browser; หน้าปกระบุสมาชิกทั้ง 3 คนแล้ว |

## ขั้นตอนก่อนส่ง

1. เพิ่มสมาชิก 3–4 คนและให้แต่ละคนทำ branch/Pull Request ตามบทบาทกลุ่ม
2. ตรวจ Jenkins job ที่ http://localhost:8080/job/TodoCI/
3. ดาวน์โหลด/ตรวจ `todo-app.tar.gz` จาก Jenkins Build #1 artifacts
4. บันทึกภาพ Pipeline Overview ที่แสดงผลสำเร็จจากภาพในบทสนทนา แล้วแนบในงานส่ง
5. ตรวจชื่อสมาชิกและรหัสในหน้าปกก่อนนำเสนอ

> Deploy ในตัวอย่างเป็นการจำลองพร้อม smoke test ไม่ใช่ public hosting หากอาจารย์ต้องการ URL เว็บที่เปิดจากภายนอก ต้องกำหนด hosting/เครื่องปลายทางและ credentials เพิ่มเติม
