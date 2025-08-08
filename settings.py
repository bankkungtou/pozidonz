# settings.py

# ==== API Keys & Tokens ====
TELEGRAM_BOT_TOKEN = "ใส่ TOKEN BOT TELEGRAM"
OPENAI_API_KEY = "ใส่ API KEY ของ OpenAI"
GOOGLE_TTS_CREDENTIALS_JSON = "path/to/google_tts_credentials.json"  # ถ้าใช้ Google Cloud TTS
TIKTOK_ACCESS_TOKEN = "ใส่ ACCESS TOKEN ของ TikTok API"

# ==== ไฟล์ชั่วคราว ====
TEMP_DIR = "temp"
AUDIO_FILE = f"{TEMP_DIR}/audio.mp3"
THUMBNAIL_FILE = f"{TEMP_DIR}/thumb.jpg"
COVER_IMAGE_FILE = f"{TEMP_DIR}/cover.jpg"
OUTPUT_VIDEO_FILE = f"{TEMP_DIR}/output.mp4"

# ==== ค่าตั้งต้นอื่นๆ ====
TIKTOK_HASHTAGS = "#เรื่องผี #เล่าเรื่องผี #สรุปผี"
VIDEO_DURATION_PADDING = 2  # วินาที padding เสียง