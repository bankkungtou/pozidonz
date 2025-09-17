"""
การตั้งค่าสำหรับระบบสร้างคอนเทนต์เรื่องผีอัตโนมัติ (ปรับปรุงเพื่อความปลอดภัย)
"""
import os
from datetime import time

# API Keys และการตั้งค่า
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your_gemini_api_key_here')
GEMINI_MODEL = 'gemini-pro'

# TikTok API Settings (สำหรับการสร้างเนื้อหาเท่านั้น ไม่อัตโนมัติโพสต์)
TIKTOK_CLIENT_KEY = os.getenv('TIKTOK_CLIENT_KEY', 'your_tiktok_client_key')
TIKTOK_CLIENT_SECRET = os.getenv('TIKTOK_CLIENT_SECRET', 'your_tiktok_client_secret')
TIKTOK_ACCESS_TOKEN = os.getenv('TIKTOK_ACCESS_TOKEN', 'your_tiktok_access_token')

# Instagram API Settings
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN', 'your_instagram_access_token')
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', 'your_business_account_id')

# YouTube API Settings
YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID', 'your_youtube_client_id')
YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET', 'your_youtube_client_secret')
YOUTUBE_REFRESH_TOKEN = os.getenv('YOUTUBE_REFRESH_TOKEN', 'your_youtube_refresh_token')

# Cloudinary Settings (สำหรับ Instagram Reels)
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', 'your_cloudinary_cloud_name')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', 'your_cloudinary_api_key')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', 'your_cloudinary_api_secret')

# โหมดการทำงาน - เปลี่ยนเป็น SAFE MODE
OPERATION_MODE = 'SAFE'  # 'SAFE' = สร้างไฟล์เท่านั้น, 'AUTO' = โพสต์อัตโนมัติ (ไม่แนะนำ)

# การเลือกแพลตฟอร์มที่จะใช้งาน
ENABLED_PLATFORMS = {
    'tiktok': True,
    'instagram': True,
    'youtube': True
}

# เวลาในการสร้างเนื้อหา (ลดเหลือ 2 รอบต่อวัน)
CONTENT_CREATION_TIMES = [
    time(9, 0),   # 09:00
    time(18, 0),  # 18:00
]

# การตั้งค่าไฟล์และโฟลเดอร์
OUTPUT_DIR = 'output'
AUDIO_DIR = os.path.join(OUTPUT_DIR, 'audio')
IMAGE_DIR = os.path.join(OUTPUT_DIR, 'images')
VIDEO_DIR = os.path.join(OUTPUT_DIR, 'videos')
DRAFT_DIR = os.path.join(OUTPUT_DIR, 'drafts')  # โฟลเดอร์สำหรับเก็บ draft
DATA_DIR = 'data'

# ไฟล์สำหรับเก็บประวัติเรื่องที่สร้างแล้ว
CREATED_STORIES_FILE = os.path.join(DATA_DIR, 'created_stories.txt')
POSTED_STORIES_FILE = os.path.join(DATA_DIR, 'posted_stories.txt')  # เก็บไว้สำหรับการโพสต์ด้วยตนเอง

# การตั้งค่าภาพและวิดีโอ
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920  # อัตราส่วน 9:16 สำหรับ TikTok, Instagram Reels, YouTube Shorts
BACKGROUND_COLOR = (0, 0, 0)  # สีดำ
TEXT_COLOR = (200, 50, 50)  # สีแดงอ่อนลง (ไม่เข้มเกินไป)

# ฟ้อนต์สำหรับข้อความ (ใช้ฟ้อนต์ที่อ่านง่าย)
FONT_PATH = 'fonts/thai_font.ttf'  # เปลี่ยนเป็นฟ้อนต์ธรรมดา
FONT_SIZE = 70  # ลดขนาดลงเล็กน้อย

# การตั้งค่า Text-to-Speech
TTS_LANGUAGE = 'th'  # ภาษาไทย
TTS_SPEED = 0.9  # ช้าลงเล็กน้อยเพื่อให้ฟังง่าย

# การตั้งค่าเนื้อหาเพื่อความปลอดภัย
CONTENT_GUIDELINES = {
    'scary_level': 'mild',           # ระดับความน่ากลัว: mild, moderate, high
    'family_friendly': True,         # เหมาะสำหรับครอบครัว
    'include_disclaimer': True,      # ใส่คำเตือน
    'educational_focus': True,       # เน้นการศึกษาวัฒนธรรม
    'max_story_length': 250,         # จำกัดความยาวเรื่อง
    'avoid_graphic_content': True,   # หลีกเลี่ยงเนื้อหาที่รุนแรง
}

# แฮชแท็กที่ปลอดภัยและเหมาะสม
SAFE_HASHTAGS = [
    '#เรื่องเล่าไทย', '#วัฒนธรรมไทย', '#ตำนานไทย', 
    '#เรื่องเล่าพื้นบ้าน', '#ประวัติศาสตร์ไทย', '#ภูมิปัญญาไทย',
    '#เรื่องลึกลับ', '#ความเชื่อไทย'
]

# การตั้งค่า TikTok (สำหรับโหมดปลอดภัย)
TIKTOK_SETTINGS = {
    'privacy_level': 'SELF_ONLY',    # บันทึกเป็น draft ก่อน
    'disable_duet': False,
    'disable_comment': False,
    'disable_stitch': False,
    'auto_post': False,              # ปิดการโพสต์อัตโนมัติ
}

# การตั้งค่า Instagram Reels
INSTAGRAM_SETTINGS = {
    'privacy_level': 'SELF_ONLY',    # บันทึกเป็น draft ก่อน
    'auto_post': False,              # ปิดการโพสต์อัตโนมัติ
    'location_id': None,             # ไม่ระบุสถานที่
    'share_to_feed': False,          # ไม่แชร์ไปยัง feed
}

# การตั้งค่า YouTube Shorts
YOUTUBE_SETTINGS = {
    'privacy_status': 'private',     # ตั้งเป็น private ก่อน
    'auto_post': False,              # ปิดการโพสต์อัตโนมัติ
    'category_id': '24',             # Entertainment category
    'made_for_kids': False,          # ไม่ใช่เนื้อหาสำหรับเด็ก
    'shorts_eligible': True,         # เป็น YouTube Shorts
}

# ข้อความเตือนที่จะใส่ในเนื้อหา
DISCLAIMER_TEXT = """
⚠️ เรื่องเล่านี้เป็นส่วนหนึ่งของวัฒนธรรมและความเชื่อพื้นบ้านไทย
มีจุดประสงค์เพื่อการศึกษาและอนุรักษ์วัฒนธรรม
"""

# การแจ้งเตือน
NOTIFICATION_SETTINGS = {
    'enable_notifications': True,
    'notify_on_content_ready': True,
    'notify_on_error': True,
    'notification_sound': True,
}

# ข้อจำกัดการใช้งาน
USAGE_LIMITS = {
    'max_stories_per_day': 2,        # จำกัดแค่ 2 เรื่องต่อวัน
    'min_interval_hours': 6,         # ห่างกันอย่างน้อย 6 ชั่วโมง
    'max_retries': 3,                # ลองใหม่สูงสุด 3 ครั้ง
}

# โหมดการทำงานต่างๆ
MODES = {
    'SAFE': {
        'description': 'สร้างเนื้อหาและบันทึกเป็นไฟล์เท่านั้น',
        'auto_post': False,
        'create_drafts': True,
        'manual_review': True,
    },
    'PREVIEW': {
        'description': 'สร้างเนื้อหาและแสดงตัวอย่าง',
        'auto_post': False,
        'create_drafts': True,
        'show_preview': True,
    },
    'MANUAL': {
        'description': 'สร้างเนื้อหาและรอการอนุมัติ',
        'auto_post': False,
        'require_approval': True,
    }
}

# การตั้งค่าเฉพาะแต่ละแพลตฟอร์ม
PLATFORM_SPECIFIC_SETTINGS = {
    'tiktok': {
        'max_duration': 60,          # วินาที
        'recommended_duration': 30,  # วินาที
        'hashtag_limit': 5,
        'description_limit': 150,
    },
    'instagram': {
        'max_duration': 90,          # วินาที
        'recommended_duration': 30,  # วินาที
        'hashtag_limit': 30,
        'description_limit': 2200,
    },
    'youtube': {
        'max_duration': 60,          # วินาที
        'recommended_duration': 30,  # วินาที
        'hashtag_limit': 15,
        'description_limit': 5000,
        'title_limit': 100,
    }
}

def create_directories():
    """สร้างโฟลเดอร์ที่จำเป็นสำหรับการทำงาน"""
    directories = [
        OUTPUT_DIR, AUDIO_DIR, IMAGE_DIR, 
        VIDEO_DIR, DRAFT_DIR, DATA_DIR
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def get_current_mode_settings():
    """ได้การตั้งค่าของโหมดปัจจุบัน"""
    return MODES.get(OPERATION_MODE, MODES['SAFE'])

def is_safe_mode():
    """ตรวจสอบว่าอยู่ในโหมดปลอดภัยหรือไม่"""
    return OPERATION_MODE == 'SAFE'

def get_enabled_platforms():
    """ได้รายการแพลตฟอร์มที่เปิดใช้งาน"""
    return [platform for platform, enabled in ENABLED_PLATFORMS.items() if enabled]

def get_platform_settings(platform):
    """ได้การตั้งค่าเฉพาะของแพลตฟอร์ม"""
    platform_settings = {
        'tiktok': TIKTOK_SETTINGS,
        'instagram': INSTAGRAM_SETTINGS,
        'youtube': YOUTUBE_SETTINGS
    }
    return platform_settings.get(platform, {})

def get_content_prompt():
    """สร้าง prompt สำหรับ Gemini ตามการตั้งค่าความปลอดภัย"""
    if CONTENT_GUIDELINES['family_friendly']:
        return """
        กรุณาสร้างเรื่องเล่าพื้นบ้านไทยที่น่าสนใจและมีคุณค่าทางวัฒนธรรม
        
        ข้อกำหนด:
        - เหมาะสำหรับทุกวัย ไม่น่ากลัวเกินไป
        - เน้นการเรียนรู้วัฒนธรรมและประวัติศาสตร์ไทย
        - มีบทเรียนหรือคุณค่าที่ได้รับ
        - ความยาวไม่เกิน 250 คำ
        - หลีกเลี่ยงเนื้อหาที่รุนแรงหรือน่าตกใจ
        
        กรุณาตอบในรูปแบบ JSON ดังนี้:
        {
            "title": "ชื่อเรื่อง",
            "story": "เนื้อเรื่องที่เน้นการเรียนรู้วัฒนธรรม",
            "location": "สถานที่",
            "time_period": "ช่วงเวลา",
            "moral": "บทเรียนหรือคุณค่าที่ได้รับ",
            "cultural_value": "คุณค่าทางวัฒนธรรม"
        }
        """
    else:
        return "สร้างเรื่องผีไทยที่น่ากลัว"  # prompt เดิม

if __name__ == "__main__":
    create_directories()
    print("📁 โฟลเดอร์ทั้งหมดถูกสร้างเรียบร้อยแล้ว")
    print(f"🔒 โหมดการทำงาน: {OPERATION_MODE}")
    print(f"📋 การตั้งค่า: {get_current_mode_settings()['description']}")
    print(f"🎯 แพลตฟอร์มที่เปิดใช้งาน: {', '.join(get_enabled_platforms())}")
    
    if is_safe_mode():
        print("✅ ระบบทำงานในโหมดปลอดภัย - จะสร้างไฟล์เท่านั้น ไม่โพสต์อัตโนมัติ")
    else:
        print("⚠️  ระบบทำงานในโหมดอัตโนมัติ - กรุณาระวังระเบียบของแพลตฟอร์มต่างๆ")