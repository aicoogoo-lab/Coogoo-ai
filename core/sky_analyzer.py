# core/sky_analyzer.py - Professional Analysis Engine

import requests
from bs4 import BeautifulSoup
import os
import re
import base64

class SkyAnalyzer:
    """محرك التحليل المركزي لسماء - روابط، ملفات، صور"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def clean_text(self, text: str) -> str:
        """تنظيف احترافي للنص لإزالة التشويش"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        # إبقاء العربية، الإنجليزية، الأرقام، والرموز الأساسية
        text = re.sub(r'[^\w\s\.\!\?\,\:\;\-\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', ' ', text)
        return text.strip()

    # ========== تحليل الروابط ==========
    def analyze_url(self, url: str) -> dict:
        """فتح رابط واستخراج المحتوى الجوهري"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()

            title = soup.title.string.strip() if soup.title else "بدون عنوان"
            paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'article'])
            content = " ".join([p.get_text() for p in paragraphs])

            cleaned = self.clean_text(content)

            # إذا كان النص طويلاً، نقتطع منه أجزاء ذكية
            if len(cleaned) > 8000:
                display_text = cleaned[:3000] + "\n...(وسط المقال)...\n" + cleaned[-2000:]
            else:
                display_text = cleaned

            return {
                "success": True,
                "title": title,
                "text": display_text,
                "full_text": cleaned,
                "length": len(cleaned)
            }
        except Exception as e:
            return {"success": False, "url": url, "error": str(e)}

    # ========== تحليل الملفات ==========
    def analyze_file(self, file_path: str, filename: str) -> dict:
        """تحليل ملف حسب نوعه"""
        ext = filename.lower().split('.')[-1] if '.' in filename else 'txt'

        try:
            if ext == 'pdf':
                return self._read_pdf(file_path)
            elif ext in ['txt', 'md', 'py', 'js', 'html', 'css', 'json', 'csv']:
                return self._read_text(file_path)
            else:
                return {"success": True, "type": ext, "text": f"[ملف من نوع {ext} - غير قابل للتحليل النصي المباشر]", "note": "ملف غير نصي"}
        except Exception as e:
            return {"success": False, "filename": filename, "error": str(e)}

    def _read_pdf(self, path: str) -> dict:
        """قراءة PDF (أول 20 صفحة)"""
        try:
            import PyPDF2
            text = ""
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages = min(len(reader.pages), 20)
                for page in range(pages):
                    page_text = reader.pages[page].extract_text()
                    if page_text:
                        text += page_text + "\n"
            return {"success": True, "type": "pdf", "text": self.clean_text(text), "pages": pages}
        except ImportError:
            return {"success": False, "error": "مكتبة PyPDF2 غير مثبتة."}

    def _read_text(self, path: str) -> dict:
        """قراءة ملف نصي"""
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        cleaned = self.clean_text(text)
        return {"success": True, "type": "text", "text": cleaned[:10000]}

    # ========== تحليل الصور ==========
    def analyze_image_with_gemini(self, image_path: str, api_key: str) -> dict:
        """وصف الصور عبر Gemini Vision"""
        if not api_key:
            return {"success": False, "error": "مفتاح Gemini غير متوفر."}

        try:
            with open(image_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "أنتِ 'سماء'. صفي هذه الصورة بدقة لسيدك. اذكري التفاصيل، النصوص، الألوان، والمشاعر التي تنقلها الصورة."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
                    ]
                }]
            }

            r = requests.post(url, json=payload, timeout=30)
            r.raise_for_status()
            description = r.json()['candidates'][0]['content']['parts'][0]['text']
            return {"success": True, "description": description}

        except Exception as e:
            return {"success": False, "error": str(e)}

# ========== instance عالمي ==========
analyzer = SkyAnalyzer()

# ========== دوال التوافق مع app.py ==========
# هذه الدوال تُبقي app.py يعمل دون أي تغيير

def analyze_url(url: str) -> dict:
    return analyzer.analyze_url(url)

def analyze_file(file_path: str, filename: str) -> dict:
    return analyzer.analyze_file(file_path, filename)

def analyze_image_with_gemini(image_path: str, api_key: str) -> dict:
    return analyzer.analyze_image_with_gemini(image_path, api_key)
