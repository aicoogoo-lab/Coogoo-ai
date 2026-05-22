"""
Sky Analyzer v10.3 — محرك التحليل الذكي المتكامل (مع ربط قوي بالذاكرة)
================================================================================
تحسينات هذه النسخة:
- ربط تلقائي قوي مع memory.py
- دعم اختياري للحفظ في QuantumHolographicMemory
- تنظيم أفضل وتعليقات واضحة
- معالجة أخطاء محسنة
- دوال جاهزة للاستخدام مع Core Engine
"""

import requests
from bs4 import BeautifulSoup
import re
import logging
from typing import Dict, Optional, Any

# Retry
from tenacity import (
    retry, stop_after_attempt, wait_exponential,
    retry_if_exception_type, before_log, after_log
)

# OCR + Vision
try:
    import pytesseract
    import cv2
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

# استيراد الذاكرة
try:
    from memory import save_knowledge, save_url_analysis
except ImportError:
    try:
        from core.memory import save_knowledge, save_url_analysis
    except ImportError:
        def save_knowledge(*a, **k): return False
        def save_url_analysis(*a, **k): return False

logger = logging.getLogger("SkyAnalyzer")


class SkyAnalyzer:
    """محرك التحليل الذكي المتقدم والمتكامل مع الذاكرة"""

    def __init__(self):
        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/128.0.0.0 Safari/537.36'
            )
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    # ========================================================
    # تنظيف النصوص
    # ========================================================
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'[^\w\s\.\!\?\,\:\;\-\=\+\*\/\\\'\"\`\{\}\[\]\(\)\<\>\#\@\$\%\^\&\~\|\u0600-\u06FF]', ' ', text)
        return text.strip()

    # ========================================================
    # تحليل الروابط
    # ========================================================
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1.5, min=2, max=15),
        retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.ConnectionError))
    )
    def analyze_url(self, url: str, save_to_memory: bool = True) -> Dict:
        """
        تحليل رابط + حفظ النتيجة في الذاكرة تلقائياً
        """
        try:
            response = self.session.get(url, timeout=20, allow_redirects=True)
            soup = BeautifulSoup(response.content, 'html.parser')

            for tag in ["script", "style", "nav", "footer", "header", "aside", "form", "noscript"]:
                for element in soup.select(tag):
                    element.decompose()

            title = soup.title.string.strip() if soup.title else "بدون عنوان"
            paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'article', 'main', 'section'])
            content = " ".join(p.get_text(strip=True) for p in paragraphs)
            cleaned = self.clean_text(content)

            result = {
                "success": True,
                "title": title,
                "text": cleaned[:7000],
                "full_text": cleaned,
                "length": len(cleaned),
                "url": url
            }

            # حفظ في الذاكرة
            if save_to_memory:
                try:
                    save_url_analysis(url, title, cleaned[:2000])
                    save_knowledge(f"رابط: {title}", cleaned[:1800], source=url, importance=0.8)
                except Exception:
                    pass

            return result

        except Exception as e:
            logger.error(f"فشل تحليل الرابط {url}: {e}")
            return {"success": False, "url": url, "error": str(e)}

    # ========================================================
    # OCR للصور
    # ========================================================
    def _perform_ocr(self, image_path: str) -> str:
        if not OCR_AVAILABLE:
            return ""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return ""
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray = clahe.apply(gray)
            gray = cv2.bilateralFilter(gray, 9, 75, 75)
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
            text = pytesseract.image_to_string(thresh, lang='ara+eng')
            return self.clean_text(text)
        except Exception as e:
            logger.warning(f"فشل OCR: {e}")
            return ""

    # ========================================================
    # تحليل الصور بـ Gemini Vision
    # ========================================================
    def analyze_image_with_gemini(self, image_path: str, api_key: str) -> Dict:
        if not api_key:
            return {"success": False, "error": "مفتاح Gemini غير متوفر"}

        try:
            import base64
            with open(image_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

            payload = {
                "contents": [{
                    "parts": [
                        {"text": "صف هذه الصورة بدقة عالية. استخرج النصوص والرموز والسياق."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
                    ]
                }]
            }

            r = requests.post(url, json=payload, timeout=50)
            r.raise_for_status()
            description = r.json()['candidates'][0]['content']['parts'][0]['text']

            return {"success": True, "description": description, "method": "gemini"}

        except Exception as e:
            logger.warning(f"فشل Gemini Vision: {e}")
            ocr_text = self._perform_ocr(image_path)
            if ocr_text:
                return {"success": True, "description": f"[OCR Fallback]\n{ocr_text}", "method": "ocr"}
            return {"success": False, "error": str(e)}

    # ========================================================
    # تحليل الملفات
    # ========================================================
    def analyze_file(self, file_path: str, filename: str, save_to_memory: bool = True) -> Dict:
        ext = filename.lower().split('.')[-1] if '.' in filename else ''

        try:
            if ext == 'pdf':
                result = self._read_pdf(file_path)
            elif ext in ['jpg', 'jpeg', 'png', 'webp']:
                result = {"success": True, "type": "image", "note": "يمكن تحليلها بـ Gemini Vision"}
            elif ext in ['txt', 'md', 'py', 'js', 'html', 'css', 'json']:
                result = self._read_text(file_path)
            elif ext == 'docx':
                result = self._read_docx(file_path)
            else:
                result = {"success": True, "type": ext, "note": "نوع غير مدعوم نصياً"}

            # حفظ في الذاكرة
            if save_to_memory and result.get("success"):
                try:
                    save_knowledge(
                        topic=f"ملف: {filename}",
                        content=str(result.get("text", ""))[:1500],
                        source=filename,
                        importance=0.7
                    )
                except Exception:
                    pass

            return result

        except Exception as e:
            logger.error(f"خطأ تحليل الملف {filename}: {e}")
            return {"success": False, "error": str(e)}

    def _read_text(self, file_path: str) -> Dict:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return {"success": True, "type": "text", "text": self.clean_text(content)[:15000]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _read_pdf(self, file_path: str) -> Dict:
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = "".join(page.extract_text() or "" for page in reader.pages[:12])
            return {"success": True, "type": "pdf", "text": self.clean_text(text)[:15000]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _read_docx(self, file_path: str) -> Dict:
        try:
            from docx import Document
            doc = Document(file_path)
            text = "\n".join(p.text for p in doc.paragraphs)
            return {"success": True, "type": "docx", "text": self.clean_text(text)[:15000]}
        except Exception as e:
            return {"success": False, "error": str(e)}


# ============================================================
# Instance عالمي
# ============================================================
analyzer = SkyAnalyzer()

def analyze_url(url: str) -> Dict:
    return analyzer.analyze_url(url)

def analyze_file(file_path: str, filename: str) -> Dict:
    return analyzer.analyze_file(file_path, filename)

def analyze_image_with_gemini(image_path: str, api_key: str) -> Dict:
    return analyzer.analyze_image_with_gemini(image_path, api_key)
