"""
ควบคุมการอัปโหลดวิดีโอไป YouTube Shorts
"""
import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from setting import SAFE_HASHTAGS, DISCLAIMER_TEXT

class YouTubeController:
    def __init__(self):
        """เริ่มต้นการเชื่อมต่อกับ YouTube Data API"""
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        self.API_SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.CLIENT_SECRETS_FILE = 'client_secret.json'  # ไฟล์ credentials จาก Google Cloud Console
        self.TOKEN_FILE = 'token.pickle'
        
        self.youtube = self.authenticate()
    
    def authenticate(self):
        """ยืนยันตัวตนกับ YouTube API"""
        creds = None
        
        # โหลด token ที่บันทึกไว้
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # ถ้าไม่มี credentials ที่ใช้ได้ ให้ทำการ login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.CLIENT_SECRETS_FILE):
                    print(f"❌ ไม่พบไฟล์ {self.CLIENT_SECRETS_FILE}")
                    print("กรุณาดาวน์โหลดจาก Google Cloud Console")
                    return None
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_SECRETS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # บันทึก credentials
            with open(self.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        
        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials=creds)
    
    def create_video_metadata(self, story_data):
        """สร้าง metadata สำหรับวิดีโอ YouTube"""
        title = f"{story_data['title']} | เรื่องเล่าไทย"
        
        description = f"""
{story_data['title']}

{story_data.get('story', '')}

📍 สถานที่: {story_data.get('location', 'ไม่ระบุ')}
⏰ ช่วงเวลา: {story_data.get('time_period', 'ไม่ระบุ')}

{story_data.get('moral', '')}

{DISCLAIMER_TEXT}

#Shorts {' '.join(SAFE_HASHTAGS)}
        """.strip()
        
        # YouTube tags (คำสำคัญ)
        tags = [
            'เรื่องเล่าไทย', 'วัฒนธรรมไทย', 'ตำนานไทย', 'ประวัติศาสตร์ไทย',
            'Thai culture', 'Thai folklore', 'Thai stories', 'shorts',
            story_data.get('location', '').replace(' ', ''),
        ]
        
        # กรองแท็กที่ไม่ว่าง
        tags = [tag for tag in tags if tag.strip()]
        
        return {
            'snippet': {
                'title': title[:100],  # YouTube จำกัด 100 ตัวอักษร
                'description': description[:5000],  # YouTube จำกัด 5000 ตัวอักษร
                'tags': tags[:500],  # YouTube จำกัด 500 แท็ก
                'categoryId': '22',  # People & Blogs
                'defaultLanguage': 'th',
                'defaultAudioLanguage': 'th'
            },
            'status': {
                'privacyStatus': 'private',  # เริ่มต้นเป็น private เพื่อความปลอดภัย
                'selfDeclaredMadeForKids': False,
            }
        }
    
    def upload_video(self, video_path, story_data):
        """อัปโหลดวิดีโอไป YouTube"""
        try:
            if not self.youtube:
                print("❌ ไม่สามารถเชื่อมต่อ YouTube API ได้")
                return False
            
            print("📤 กำลังอัปโหลดไป YouTube...")
            
            # สร้าง metadata
            body = self.create_video_metadata(story_data)
            
            # สร้าง MediaFileUpload object
            media = MediaFileUpload(
                video_path,
                chunksize=-1,  # อัปโหลดทั้งไฟล์ในครั้งเดียว
                resumable=True,
                mimetype='video/mp4'
            )
            
            # เริ่มการอัปโหลด
            insert_request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            # ทำการอัปโหลดแบบ resumable
            video_id = self.resumable_upload(insert_request)
            
            if video_id:
                print(f"✅ อัปโหลด YouTube สำเร็จ: https://youtu.be/{video_id}")
                return video_id
            else:
                print("❌ การอัปโหลดล้มเหลว")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการอัปโหลด YouTube: {e}")
            return False
    
    def resumable_upload(self, insert_request):
        """อัปโหลดแบบ resumable"""
        response = None
        error = None
        retry = 0
        
        while response is None:
            try:
                print("⏳ กำลังอัปโหลด...")
                status, response = insert_request.next_chunk()
                
                if response is not None:
                    if 'id' in response:
                        return response['id']
                    else:
                        print(f"❌ การอัปโหลดล้มเหลว: {response}")
                        return None
                        
            except Exception as e:
                error = e
                retry += 1
                
                if retry > 3:
                    print(f"❌ การอัปโหลดล้มเหลวหลังจากลองใหม่ 3 ครั้ง: {error}")
                    return None
                
                print(f"⚠️ เกิดข้อผิดพลาด ลองใหม่ครั้งที่ {retry}: {error}")
        
        return None
    
    def update_video_privacy(self, video_id, privacy_status='public'):
        """เปลี่ยนสถานะความเป็นส่วนตัวของวิดีโอ"""
        try:
            self.youtube.videos().update(
                part='status',
                body={
                    'id': video_id,
                    'status': {
                        'privacyStatus': privacy_status
                    }
                }
            ).execute()
            
            print(f"✅ เปลี่ยนสถานะวิดีโอเป็น {privacy_status}")
            return True
            
        except Exception as e:
            print(f"❌ ไม่สามารถเปลี่ยนสถานะได้: {e}")
            return False
    
    def get_channel_info(self):
        """ดึงข้อมูลช่อง YouTube"""
        try:
            if not self.youtube:
                return None
            
            response = self.youtube.channels().list(
                part='snippet,statistics',
                mine=True
            ).execute()
            
            if response['items']:
                channel = response['items'][0]
                return {
                    'title': channel['snippet']['title'],
                    'subscriber_count': channel['statistics'].get('subscriberCount', 0),
                    'video_count': channel['statistics'].get('videoCount', 0)
                }
            
            return None
            
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการดึงข้อมูลช่อง: {e}")
            return None
    
    def test_connection(self):
        """ทดสอบการเชื่อมต่อกับ YouTube API"""
        try:
            channel_info = self.get_channel_info()
            
            if channel_info:
                print(f"✅ เชื่อมต่อ YouTube API สำเร็จ")
                print(f"   ช่อง: {channel_info['title']}")
                print(f"   ผู้ติดตาม: {channel_info['subscriber_count']}")
                print(f"   วิดีโอ: {channel_info['video_count']}")
                return True
            else:
                print("❌ ไม่สามารถเชื่อมต่อ YouTube API ได้")
                return False
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการทดสอบการเชื่อมต่อ: {e}")
            return False

if __name__ == "__main__":
    # ทดสอบการทำงาน
    youtube = YouTubeController()
    
    if youtube.test_connection():
        print("YouTube API พร้อมใช้งาน")
    else:
        print("กรุณาตรวจสอบการตั้งค่า YouTube API")