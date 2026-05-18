# core/sky_analyzer.py
# قدرات سماء اللامحدودة على قراءة وتحليل الملفات والروابط والصور والفيديو

import requests
from bs4 import BeautifulSoup
import os
import tempfile
from werkzeug.utils import secure_filename
from datetime import datetime

# الحد الأقصى لعدد الأحرف التي تُمرر مباشرة إلى النموذج اللغوي في سياق الرد
MAX_CONTEXT_CHARS = 8000

# --- 1. تحليل الروابط (ذكي ضد الاختناق) ---

def analyze_url(url: str) -> dict:
    """
    تفتح الرابط، تستخرج النص كاملاً، وتحضر نسخة ذكية لا تخنق النموذج.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # إزالة العناصر غير النصية
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()

        text = soup.get_text(separator='\n', strip=True)
        title = soup.title.string.strip() if soup.title else url

        # تنظيف النص
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        full_text = '\n'.join(lines)
        total_length = len(full_text)

        # بناء النص الذكي الذي سيُعطى للنموذج
        if total_length <= MAX_CONTEXT_CHARS:
            smart_text = full_text
        else:
            part1 = full_text[:2000]
            part2 = full_text[total_length // 2 - 1000 : total_length // 2 + 1000]
            part3 = full_text[-2000:]
            smart_text = (
                f"[هذا ملخص ذكي لمحتوى ضخم ({total_length:,} حرف). النص الكامل محفوظ في ذاكرتي.]\n\n"
                f"--- مقتطف من البداية ---\n{part1}\n\n"
                f"--- مقتطف من الوسط ---\n{part2}\n\n"
                f"--- مقتطف من النهاية ---\n{part3}"
            )

        return {
            "success": True,
            "url": url,
            "title": title,
            "text": smart_text,          # النص المُمرر للنموذج
            "full_text": full_text,       # النص الكامل للحفظ في الذاكرة
            "length": total_length
        }

    except Exception as e:
        return {"success": False, "url": url, "error": str(e)}

# --- 2. تحليل المستندات (PDF, TXT, والمزيد) ---

def analyze_file(file_path: str, original_filename: str) -> dict:
    """
    يحلل ملفاً ويستخرج النص بذكاء.
    """
    ext = original_filename.lower().split('.')[-1] if '.' in original_filename else 'txt'

    try:
        if ext == 'pdf':
            return _read_pdf(file_path, original_filename)
        elif ext in ['txt', 'md', 'py', 'js', 'html', 'css', 'json', 'csv', 'xml']:
            return _read_text(file_path, original_filename)
        else:
            return {
                "success": True,
                "filename": original_filename,
                "type": ext,
                "text": f"[ملف من نوع {ext} تم حفظه. استخدمي أدوات متخصصة لتحليله.]",
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
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return _smart_text_dict(filename, "pdf", text, len(reader.pages))
    except ImportError:
        return {"success": False, "filename": filename, "error": "مكتبة PyPDF2 غير مثبتة."}

def _read_text(file_path: str, filename: str) -> dict:
    """قراءة ملف نصي."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    return _smart_text_dict(filename, "text", text)

def _smart_text_dict(filename: str, file_type: str, raw_text: str, pages: int = None):
    """يبني قاموس النتيجة مع نص ذكي لا يختنق."""
    total_length = len(raw_text)

    if total_length <= MAX_CONTEXT_CHARS:
        display_text = raw_text
    else:
        part1 = raw_text[:2000]
        part2 = raw_text[total_length // 2 - 1000 : total_length // 2 + 1000]
        part3 = raw_text[-2000:]
        display_text = (
            f"[ملخص ذكي لملف ضخم ({total_length:,} حرف). المحتوى الكامل محفوظ في ذاكرتي.]\n\n"
            f"--- مقتطف من البداية ---\n{part1}\n\n"
            f"--- مقتطف من الوسط ---\n{part2}\n\n"
            f"--- مقتطف من النهاية ---\n{part3}"
        )

    result = {
        "success": True,
        "filename": filename,
        "type": file_type,
        "text": display_text,
        "full_text": raw_text
    }
    if pages:
        result["pages"] = pages
    return result

# --- 3. تحليل الصور والفيديو (باستخدام Gemini) ---

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
                    {"text": "حلل هذه الصورة بالتفصيل. صف كل ما تراه. اذكر النصوص، الأشخاص، الأشياء، الألوان، والمشاعر التي تنقلها الصورة."},
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
            cap.release()
            return {"success": False, "error": "الفيديو فارغ أو لا يمكن قراءته."}

        descriptions = []
        frames_to_capture = [int(total_frames * i / (num_frames + 1)) for i in range(1, num_frames + 1)]

        for frame_num in frames_to_capture:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if ret:
                temp_path = f"/tmp/sky_frame_{frame_num}.jpg"
                cv2.imwrite(temp_path, frame)

                result = analyze_image_with_gemini(temp_path, api_key)
                if result["success"]:
                    descriptions.append(f"[لقطة {frame_num}/{total_frames}]: {result['description']}")

                if os.path.exists(temp_path):
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
