# main.py
import os
import yt_dlp
import openai
import subprocess
import requests
from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from settings import *

# ===== Init =====
openai.api_key = OPENAI_API_KEY
os.makedirs(TEMP_DIR, exist_ok=True)

# ===== 1. ดึงข้อมูลจาก YouTube =====
def download_youtube(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': AUDIO_FILE,
        'writethumbnail': True,
        'writeinfojson': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title")
        thumbnail_url = info.get("thumbnail")

        # ดาวน์โหลด thumbnail
        response = requests.get(thumbnail_url)
        with open(THUMBNAIL_FILE, 'wb') as f:
            f.write(response.content)
        return title

# ===== 2. ถอดเสียงด้วย Whisper =====
def transcribe_audio():
    with open(AUDIO_FILE, "rb") as f:
        transcript = openai.Audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text

# ===== 3. สรุปเรื่องผี =====
def summarize_story(transcript):
    prompt = f"""
    คุณเป็นนักเล่าเรื่องผี สรุปเรื่องผีจากข้อความด้านล่างให้กระชับแต่ยังคงความน่ากลัว
    และให้ฟังแล้วเหมือนเล่าในรายการวิทยุสยองขวัญ ความยาวไม่เกิน 3 ย่อหน้า
    เน้นภาษาไทยที่อ่านแล้วชวนขนลุก:
    {transcript}
    """
    res = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return res.choices[0].message.content

# ===== 4. แปลงสรุปเป็นเสียง =====
def text_to_speech(text):
    from google.cloud import texttospeech
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_TTS_CREDENTIALS_JSON

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="th-TH", 
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config
    )
    with open(AUDIO_FILE, "wb") as out:
        out.write(response.audio_content)

# ===== 5. สร้างภาพปก =====
def create_cover_image(title, summary):
    img = Image.open(THUMBNAIL_FILE).convert("RGB")
    w, h = img.size

    new_h = h + 300
    new_img = Image.new("RGB", (w, new_h), (0, 0, 0))
    new_img.paste(img, (0, 0))

    draw = ImageDraw.Draw(new_img)
    try:
        font_title = ImageFont.truetype("arial.ttf", 32)
        font_summary = ImageFont.truetype("arial.ttf", 24)
    except:
        font_title = ImageFont.load_default()
        font_summary = ImageFont.load_default()

    # วาดข้อความ title
    draw.text((20, h + 20), title[:50] + "...", font=font_title, fill=(255, 255, 255))
    
    # วาดข้อความ summary
    summary_text = summary[:150] + "..."
    draw.text((20, h + 80), summary_text, font=font_summary, fill=(200, 200, 200))

    new_img.save(COVER_IMAGE_FILE)

# ===== 6. รวมภาพและเสียงเป็น MP4 =====
def merge_audio_image_to_mp4():
    subprocess.run([
        "ffmpeg", "-loop", "1",
        "-i", COVER_IMAGE_FILE,
        "-i", AUDIO_FILE,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest", OUTPUT_VIDEO_FILE,
        "-y"
    ])

# ===== 7. อัปโหลด TikTok =====
def upload_to_tiktok(caption):
    # TikTok API เอกสาร: https://developers.tiktok.com/
    # ต้องทำการ Auth และเรียก endpoint /video/upload/
    # ตัวอย่างการใช้งาน (ต้องปรับแต่งตาม API จริง)
    """
    headers = {
        'Authorization': f'Bearer {TIKTOK_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'caption': caption,
        'video_file': OUTPUT_VIDEO_FILE
    }
    
    response = requests.post(
        'https://open-api.tiktok.com/video/upload/',
        headers=headers,
        files={'video': open(OUTPUT_VIDEO_FILE, 'rb')},
        data={'caption': caption}
    )
    
    return response.json()
    """
    print(f"จะอัปโหลดไปยัง TikTok ด้วยแคปชั่น: {caption}")
    pass

# ===== Telegram Bot Handler =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    # ตรวจสอบว่าเป็น YouTube URL หรือไม่
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("❌ กรุณาส่งลิงก์ YouTube ที่ถูกต้อง")
        return
    
    await update.message.reply_text("⏳ กำลังประมวลผล...")
    
    try:
        # ขั้นตอนการประมวลผล
        await update.message.reply_text("📥 กำลังดาวน์โหลดจาก YouTube...")
        title = download_youtube(url)
        
        await update.message.reply_text("🎤 กำลังถอดเสียง...")
        transcript = transcribe_audio()
        
        await update.message.reply_text("👻 กำลังสรุปเป็นเรื่องผี...")
        summary = summarize_story(transcript)
        
        await update.message.reply_text("🔊 กำลังแปลงเป็นเสียง...")
        text_to_speech(summary)
        
        await update.message.reply_text("🖼️ กำลังสร้างภาพปก...")
        create_cover_image(title, summary)
        
        await update.message.reply_text("🎬 กำลังรวมเป็นวิดีโอ...")
        merge_audio_image_to_mp4()
        
        # ส่งไฟล์วิดีโอกลับไปยัง Telegram
        with open(OUTPUT_VIDEO_FILE, 'rb') as video:
            await update.message.reply_video(
                video=video,
                caption=f"🎬 {title}\n\n👻 {summary[:100]}...\n\n{TIKTOK_HASHTAGS}"
            )
        
        # อัปโหลดไปยัง TikTok (ถ้าต้องการ)
        # upload_to_tiktok(f"{title} {TIKTOK_HASHTAGS}")
        
        await update.message.reply_text("✅ เสร็จแล้ว! พร้อมโพสต์ TikTok")
        
    except Exception as e:
        await update.message.reply_text(f"❌ เกิดข้อผิดพลาด: {str(e)}")
        print(f"Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot เริ่มทำงานแล้ว...")
    app.run_polling()