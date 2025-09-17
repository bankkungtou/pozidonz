"""
ควบคุมการเชื่อมต่อกับ Gemini API และสร้างเรื่องผี
"""
import google.generativeai as genai
import random
import json
from datetime import datetime
from setting import GEMINI_API_KEY, GEMINI_MODEL, POSTED_STORIES_FILE

class GeminiController:
    def __init__(self):
        """เริ่มต้นการเชื่อมต่อกับ Gemini API"""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        
    def get_ghost_story(self):
        """ขอเรื่องผีจาก Gemini API"""
        prompt = """
        กรุณาสร้างเรื่องผีประจำวันที่น่ากลัวและน่าสนใจจากทั่วประเทศ
        เป็นเรื่องจริงหรือตำนานที่มีมาแต่อดีตจนถึงปัจจุบัน 
        
        กรุณาตอบในรูปแบบ JSON ดังนี้:
        {
            "title": "ชื่อเรื่อง",
            "story": "เนื้อเรื่องสั้นๆ ประมาณ 200-300 คำ เหมาะสำหรับอ่านใน TikTok/Reels/Short",
            "location": "สถานที่เกิดเหตุ",
            "time_period": "ช่วงเวลาที่เกิดเหตุ"
        }
        
        เรื่องต้องน่ากลัว น่าสนใจ 
        """
        
        try:
            response = self.model.generate_content(prompt)
            story_data = json.loads(response.text)
            
            # ตรวจสอบว่าเรื่องนี้เคยโพสต์ไปแล้วหรือไม่
            if not self.is_story_posted(story_data['title']):
                return story_data
            else:
                # ถ้าเรื่องซ้ำ ให้ขอเรื่องใหม่
                return self.get_ghost_story()
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการขอเรื่องผี: {e}")
            return None
    
    def is_story_posted(self, title):
        """ตรวจสอบว่าเรื่องนี้เคยโพสต์ไปแล้วหรือไม่"""
        try:
            with open(POSTED_STORIES_FILE, 'r', encoding='utf-8') as f:
                posted_stories = f.read()
                return title in posted_stories
        except FileNotFoundError:
            return False
    
    def mark_story_as_posted(self, story_data):
        """บันทึกเรื่องที่โพสต์แล้ว"""
        try:
            with open(POSTED_STORIES_FILE, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp} - {story_data['title']}\n")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการบันทึกประวัติ: {e}")
    
    def create_script(self, story_data):
        """สร้างสคริปต์สำหรับอ่าน"""
        if not story_data:
            return None
            
        script = f"""
        {story_data['title']}
        
        {story_data['story']}
        
        เกิดขึ้นที่ {story_data['location']} 
        ในช่วง {story_data['time_period']}
        
        นี่คือเรื่องจริงที่เกิดขึ้นในประเทศไทย
        หากใครมีเรื่องผีน่ากลัวอื่นๆ สามารถแชร์ได้ในคอมเมนต์
        """
        
        return script.strip()

if __name__ == "__main__":
    # ทดสอบการทำงาน
    gemini = GeminiController()
    story = gemini.get_ghost_story()
    if story:
        print("ได้เรื่องผีแล้ว:")
        print(json.dumps(story, ensure_ascii=False, indent=2))
        
        script = gemini.create_script(story)
        print("\nสคริปต์:")
        print(script)