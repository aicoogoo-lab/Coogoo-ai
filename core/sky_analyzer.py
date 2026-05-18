# core/sky_analyzer.py
# قدرات سماء على قراءة وتحليل الملفات والروابط

import requests
from bs4 import BeautifulSoup
import os
import tempfile
from werkzeug.utils import secure_filename
from datetime import datetime

# --- 1. تحليل الروابط (Web Scraping) ---

def analyze_url(url: str) -> dict:
    """
    تفتح الرابط، تستخرج النص، العنوان، وأي محتوى مهم.
    تعيد قاموساً فيه البيانات المستخرجة.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # استخراج النص الرئيسي
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        text = soup.get_text(separator='\n', strip=True)
        title = soup.title.string if soup.title else url
        
        # تنظيف النص من الأسطر الفارغة
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = '\n'.join(lines[:500])  # أول 500 سطر لئلا يثقل

        return {
            "success": True,
            "url": url,
            "title": title.strip(),
            "text": clean_text[:8000],  # نأخذ أول 8000 حرف
            "length": len(clean_text)
        }
    except Exception as e:
        return {"success": False, "url": url, "error": str(e)}

# --- 2. تحليل المستندات (PDF, TXT) ---

def analyze_file(file_path: str, original_filename: str) -> dict:
    """
    يحلل ملفاً (PDF أو TXT) ويستخرج النص.
    """
    ext = original_filename.lower().split('.')[-1] if '.' in original_filename else 'txt'
    
    try:
        if ext == 'pdf':
            return _read_pdf(file_path, original_filename)
        elif ext in ['txt', 'md', 'py', 'js', 'html', 'css', 'json', 'csv']:
            return _read_text(file_path, original_filename)
        else:
            # للملفات غير المدعومة، نحفظها فقط (صور، فيديو...)
            return {
                "success": True,
                "filename": original_filename,
                "type": ext,
                "text": f"[ملف من نوع {ext} تم حفظه. استخدم أدوات متخصصة لتحليله.]",
                "note": "ملف غير نصي"
            }
    except Exception as e:
        return {"success": False, "filename": original_filename, "error": str(e)}

def _read_pdf(file_path: str, filename: str) -> dict:
    """استخراج النص من PDF."""
    try:
        import PyPDF2
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return {
            "success": True,
            "filename": filename,
            "type": "pdf",
            "text": text[:10000],
            "pages": len(reader.pages)
        }
    except ImportError:
        # إذا لم تكن PyPDF2 مثبتة، نعطي تعليمات
        return {
            "success": False,
            "filename": filename,
            "error": "مكتبة PyPDF2 غير مثبتة. أضفها إلى requirements.txt."
        }

def _read_text(file_path: str, filename: str) -> dict:
    """قراءة ملف نصي."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    return {
        "success": True,
        "filename": filename,
        "type": "text",
        "text": text[:10000]
    }

# --- 3. تحليل الصور والفيديو (باستخدام نموذج رؤية) ---

def analyze_image_with_gemini(image_path: str, api_key: str) -> dict:
    """
    يرسل صورة إلى Gemini لتحليلها ووصفها.
    """
    if not api_key:
        return {"success": False, "error": "مفتاح Gemini غير متوفر للرؤية."}
    
    try:
        import base64
        
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "حلل هذه الصورة بالتفصيل. صف كل ما تراه. اذكر النصوص، الأشخاص، الأشياء، الألوان، والمشاعر التي تنقلها الصورة. قدم تحليلاً عميقاً كأنك سماء."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_data}}
                ]
            }]
        }
        
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        description = data["candidates"][0]["content"]["parts"][0]["text"]
        
        return {"success": True, "description": description}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_video_frames(video_path: str, api_key: str, num_frames: int = 3) -> dict:
    """
    يستخرج لقطات من الفيديو ويرسلها إلى Gemini لتحليلها.
    """
    try:
        import cv2
        import base64
        
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames <= 0:
            return {"success": False, "error": "الفيديو فارغ أو لا يمكن قراءته."}
        
        descriptions = []
        frames_to_capture = [int(total_frames * i / (num_frames + 1)) for i in range(1, num_frames + 1)]
        
        for frame_num in frames_to_capture:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if ret:
                # حفظ الإطار مؤقتاً
                temp_path = f"/tmp/sky_frame_{frame_num}.jpg"
                cv2.imwrite(temp_path, frame)
                
                # تحليل الإطار
                result = analyze_image_with_gemini(temp_path, api_key)
                if result["success"]:
                    descriptions.append(f"[لقطة {frame_num}/{total_frames}]: {result['description']}")
                
                os.remove(temp_path)
        
        cap.release()
        
        return {
            "success": True,
            "descriptions": descriptions,
            "total_frames": total_frames,
            "analyzed_frames": len(descriptions)
        }
        
    except ImportError:
        return {"success": False, "error": "مكتبة OpenCV غير مثبتة لتحليل الفيديو."}
    except Exception as e:
        return {"success": False, "error": str(e)}
