"""
สร้างภาพพื้นหลังและรวมเป็นวิดีโอ
"""
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from setting import (
    IMAGE_WIDTH, IMAGE_HEIGHT, BACKGROUND_COLOR, TEXT_COLOR,
    FONT_PATH, FONT_SIZE, IMAGE_DIR, VIDEO_DIR
)

class VideoGenerator:
    def __init__(self):
        """เริ่มต้นตัวสร้างวิดีโอ"""
        self.setup_font()
    
    def setup_font(self):
        """ตั้งค่าฟ้อนต์"""
        try:
            self.font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        except:
            # ถ้าไม่มีฟ้อนต์ที่กำหนด ใช้ฟ้อนต์เริ่มต้น
            try:
                # ลองหาฟ้อนต์ไทยในระบบ
                self.font = ImageFont.truetype("arial.ttf", FONT_SIZE)
            except:
                self.font = ImageFont.load_default()
    
    def create_background_image(self, title, output_filename):
        """สร้างภาพพื้นหลังสีดำพร้อมชื่อเรื่องสีแดง"""
        # สร้างภาพพื้นหลังสีดำ
        img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)
        
        # คำนวณตำแหน่งข้อความให้อยู่กึ่งกลาง
        bbox = draw.textbbox((0, 0), title, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (IMAGE_WIDTH - text_width) // 2
        y = (IMAGE_HEIGHT - text_height) // 2
        
        # วาดข้อความสีแดง
        draw.text((x, y), title, font=self.font, fill=TEXT_COLOR)
        
        # เพิ่มเอฟเฟกต์เงาให้ดูน่ากลัวขึ้น
        shadow_offset = 3
        draw.text((x + shadow_offset, y + shadow_offset), title, 
                 font=self.font, fill=(100, 0, 0))  # เงาสีแดงเข้ม
        draw.text((x, y), title, font=self.font, fill=TEXT_COLOR)
        
        # บันทึกภาพ
        full_path = os.path.join(IMAGE_DIR, output_filename)
        img.save(full_path, 'JPEG', quality=95)
        
        print(f"สร้างภาพพื้นหลังสำเร็จ: {full_path}")
        return full_path
    
    def create_video_from_audio_and_image(self, image_path, audio_path, output_filename):
        """รวมภาพและเสียงเป็นวิดีโอ"""
        try:
            # โหลดไฟล์เสียง
            audio_clip = AudioFileClip(audio_path)
            
            # สร้างคลิปภาพที่มีความยาวเท่ากับเสียง
            image_clip = ImageClip(image_path, duration=audio_clip.duration)
            
            # รวมภาพและเสียง
            video_clip = image_clip.set_audio(audio_clip)
            
            # บันทึกวิดีโอ
            full_path = os.path.join(VIDEO_DIR, output_filename)
            video_clip.write_videofile(
                full_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            # ปิดคลิป
            audio_clip.close()
            image_clip.close()
            video_clip.close()
            
            print(f"สร้างวิดีโอสำเร็จ: {full_path}")
            return full_path
            
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการสร้างวิดีโอ: {e}")
            return None
    
    def generate_complete_video(self, story_data, audio_file):
        """สร้างวิดีโอสมบูรณ์จากข้อมูลเรื่องและไฟล์เสียง"""
        if not story_data or not audio_file:
            return None
        
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # สร้างภาพพื้นหลัง
        image_filename = f"{story_data['title']}_{timestamp}.jpg"
        image_path = self.create_background_image(story_data['title'], image_filename)
        
        if not image_path:
            return None
        
        # สร้างวิดีโอ
        video_filename = f"{story_data['title']}_{timestamp}.mp4"
        video_path = self.create_video_from_audio_and_image(
            image_path, audio_file, video_filename
        )
        
        return video_path

if __name__ == "__main__":
    # ทดสอบการทำงาน
    generator = VideoGenerator()
    
    # ทดสอบสร้างภาพพื้นหลัง
    test_title = "ผีแม่นาค"
    image_path = generator.create_background_image(test_title, "test_image.jpg")
    
    if image_path:
        print(f"สร้างภาพทดสอบสำเร็จ: {image_path}")