# IoT-230 Smart Agro-Environmental & Farm System (ESP32 + ESPHome + Firebase RTDB + GitHub Pages)

ระบบตรวจวัดและรายงานสภาพแวดล้อมเพื่อการเกษตรอัจฉริยะ (Smart Agro-Environmental Station) ส่งข้อมูลจากบอร์ด ESP32 ด้วย ESPHome ไปจัดเก็บบน Google Firebase Realtime Database แบบ Real-time (ทั้ง `/latest` และ `/history`) และแสดงผลผ่านเว็บแดชบอร์ดที่โฮสต์บน GitHub Pages

---

## 📌 สถาปัตยกรรมระบบ (System Architecture)

```
        +----------------------------------------------+
        |             ESP32 (DevKit V1)                |
        |                  ESPHome                     |
        |  - temp (สุ่ม 25-35 °C)                      |
        |  - humi (สุ่ม 50-80 %)                       |
        |  - soil (สุ่ม 40-75 %)                       |
        |  - light (สุ่ม 150-1100 lx)                  |
        |  - co2 (สุ่ม 400-900 ppm)                    |
        |  - pm25 (สุ่ม 12-57 µg/m³)                   |
        |  - water_level (สุ่ม 45-95 %)                |
        |  - SNTP -> timestamp (Asia/Bangkok)          |
        +----------------------+-----------------------+
                               |
                               | HTTPS REST API (Every 10s)
                               v
        +----------------------------------------------+
        |         Firebase Realtime Database           |
        |  iot-230-default-rtdb.asia-southeast1        |
        |                                              |
        |  /lab/esp32                                  |
        |    ├── latest  (PUT: ค่าปัจจุบันชุดล่าสุด)      |
        |    └── history (POST: บันทึกย้อนหลัง Time-Series)|
        +----------------------+-----------------------+
                               |
                               | EventSource (SSE) & REST
                               v
        +----------------------------------------------+
        |         GitHub Pages Web Dashboard           |
        |   URL: https://nekojeng12.github.io/freeboard|
        |                                              |
        |  - Live Status Indicator                     |
        |  - 7 Sensor Realtime Metric Cards            |
        |  - Dynamic Trend Deltas (▲ / ▼)              |
        |  - Real-time Interactive Charts (Chart.js)   |
        |  - History Log Table + Export CSV            |
        |  - Dark Mode & Sound Alert Support           |
        +----------------------------------------------+
```

---

## 📊 รายการข้อมูลเซนเซอร์ (Data Schema - 7 คอลัมน์ + เวลา)

| ลำดับ | รหัสคีย์ (Field) | ชื่อเซนเซอร์ / พารามิเตอร์ | หน่วยวัด | ช่วงค่าจำลอง | ประโยชน์และการนำไปใช้จริง |
|---|---|---|---|---|---|
| 1 | `temp` | อุณหภูมิอากาศ (Temperature) | °C | 25.0 - 35.0 | ตรวจวัดความร้อนในโรงเรือนเพื่อควบคุมพัดลมระบายอากาศ |
| 2 | `humi` | ความชื้นสัมพัทธ์ในอากาศ (Humidity) | % | 50.0 - 80.0 | ควบคุมการระเหยน้ำและป้องกันเชื้อราในพืช |
| 3 | `soil` | ความชื้นในดิน (Soil Moisture) | % | 40.0 - 75.0 | ระบบสั่งรดน้ำอัตโนมัติเมื่อดินแห้งเกินเกณฑ์ |
| 4 | `light` | ความเข้มแสงแดด (Light Intensity) | lx | 150 - 1100 | ประเมินอัตราการสังเคราะห์แสงของพืชในแต่ละช่วงวัน |
| 5 | `co2` | ปริมาณก๊าซคาร์บอนไดออกไซด์ (CO2) | ppm | 400 - 900 | วัดความอุดมสมบูรณ์ของก๊าซสำหรับการเจริญเติบโต |
| 6 | `pm25` | ฝุ่นละออง PM2.5 (Air Quality) | µg/m³ | 12.0 - 57.0 | ตรวจสอบคุณภาพอากาศและความปลอดภัยในพื้นที่ปฏิบัติงาน |
| 7 | `water_level` | ระดับน้ำสำรองในถัง (Reservoir Level) | % | 45.0 - 95.0 | ตรวจสอบปริมาณน้ำต้นทุนเพื่อเตือนก่อนน้ำหมดถัง |
| 8 | `timestamp` | เวลา Unix Timestamp | วินาที (s) | SNTP | อ้างอิงเวลาที่ตรวจวัดจริงเพื่อพล็อตกราฟและเรียงประวัติ |

---

## 🔗 ข้อมูลการส่งงานและ URL สำคัญ

- **URL Dashboard บน GitHub Pages (ส่งใน Classroom):**  
  `https://nekojeng12.github.io/freeboard`
- **Firebase Database URL:**  
  `https://iot-230-default-rtdb.asia-southeast1.firebasedatabase.app`
- **Firebase REST Endpoints:**  
  - Current state: `https://iot-230-default-rtdb.asia-southeast1.firebasedatabase.app/lab/esp32/latest.json`  
  - Historical data: `https://iot-230-default-rtdb.asia-southeast1.firebasedatabase.app/lab/esp32/history.json`

---

## 🛠️ ไฟล์ในโปรเจกต์

1. `index.html` : หน้าแดชบอร์ดหลักที่ใช้แสดงผลแบบ Realtime บน GitHub Pages
2. `iot-230.yaml` : ไฟล์คอนฟิก ESPHome สำหรับบอร์ด ESP32 DevKit V1
3. `simulator.py` : สคริปต์ Python สำหรับจำลองการส่งข้อมูลเซนเซอร์ขึ้น Firebase อย่างต่อเนื่อง
