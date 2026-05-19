"""
محرك التحليل الذكي لسماء - Sky Analyzer v4.0
النسخة الاحترافية الكاملة | Arabic OCR محسن + Vision Models متعددة + معالجة ملفات شاملة
"""

import requests
from bs4 import BeautifulSoup
import os
import re
import base64
import logging
from pathlib import Path
from typing import Dict, Optional, List, Any
from io import BytesIO
import time

# ====================== Retry متقدم ======================
from tenacity import (
    retry, stop_after_attempt, wait_exponential,
    retry_if_exception_type, before_log, after_log
)

# ====================== OCR + معالجة صور ======================
try:
    import pytesseract
    import cv2
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logging.warning("pytesseract أو OpenCV غير مثبتين. OCR معطل.")

logger = logging.getLogger(__name__)


class SkyAnalyzer:
    """محرك التحليل الذكي المتقدم لسماء - النسخة الاحترافية"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    # ====================== تنظيف النص ======================
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\!\?\,\:\;\-\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]', ' ', text)
        return text.strip()

    # ====================== Retry Decorator ======================
    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1.4, min=2, max=20),
        retry=retry_if_exception_type((requests.exceptions.Timeout,
                                       requests.exceptions.ConnectionError,
                                       requests.exceptions.HTTPError)),
        before=before_log(logger, logging.DEBUG),
        after=after_log(logger, logging.WARNING)
    )
    def _fetch_url(self, url: str) -> requests.Response:
        return self.session.get(url, timeout=22, allow_redirects=True)

    # ====================== تحليل الروابط ======================
    def analyze_url(self, url: str) -> Dict:
        try:
            response = self._fetch_url(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            for tag in ["script", "style", "nav", "footer", "header", "aside", "form", "noscript"]:
                for element in soup.select(tag):
                    element.decompose()

            title = soup.title.string.strip() if soup.title else "بدون عنوان"
            meta_desc = soup.find("meta", attrs={"name": "description"})
            description = meta_desc["content"].strip() if meta_desc else ""

            paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'article', 'main', 'section'])
            content = " ".join(p.get_text(strip=True) for p in paragraphs)

            cleaned = self.clean_text(content)
            display_text = (cleaned[:3800] + "\n\n...(مقتطف من المقال)...\n\n" + cleaned[-2000:]
                           if len(cleaned) > 6000 else cleaned)

            return {
                "success": True,
                "title": title,
                "description": description,
                "text": display_text,
                "full_text": cleaned,
                "length": len(cleaned),
                "url": url,
                "status_code": response.status_code
            }

        except Exception as e:
            logger.error(f"فشل تحليل الرابط {url}: {e}")
            return {"success": False, "url": url, "error": str(e)}

    # ====================== تحسين الصورة للعربية ======================
    def _preprocess_image_for_arabic(self, image_path: str) -> Optional[Any]:
        """معالجة متقدمة لتحسين دقة OCR العربي"""
        if not OCR_AVAILABLE:
            return None
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None

            # تحويل إلى رمادي
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # تحسين التباين
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray = clahe.apply(gray)

            # إزالة الضوضاء
            gray = cv2.bilateralFilter(gray, 9, 75, 75)

            # عتبة تكيفية
            thresh = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 31, 2
            )

            # توسيع النص قليلاً (مفيد للعربية)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
            thresh = cv2.dilate(thresh, kernel, iterations=1)

            return thresh
        except Exception as e:
            logger.warning(f"فشل معالجة الصورة للعربية: {e}")
            return None

    # ====================== OCR متعدد الاستراتيجيات ======================
    def _perform_ocr(self, image_path: str, lang: str = 'ara+eng') -> str:
        if not OCR_AVAILABLE:
            return ""

        try:
            # الاستراتيجية 1: معالجة متقدمة للعربية
            processed = self._preprocess_image_for_arabic(image_path)
            if processed is not None:
                custom_config = r'--oem 3 --psm 6 -l ara+eng'
                text1 = pytesseract.image_to_string(processed, config=custom_config, lang=lang)
            else:
                text1 = ""

            # الاستراتيجية 2: الصورة الأصلية
            try:
                img = Image.open(image_path)
                text2 = pytesseract.image_to_string(img, lang=lang)
            except:
                text2 = ""

            # دمج النتائج وتنظيف
            combined = text1 + " " + text2
            return self.clean_text(combined)
        except Exception as e:
            logger.warning(f"فشل OCR: {e}")
            return ""

    # ====================== تحليل الصور بـ Gemini ======================
    def analyze_image_with_gemini(self, image_path: str, api_key: str) -> Dict:
        if not api_key:
            return {"success": False, "error": "مفتاح Gemini غير متوفر"}

        try:
            with open(image_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

            payload = {
                "contents": [{
                    "parts": [
                        {
                            "text": "أنتِ سماء. صف هذه الصورة بدقة عالية. "
                                    "استخرج كل النصوص الموجودة (خاصة العربية)، "
                                    "وصف المحتوى، الألوان، السياق، والعناصر المهمة."
                        },
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
                    ]
                }]
            }

            r = requests.post(url, json=payload, timeout=45)
            r.raise_for_status()
            description = r.json()['candidates'][0]['content']['parts'][0]['text']

            return {"success": True, "description": description, "method": "gemini"}

        except Exception as gemini_error:
            logger.warning(f"فشل Gemini Vision: {gemini_error}")

            # Fallback إلى OCR محسن
            if OCR_AVAILABLE:
                ocr_text = self._perform_ocr(image_path)
                if ocr_text.strip():
                    return {
                        "success": True,
                        "description": f"[استخراج نصي عبر OCR محسن]\n{ocr_text}",
                        "method": "ocr"
                    }

            return {"success": False, "error": "فشل Gemini و OCR", "method": "failed"}

    # ====================== تحليل الملفات ======================
    def analyze_file(self, file_path: str, filename: str) -> Dict:
        ext = filename.lower().split('.')[-1] if '.' in filename else ''

        try:
            if ext == 'pdf':
                return self._read_pdf(file_path)
            elif ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                return self._analyze_image_file(file_path, filename)
            elif ext in ['txt', 'md', 'py', 'js', 'html', 'css', 'json', 'csv']:
                return self._read_text(file_path)
            elif ext == 'docx':
                return self._read_docx(file_path)
            else:
                return {"success": True, "type": ext, "text": f"[ملف {ext}]", "note": "غير مدعوم نصياً حالياً"}
        except Exception as e:
            logger.error(f"خطأ تحليل ملف {filename}: {e}")
            return {"success": False, "filename": filename, "error": str(e)}

    def _analyze_image_file(self, file_path: str, filename: str) -> Dict:
        return {
            "success": True,
            "type": "image",
            "text": f"[صورة: {filename}]",
            "note": "يمكن تحليلها عبر Gemini Vision أو OCR محسن"
        }

    def _read_text(self, file_path: str) -> Dict:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return {"success": True, "type": "text", "text": self.clean_text(content)[:9000]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _read_pdf(self, file_path: str) -> Dict:
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages[:12]:
                    text += page.extract_text() or ""
            return {"success": True, "type": "pdf", "text": self.clean_text(text)[:10000]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _read_docx(self, file_path: str) -> Dict:
        try:
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
            return {"success": True, "type": "docx", "text": self.clean_text(text)[:9000]}
        except Exception as e:
            return {"success": False, "error": str(e)}


# ====================== Instance عالمي ======================
analyzer = SkyAnalyzer()

# ====================== دوال توافقية ======================
def analyze_url(url: str) -> Dict:
    return analyzer.analyze_url(url)

def analyze_file(file_path: str, filename: str) -> Dict:
    return analyzer.analyze_file(file_path, filename)

def analyze_image_with_gemini(image_path: str, api_key: str) -> Dict:
    return analyzer.analyze_image_with_gemini(image_path, api_key)
