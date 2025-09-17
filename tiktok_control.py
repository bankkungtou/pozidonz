"""
ควบคุมการอัปโหลดวิดีโอไป TikTok
"""
import requests
import json
import os
from setting import (
    TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_ACCESS_TOKEN,
    IMPORTANT_HASHTAGS
)

class TikTokController:
    def __init__(self):
        """เริ่มต้นการเชื่อมต่อกับ TikTok API"""
        self.client_key = TIKTOK_CLIENT_KEY
        self.client_secret = TIKTOK_CLIENT_SECRET
        self.access_token = TIKTOK_ACCESS_TOKEN
        self.base_url = "https://open-api.tiktok.com"
    
    def create_post_caption(self, story_data):
        """สร้างข้อความสำหรับโพสต์"""
        caption = f"{story_data['title']}\n\n"
        
        # เพิ่มแฮชแท็กสำคัญ
        hashtags = " ".join(IMPORTANT_HASHTAGS)
        caption += f"\n{hashtags}"
        
        # เพิ่มแฮชแท็กเฉพาะเรื่อง
        if story_data.get('location'):
            caption += f" #{story_data['location'].replace(' ', '')}"
        
        return caption
    
    def upload_video(self, video_path, story_data):
        """อัปโหลดวิดีโอไป TikTok"""
        try:
            # ขั้นตอนที่ 1: ขอ URL สำหรับอัปโหลด
            upload_url = self.get_upload_url()
            if not upload_url:
                return False
            
            # ขั้นตอนที่ 2: อัปโหลดไฟล์วิดีโอ
            video_id = self.upload_video_file(upload_url, video_path)
            if not video_id:
                return False
            
            # ขั้นตอนที่ 3: สร้างโพสต์
            post_result = self.create_post(video_id, story_data)
            
            return post_result
            
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการอัปโหลด: {e}")
            return False
    
    def get_upload_url(self):
        """ขอ URL สำหรับอัปโหลดวิดีโอ"""
        try:
            url = f"{self.base_url}/v2/post/publish/video/init/"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'source_info': {
                    'source': 'FILE_UPLOAD',
                    'video_size': os.path.getsize(video_path) if 'video_path' in locals() else 0
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('data', {}).get('upload_url')
            else:
                print(f"ไม่สามารถขอ URL อัปโหลดได้: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการขอ URL: {e}")
            return None
    
    def upload_video_file(self, upload_url, video_path):
        """อัปโหลดไฟล์วิดีโอ"""
        try:
            with open(video_path, 'rb') as video_file:
                files = {'video': video_file}
                response = requests.post(upload_url, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('data', {}).get('video_id')
                else:
                    print(f"ไม่สามารถอัปโหลดวิดีโอได้: {response.status_code}")
                    return None
                    
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการอัปโหลดไฟล์: {e}")
            return None
    
    def create_post(self, video_id, story_data):
        """สร้างโพสต์ TikTok"""
        try:
            url = f"{self.base_url}/v2/post/publish/video/init/"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            caption = self.create_post_caption(story_data)
            
            data = {
                'post_info': {
                    'title': caption,
                    'privacy_level': 'SELF_ONLY',  # เปลี่ยนเป็น 'PUBLIC_TO_EVERYONE' เมื่อพร้อม
                    'disable_duet': False,
                    'disable_comment': False,
                    'disable_stitch': False,
                    'video_cover_timestamp_ms': 1000
                },
                'source_info': {
                    'video_id': video_id,
                    'source': 'FILE_UPLOAD'
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"โพสต์สำเร็จ: {result}")
                return True
            else:
                print(f"ไม่สามารถสร้างโพสต์ได้: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการสร้างโพสต์: {e}")
            return False
    
    def test_connection(self):
        """ทดสอบการเชื่อมต่อกับ TikTok API"""
        try:
            url = f"{self.base_url}/v2/user/info/"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                print("เชื่อมต่อ TikTok API สำเร็จ")
                return True
            else:
                print(f"ไม่สามารถเชื่อมต่อ TikTok API ได้: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการทดสอบการเชื่อมต่อ: {e}")
            return False

if __name__ == "__main__":
    # ทดสอบการทำงาน
    tiktok = TikTokController()
    
    # ทดสอบการเชื่อมต่อ
    if tiktok.test_connection():
        print("TikTok API พร้อมใช้งาน")
    else:
        print("กรุณาตรวจสอบการตั้งค่า TikTok API")