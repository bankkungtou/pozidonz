"""
แปลงข้อความเป็นเสียงภาษาไทย
"""
import pyttsx3
import os
from gtts import gTTS
from setting import TTS_LANGUAGE, TTS_SPEED, AUDIO_DIR

class TextToSpeech:
    def __init__(self):
        """เริ่มต้น Text-to-Speech engine"""
        self.engine = pyttsx3.init()
        self.setup_voice()
    
    def setup_voice(self):
        """ตั้งค่าเสียง"""
        voices = self.engine.getProperty('voices')
        # หาเสียงภาษาไทย (ถ้ามี)
        for voice in voices:
            if 'thai' in voice.name.lower() or 'th' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # ตั้งค่าความเร็วในการพูด
        self.engine.setProperty('rate', int(200 * TTS_SPEED))
    
    def text_to_speech_pyttsx3(self, text, output_file):
        """แปลงข้อความเป็นเสียงด้วย pyttsx3"""
        try:
            full_path = os.path.join(AUDIO_DIR, output_file)
            self.engine.save_to_file(text, full_path)
            self.engine.runAndWait()
            return full_path
        except Exception as e:
            print(f"เกิดข้อผิดพลาดใน pyttsx3: {e}")
            return None
    
    def text_to_speech_gtts(self, text, output_file):
        """แปลงข้อความเป็นเสียงด้วย Google TTS (แนะนำสำหรับภาษาไทย)"""
        try:
            full_path = os.path.join(AUDIO_DIR, output_file)
            
            # สร้างไฟล์เสียงด้วย gTTS
            tts = gTTS(text=text, lang=TTS_LANGUAGE, slow=False)
            tts.save(full_path)
            
            print(f"สร้างไฟล์เสียงสำเร็จ: {full_path}")
            return full_path
            
        except Exception as e:
            print(f"เกิดข้อผิดพลาดใน gTTS: {e}")
            return None
    
    def create_audio_from_script(self, script, story_title):
        """สร้างไฟล์เสียงจากสคริปต์"""
        if not script:
            return None
        
        # สร้างชื่อไฟล์จากชื่อเรื่องและเวลา
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{story_title}_{timestamp}.mp3"
        
        # ลองใช้ gTTS ก่อน (ดีกว่าสำหรับภาษาไทย)
        audio_file = self.text_to_speech_gtts(script, filename)
        
        # ถ้า gTTS ไม่ได้ ให้ลอง pyttsx3
        if not audio_file:
            filename_wav = filename.replace('.mp3', '.wav')
            audio_file = self.text_to_speech_pyttsx3(script, filename_wav)
        
        return audio_file

if __name__ == "__main__":
    # ทดสอบการทำงาน
    tts = TextToSpeech()
    
    test_script = """
    ผีแม่นาค
    
    เรื่องราวของแม่นาคที่เกิดขึ้นในสมัยรัชกาลที่ 4 
    ที่บ้านพระโขนง กรุงเทพมหานคร
    
    นางนาคได้เสียชีวิตขณะตั้งครรภ์ 
    แต่ยังคงรอคอยสามีที่ไปรบกลับมา
    
    นี่คือเรื่องจริงที่เกิดขึ้นในประเทศไทย
    """
    
    audio_file = tts.create_audio_from_script(test_script, "ผีแม่นาค")
    if audio_file:
        print(f"สร้างไฟล์เสียงสำเร็จ: {audio_file}")