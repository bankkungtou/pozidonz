import requests
import json
from datetime import datetime
from setting import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramNotifier:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, message):
        """ส่งข้อความไปยัง Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                print("✅ ส่งการแจ้งเตือนไป Telegram สำเร็จ")
                return True
            else:
                print(f"❌ ไม่สามารถส่งการแจ้งเตือนไป Telegram ได้: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการส่งการแจ้งเตือน Telegram: {e}")
            return False
    
    def send_post_status(self, story_title, video_status, platform_results):
        """ส่งสถานะการโพสต์ตามรูปแบบที่กำหนด"""
        try:
            # สร้างข้อความตามรูปแบบที่ต้องการ
            message = f"📱 <b>สถานะการโพสต์</b>\n\n"
            message += f"📖 <b>เรื่อง:</b> {story_title}\n"
            message += f"🎬 <b>Generate VDO:</b> {'✅ OK' if video_status else '❌ FAILED'}\n"
            
            # เพิ่มสถานะของแต่ละแพลตฟอร์ม
            platform_names = {
                'tiktok': 'TikTok',
                'youtube': 'YouTube', 
                'instagram': 'Reels'
            }
            
            for platform, success in platform_results.items():
                platform_display = platform_names.get(platform, platform.title())
                status = '✅ OK' if success else '❌ FAILED'
                message += f"📤 <b>Post to {platform_display}:</b> {status}\n"
            
            # เพิ่มเวลา
            message += f"\n🕐 <b>เวลา:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการสร้างข้อความสถานะ: {e}")
            return False
    
    def test_connection(self):
        """ทดสอบการเชื่อมต่อ Telegram Bot"""
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url)
            
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info['ok']:
                    print(f"✅ เชื่อมต่อ Telegram Bot สำเร็จ: @{bot_info['result']['username']}")
                    return True
            
            print(f"❌ ไม่สามารถเชื่อมต่อ Telegram Bot ได้: {response.text}")
            return False
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการทดสอบ Telegram Bot: {e}")
            return False

if __name__ == "__main__":
    # ทดสอบการทำงาน
    notifier = TelegramNotifier()
    
    # ทดสอบการเชื่อมต่อ
    if notifier.test_connection():
        # ทดสอบส่งข้อความ
        test_results = {
            'tiktok': True,
            'youtube': True,
            'instagram': False
        }
        notifier.send_post_status("ผีป่าช้า", True, test_results)