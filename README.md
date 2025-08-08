# Python Telegram Bot - YouTube to Ghost Story TikTok

ระบบ Telegram Bot ที่แปลงวิดีโอ YouTube เป็นเรื่องเล่าผีและสร้างวิดีโอสำหรับ TikTok

## การติดตั้ง

1. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

2. ติดตั้ง FFmpeg:
   - Windows: ดาวน์โหลดจาก https://ffmpeg.org/download.html
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

3. ตั้งค่า API Keys ในไฟล์ `settings.py`:
   - Telegram Bot Token
   - OpenAI API Key
   - Google Cloud TTS Credentials
   - TikTok Access Token

## การใช้งาน

1. รันบอท:
```bash
python main.py
```

2. ส่งลิงก์ YouTube ไปยังบอทใน Telegram

3. รอให้บอทประมวลผลและส่งวิดีโอกลับมา

## คุณสมบัติ

- ✅ ดาวน์โหลดเสียงและ thumbnail จาก YouTube
- ✅ ถอดเสียงด้วย OpenAI Whisper
- ✅ สรุปเป็นเรื่องผีด้วย GPT
- ✅ แปลงข้อความเป็นเสียงภาษาไทย
- ✅ สร้างภาพปกแบบกำหนดเอง
- ✅ รวมเสียงและภาพเป็นวิดีโอ MP4
- 🔄 อัปโหลดไปยัง TikTok (ต้องปรับแต่ง API)

## หมายเหตุ

- ต้องมี Google Cloud TTS credentials
- ต้องติดตั้ง FFmpeg
- TikTok API ยังต้องปรับแต่งตามเอกสารล่าสุด