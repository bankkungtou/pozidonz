"""
ควบคุมการอัปโหลดวิดีโอไป Instagram Reels
"""
import requests
import json
import os
import time
from setting import SAFE_HASHTAGS, DISCLAIMER_TEXT

class ReelsController:
    def __init__(self):
        """เริ่มต้นการเชื่อมต่อกับ Instagram Basic Display API"""
        self.access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN', 'your_instagram_access_token')
        self.user_id = os.getenv('INSTAGRAM_USER_ID', 'your_instagram_user_id')
        self.base_url = "https://graph.instagram.com"
        
    def create_post_caption(self, story_data):
        """สร้างข้อความสำหรับโพสต์ Instagram Reels"""
        caption = f"{story_data['title']}\n\n"
        
        # เพิ่มเนื้อหาสั้นๆ
        if len(story_data.get('story', '')) > 100:
            caption += f"{story_data['story'][:100]}...\n\n"
        else:
            caption += f"{story_data['story']}\n\n"
        
        # เพิ่มข้อมูลเพิ่มเติม
        if story_data.get('location'):
            caption += f"📍 {story_data['location']}\n"
        if story_data.get('time_period'):
            caption += f"⏰ {story_data['time_period']}\n"
        if story_data.get('moral'):
            caption += f"💡 {story_data['moral']}\n\n"
        
        # เพิ่ม disclaimer
        caption += DISCLAIMER_TEXT + "\n"
        
        # เพิ่มแฮชแท็กสำหรับ Instagram
        instagram_hashtags = [
            '#reels', '#thailand', '#thaiculture', '#storytelling',
            '#folklore', '#history', '#culture', '#education'
        ] + SAFE_HASHTAGS
        
        hashtags = " ".join(instagram_hashtags[:30])  # Instagram จำกัด 30 แฮชแท็ก
        caption += f"\n{hashtags}"
        
        return caption
    
    def upload_video_to_reels(self, video_path, story_data):
        """อัปโหลดวิดีโอไป Instagram Reels"""
        try:
            # ขั้นตอนที่ 1: สร้าง media container
            container_id = self.create_media_container(video_path, story_data)
            if not container_id:
                return False
            
            # ขั้นตอนที่ 2: รอให้ video ประมวลผลเสร็จ
            if not self.wait_for_processing(container_id):
                return False
            
            # ขั้นตอนที่ 3: เผยแพร่ Reel
            media_id = self.publish_reel(container_id)
            
            if media_id:
                print(f"✅ อัปโหลด Instagram Reels สำเร็จ: {media_id}")
                return True
            else:
                print("❌ ไม่สามารถเผยแพร่ Reel ได้")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการอัปโหลด Reels: {e}")
            return False
    
    def create_media_container(self, video_path, story_data):
        """สร้าง media container สำหรับ Reels"""
        try:
            url = f"{self.base_url}/v17.0/{self.user_id}/media"
            
            caption = self.create_post_caption(story_data)
            
            # อัปโหลดวิดีโอไปยัง server ชั่วคราวก่อน (ต้องมี public URL)
            video_url = self.upload_to_temp_server(video_path)
            if not video_url:
                return None
            
            params = {
                'media_type': 'REELS',
                'video_url': video_url,
                'caption': caption,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('id')
            else:
                print(f"ไม่สามารถสร้าง media container ได้: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการสร้าง container: {e}")
            return None
    
    def upload_to_temp_server(self, video_path):
        """อัปโหลดวิดีโอไปยัง server ชั่วคราว (ต้องใช้ service เช่น AWS S3, Cloudinary)"""
        # ในการใช้งานจริง ต้องอัปโหลดไปยัง cloud storage
        # และ return public URL
        
        # ตัวอย่างการใช้ Cloudinary (ต้องติดตั้ง cloudinary package)
        try:
            import cloudinary
            import cloudinary.uploader
            
            # ตั้งค่า Cloudinary
            cloudinary.config(
                cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
                api_key=os.getenv('CLOUDINARY_API_KEY'),
                api_secret=os.getenv('CLOUDINARY_API_SECRET')
            )
            
            # อัปโหลดวิดีโอ
            result = cloudinary.uploader.upload(
                video_path,
                resource_type="video",
                folder="ghost_stories"
            )
            
            return result.get('secure_url')
            
        except ImportError:
            print("⚠️ ต้องติดตั้ง cloudinary package หรือใช้ cloud storage อื่น")
            return None
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการอัปโหลดไฟล์: {e}")
            return None
    
    def wait_for_processing(self, container_id, max_wait=300):
        """รอให้วิดีโอประมวลผลเสร็จ"""
        try:
            url = f"{self.base_url}/v17.0/{container_id}"
            params = {
                'fields': 'status_code',
                'access_token': self.access_token
            }
            
            start_time = time.time()
            while time.time() - start_time < max_wait:
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('status_code')
                    
                    if status == 'FINISHED':
                        print("✅ วิดีโอประมวลผลเสร็จแล้ว")
                        return True
                    elif status == 'ERROR':
                        print("❌ เกิดข้อผิดพลาดในการประมวลผลวิดีโอ")
                        return False
                    else:
                        print(f"⏳ กำลังประมวลผล... ({status})")
                        time.sleep(10)
                else:
                    print(f"ไม่สามารถตรวจสอบสถานะได้: {response.status_code}")
                    return False
            
            print("⏰ หมดเวลารอการประมวลผล")
            return False
            
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการรอประมวลผล: {e}")
            return False
    
    def publish_reel(self, container_id):
        """เผยแพร่ Reel"""
        try:
            url = f"{self.base_url}/v17.0/{self.user_id}/media_publish"
            
            params = {
                'creation_id': container_id,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('id')
            else:
                print(f"ไม่สามารถเผยแพร่ Reel ได้: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการเผยแพร่: {e}")
            return None
    
    def test_connection(self):
        """ทดสอบการเชื่อมต่อกับ Instagram API"""
        try:
            url = f"{self.base_url}/v17.0/{self.user_id}"
            params = {
                'fields': 'id,username',
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ เชื่อมต่อ Instagram API สำเร็จ: @{result.get('username')}")
                return True
            else:
                print(f"❌ ไม่สามารถเชื่อมต่อ Instagram API ได้: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการทดสอบการเชื่อมต่อ: {e}")
            return False

if __name__ == "__main__":
    # ทดสอบการทำงาน
    reels = ReelsController()
    
    if reels.test_connection():
        print("Instagram Reels API พร้อมใช้งาน")
    else:
        print("กรุณาตรวจสอบการตั้งค่า Instagram API")