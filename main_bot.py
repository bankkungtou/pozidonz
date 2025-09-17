"""
ไฟล์หลักสำหรับรันระบบสร้างคอนเทนต์เรื่องผีอัตโนมัติ (รองรับหลายแพลตฟอร์ม)
"""
import schedule
import time
import datetime
import os
from google_gemini_control import GeminiController
from text_to_speech import TextToSpeech
from generate_vdo import VideoGenerator
from tiktok_control import TikTokController
from reels_control import ReelsController
from youtube_control import YouTubeController
from telegram_notifier import TelegramNotifier
from setting import (
    CONTENT_CREATION_TIMES, create_directories, get_enabled_platforms,
    get_platform_settings, is_safe_mode, get_current_mode_settings,
    TELEGRAM_SETTINGS
)

class MultiPlatformGhostStoryBot:
    def __init__(self):
        """เริ่มต้นระบบบอทหลายแพลตฟอร์ม"""
        print("🎃 เริ่มต้นระบบสร้างคอนเทนต์เรื่องผีอัตโนมัติ (หลายแพลตฟอร์ม)...")
        
        # สร้างโฟลเดอร์ที่จำเป็น
        create_directories()
        
        # เริ่มต้นคอมโพเนนต์หลัก
        self.gemini = GeminiController()
        self.tts = TextToSpeech()
        self.video_gen = VideoGenerator()
        
        # เริ่มต้นคอนโทรลเลอร์สำหรับแต่ละแพลตฟอร์ม
        self.controllers = {}
        enabled_platforms = get_enabled_platforms()
        
        if 'tiktok' in enabled_platforms:
            try:
                self.controllers['tiktok'] = TikTokController()
                print("✅ TikTok Controller เริ่มต้นสำเร็จ")
            except Exception as e:
                print(f"⚠️ ไม่สามารถเริ่มต้น TikTok Controller: {e}")
        
        if 'instagram' in enabled_platforms:
            try:
                self.controllers['instagram'] = ReelsController()
                print("✅ Instagram Reels Controller เริ่มต้นสำเร็จ")
            except Exception as e:
                print(f"⚠️ ไม่สามารถเริ่มต้น Instagram Controller: {e}")
        
        if 'youtube' in enabled_platforms:
            try:
                self.controllers['youtube'] = YouTubeController()
                print("✅ YouTube Shorts Controller เริ่มต้นสำเร็จ")
            except Exception as e:
                print(f"⚠️ ไม่สามารถเริ่มต้น YouTube Controller: {e}")
        
        print(f"✅ ระบบพร้อมใช้งาน! (แพลตฟอร์ม: {', '.join(self.controllers.keys())})")
        
        if is_safe_mode():
            print("🔒 โหมดปลอดภัย: จะสร้างไฟล์เท่านั้น ไม่โพสต์อัตโนมัติ")
    
        # เพิ่ม Telegram Notifier
        if TELEGRAM_SETTINGS.get('enabled', False):
            self.telegram_notifier = TelegramNotifier()
        else:
            self.telegram_notifier = None
    
    def create_and_post_story(self):
        """สร้างและโพสต์เรื่องผีไปยังแพลตฟอร์มที่เปิดใช้งาน"""
        try:
            print(f"🕐 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - เริ่มสร้างเรื่องผี...")
            
            # ขั้นตอนที่ 1: ขอเรื่องผีจาก Gemini
            print("📖 กำลังขอเรื่องผีจาก Gemini AI...")
            story_data = self.gemini.get_ghost_story()
            
            if not story_data:
                print("❌ ไม่สามารถขอเรื่องผีได้")
                return False
            
            print(f"✅ ได้เรื่องผีแล้ว: {story_data['title']}")
            
            # ขั้นตอนที่ 2: สร้างสคริปต์
            script = self.gemini.create_script(story_data)
            if not script:
                print("❌ ไม่สามารถสร้างสคริปต์ได้")
                return False
            
            print("✅ สร้างสคริปต์สำเร็จ")
            
            # ขั้นตอนที่ 3: แปลงข้อความเป็นเสียง
            print("🎵 กำลังสร้างไฟล์เสียง...")
            audio_file = self.tts.create_audio_from_script(script, story_data['title'])
            
            if not audio_file:
                print("❌ ไม่สามารถสร้างไฟล์เสียงได้")
                return False
            
            print(f"✅ สร้างไฟล์เสียงสำเร็จ: {audio_file}")
            
            # ขั้นตอนที่ 4: สร้างวิดีโอ
            print("🎬 กำลังสร้างวิดีโอ...")
            video_file = self.video_gen.generate_complete_video(story_data, audio_file)
            
            video_success = bool(video_file)
            
            if not video_file:
                print("❌ ไม่สามารถสร้างวิดีโอได้")
                # ส่งการแจ้งเตือนล้มเหลว
                if self.telegram_notifier and TELEGRAM_SETTINGS.get('notify_on_failure', True):
                    self.telegram_notifier.send_post_status(
                        story_data['title'], 
                        False, 
                        {platform: False for platform in self.controllers.keys()}
                    )
                return False
            
            print(f"✅ สร้างวิดีโอสำเร็จ: {video_file}")
            
            # ขั้นตอนที่ 5: อัปโหลดไปยังแพลตฟอร์มต่างๆ
            upload_results = {}
            
            for platform, controller in self.controllers.items():
                try:
                    print(f"📱 กำลังอัปโหลดไป {platform.title()}...")
                    
                    if is_safe_mode():
                        # โหมดปลอดภัย: สร้างไฟล์ draft เท่านั้น
                        success = controller.create_draft(video_file, story_data)
                        if success:
                            print(f"✅ สร้าง draft สำหรับ {platform.title()} สำเร็จ")
                        else:
                            print(f"❌ ไม่สามารถสร้าง draft สำหรับ {platform.title()} ได้")
                    else:
                        # โหมดอัตโนมัติ: อัปโหลดจริง (ไม่แนะนำ)
                        success = controller.upload_video(video_file, story_data)
                        if success:
                            print(f"✅ อัปโหลดไป {platform.title()} สำเร็จ!")
                        else:
                            print(f"❌ ไม่สามารถอัปโหลดไป {platform.title()} ได้")
                    
                    upload_results[platform] = success
                    
                except Exception as e:
                    print(f"❌ เกิดข้อผิดพลาดกับ {platform}: {e}")
                    upload_results[platform] = False
            
            # สรุปผลการอัปโหลด
            successful_uploads = [platform for platform, success in upload_results.items() if success]
            
            # ส่งการแจ้งเตือนไป Telegram
            if self.telegram_notifier:
                if successful_uploads and TELEGRAM_SETTINGS.get('notify_on_success', True):
                    self.telegram_notifier.send_post_status(
                        story_data['title'], 
                        video_success, 
                        upload_results
                    )
                elif not successful_uploads and TELEGRAM_SETTINGS.get('notify_on_failure', True):
                    self.telegram_notifier.send_post_status(
                        story_data['title'], 
                        video_success, 
                        upload_results
                    )
            
            if successful_uploads:
                if is_safe_mode():
                    print(f"🎉 สร้าง draft สำเร็จสำหรับ: {', '.join(successful_uploads)}")
                else:
                    print(f"🎉 อัปโหลดสำเร็จไปยัง: {', '.join(successful_uploads)}")
                
                # บันทึกประวัติเรื่องที่สร้างแล้ว
                self.gemini.mark_story_as_posted(story_data)
                return True
            else:
                print("❌ ไม่สามารถอัปโหลดไปยังแพลตฟอร์มใดได้เลย")
                return False
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            # ส่งการแจ้งเตือนข้อผิดพลาด
            if self.telegram_notifier and TELEGRAM_SETTINGS.get('notify_on_failure', True):
                error_results = {platform: False for platform in self.controllers.keys()}
                self.telegram_notifier.send_post_status("เกิดข้อผิดพลาด", False, error_results)
            return False
    
    def setup_schedule(self):
        """ตั้งค่าตารางเวลาการทำงานอัตโนมัติ"""
        print("⏰ กำลังตั้งค่าตารางเวลา...")
        
        for creation_time in CONTENT_CREATION_TIMES:
            schedule.every().day.at(creation_time.strftime("%H:%M")).do(self.create_and_post_story)
            print(f"📅 ตั้งเวลาสร้างคอนเทนต์: {creation_time.strftime('%H:%M')}")
        
        print("✅ ตั้งค่าตารางเวลาเสร็จสิ้น")
    
    def run_once(self):
        """รันสร้างคอนเทนต์ครั้งเดียว"""
        print("🚀 เริ่มสร้างคอนเทนต์ทันที...")
        return self.create_and_post_story()
    
    def test_platform_connections(self):
        """ทดสอบการเชื่อมต่อกับแพลตฟอร์มต่างๆ"""
        print("🔍 ทดสอบการเชื่อมต่อกับแพลตฟอร์มต่างๆ...")
        
        # ทดสอบ Gemini
        print("\n🤖 ทดสอบ Gemini AI...")
        if self.gemini.test_connection():
            print("✅ Gemini AI พร้อมใช้งาน")
        else:
            print("❌ ไม่สามารถเชื่อมต่อ Gemini AI ได้")
        
        # ทดสอบแต่ละแพลตฟอร์ม
        for platform, controller in self.controllers.items():
            print(f"\n📱 ทดสอบ {platform.title()}...")
            if hasattr(controller, 'test_connection') and controller.test_connection():
                print(f"✅ {platform.title()} พร้อมใช้งาน")
            else:
                print(f"❌ ไม่สามารถเชื่อมต่อ {platform.title()} ได้")
        
        # ทดสอบ Telegram
        if self.telegram_notifier:
            print("\n🔔 ทดสอบการเชื่อมต่อ Telegram...")
            if self.telegram_notifier.test_connection():
                print("✅ Telegram Bot พร้อมใช้งาน")
            else:
                print("❌ ไม่สามารถเชื่อมต่อ Telegram Bot ได้")
    
    def run_forever(self):
        """รันระบบแบบอัตโนมัติตามตารางเวลา"""
        self.setup_schedule()
        
        print("🔄 เริ่มรันระบบอัตโนมัติ...")
        print("กด Ctrl+C เพื่อหยุดระบบ")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # ตรวจสอบทุก 1 นาที
        except KeyboardInterrupt:
            print("\n👋 หยุดระบบแล้ว")
    
    def show_status(self):
        """แสดงสถานะปัจจุบันของระบบ"""
        print("\n" + "="*50)
        print("📊 สถานะระบบ Pozidonz Ghost Story Bot")
        print("="*50)
        
        # ข้อมูลทั่วไป
        current_mode = get_current_mode_settings()
        print(f"🔧 โหมดการทำงาน: {current_mode['name']}")
        print(f"📝 คำอธิบาย: {current_mode['description']}")
        
        # แพลตฟอร์มที่เปิดใช้งาน
        print(f"📱 แพลตฟอร์มที่เปิดใช้งาน: {len(self.controllers)} แพลตฟอร์ม")
        for platform in self.controllers.keys():
            print(f"   ✅ {platform.title()}")
        
        # ตารางเวลา
        print(f"⏰ เวลาสร้างคอนเทนต์: {len(CONTENT_CREATION_TIMES)} ช่วงเวลา")
        for creation_time in CONTENT_CREATION_TIMES:
            print(f"   🕐 {creation_time.strftime('%H:%M')}")
        
        # สถานะ Telegram
        if self.telegram_notifier:
            print("🔔 การแจ้งเตือน Telegram: เปิดใช้งาน")
        else:
            print("🔔 การแจ้งเตือน Telegram: ปิดใช้งาน")
        
        print("="*50)

def main():
    """ฟังก์ชันหลักสำหรับรันโปรแกรม"""
    bot = MultiPlatformGhostStoryBot()
    
    while True:
        print("\n" + "="*50)
        print("🎃 Pozidonz - ระบบสร้างคอนเทนต์เรื่องผีอัตโนมัติ")
        print("="*50)
        print("1. สร้างและโพสต์เรื่องผีทันที")
        print("2. รันระบบอัตโนมัติตามตารางเวลา")
        print("3. แสดงสถานะระบบ")
        print("4. ทดสอบการเชื่อมต่อแพลตฟอร์ม")
        print("5. ออกจากโปรแกรม")
        print("="*50)
        
        choice = input("เลือกตัวเลือก (1-5): ").strip()
        
        if choice == "1":
            bot.run_once()
        elif choice == "2":
            bot.run_forever()
        elif choice == "3":
            bot.show_status()
        elif choice == "4":
            bot.test_platform_connections()
        elif choice == "5":
            print("👋 ขอบคุณที่ใช้งาน!")
            break
        else:
            print("❌ กรุณาเลือกตัวเลือก 1-5")

if __name__ == "__main__":
    main()