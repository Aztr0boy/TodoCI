# TodoCI — รายการตรวจส่ง Mini-Project

## ข้อกำหนดและสถานะ

| ข้อกำหนด | สถานะ | หลักฐาน/สิ่งที่ต้องทำ |
|---|---|---|
| เลือกระบบหนึ่งระบบ | ทำแล้ว | TodoCI เป็นระบบจัดการรายการงาน |
| จำลอง source code ที่รันได้ | ทำแล้ว | เว็บ, REST API และ CLI อยู่ในโปรเจกต์ |
| ใช้ GitHub ร่วมกัน | เตรียมขั้นตอนไว้แล้ว | สร้าง repository, push โค้ด, แบ่ง branch และ review ผ่าน Pull Request |
| Jenkins Build | เตรียม pipeline แล้ว | Jenkinsfile สร้าง venv, ติดตั้ง requirements และตรวจ syntax |
| Jenkins Test | เตรียม pipeline แล้ว | รัน pytest และเผยแพร่ JUnit; ในเครื่องตรวจแล้ว 38 tests ผ่าน |
| Jenkins Deploy | เตรียม pipeline แล้ว | Deploy จำลองใน temporary directory, smoke test เว็บ/API และเก็บ artifact |
| ลิงก์ GitHub | รอทำภายนอก | ใส่ลิงก์ repository จริงในรายงาน/สไลด์หลังสร้าง repository |
| ภาพหน้าจอ Jenkins | รอทำภายนอก | จับภาพ pipeline ที่ผ่านครบทุก stage และหน้า artifact หลังรัน Jenkins จริง |
| สไลด์นำเสนอ | ทำแล้ว | เปิด `todoci-presentation.html` ใน browser; ใช้ปุ่มลูกศรเปลี่ยนสไลด์ |

## ขั้นตอนก่อนส่ง

1. สร้าง repository บน GitHub และ push โค้ดตามคำสั่งใน README
2. เพิ่มสมาชิก 3–4 คนและใช้ Pull Request เป็นหลักฐานการทำงานร่วมกัน
3. ตั้ง Jenkins Pipeline from SCM ให้ชี้ repository และ `Jenkinsfile`
4. กด **Build Now**; ตรวจให้ Build, Test, Deploy เป็นสีเขียว และ JUnit แสดง 38 tests
5. ดาวน์โหลด/ตรวจ `todo-app.tar.gz` จาก Jenkins artifacts
6. จับภาพหน้า Pipeline/Console Output ที่สำเร็จและหน้า artifact แล้วแนบในงานส่ง
7. แทนที่ข้อความ `[ใส่ลิงก์ GitHub]` ในสไลด์ด้วย URL จริงก่อนนำเสนอ

> Deploy ในตัวอย่างเป็นการจำลองพร้อม smoke test ไม่ใช่ public hosting หากอาจารย์ต้องการ URL เว็บที่เปิดจากภายนอก ต้องกำหนด hosting/เครื่องปลายทางและ credentials เพิ่มเติม
