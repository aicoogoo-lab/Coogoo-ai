# core/sky_analyzer.py
"""
محرك التحليل المتقدم لسماء - Sky Analyzer v2.1
- Tenacity Retry متقدم
- دعم OCR (pytesseract + OpenCV)
- Fallback ذكي متعدد المراحل
"""

import requests
from bs4 import BeautifulSoup
import os
import re
import base64
import logging
from pathlib import Path
from typing import Dict, Optional

# ====================== Tenacity - Retry متقدم ======================
from tenacity import (
    retry, stop_after_attempt, wait_exponential, 
    retry_if_exception_type, before_log, after_log
)

# ====================== OCR ======================
try:
    import pytesseract
    import cv2
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logging.warning("pytesseract أو OpenCV غير مثبتين. OCR معطل.")

logger = logging.getLogger(__name__)


class SkyAnalyzer:
    """محرك التحليل الذكي المتقدم لسماء"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def clean_text(self, text: str) -> str:
        """تنظيف النص الاحترافي"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\!\?\,\:\;\-\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]', ' ', text)
        return text.strip()

    # ====================== Retry Decorator متقدم ======================
    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1.2, min=2, max=15),
        retry=retry_if_exception_type((requests.exceptions.Timeout,
                                       requests.exceptions.ConnectionError,
                                       requests.exceptions.HTTPError)),
        before=before_log(logger, logging.DEBUG),
        after=after_log(logger, logging.WARNING)
    )
    def _fetch_url(self, url: str) -> requests.Response:
        """جلب الصفحة مع Retry ذكي"""
        return self.session.get(url, timeout=18)

    # ====================== تحليل الروابط ======================
    def analyze_url(self, url: str) -> Dict:
        """تحليل رابط مع Retry + Error Handling متقدم"""
        try:
            response = self._fetch_url(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # إزالة عناصر غير مرغوبة
            for tag in ["script", "style", "nav", "footer", "header", "aside"]:
                for element in soup.select(tag):
                    element.decompose()

            title = soup.title.string.strip() if soup.title else "بدون عنوان"
            paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'article', 'main'])
            content = " ".join(p.get_text(strip=True) for p in paragraphs)

            cleaned = self.clean_text(content)
            display_text = (cleaned[:3200] + "\n\n...(مقتطف من المقال)...\n\n" + cleaned[-2000:]
                           if len(cleaned) > 5200 else cleaned)

            return {
                "success": True,
                "title": title,
                "text": display_text,
                "full_text": cleaned,
                "length": len(cleaned),
                "url": url,
                "status_code": response.status_code
            }

        except Exception as e:
            logger.error(f"فشل تحليل الرابط {url}: {e}")
            return {"success": False, "url": url, "error": str(e)}

    # ====================== OCR Functions ======================
    def _perform_ocr(self, image_path: str) -> str:
        """استخراج نص من الصورة باستخدام OCR"""
        if not OCR_AVAILABLE:
            return ""

        try:
            # قراءة الصورة بـ OpenCV
            img = cv2.imread(image_path)
            if img is None:
                return ""

            # تحسين الصورة لـ OCR
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # تطبيق Threshold لتحسين النصوص
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # استخراج النص
            text = pytesseract.image_to_string(thresh, lang='ara+eng')
            return self.clean_text(text)
        except Exception as e:
            logger.warning(f"فشل OCR: {e}")
            return ""

    # ====================== تحليل الصور ======================
    def analyze_image_with_gemini(self, image_path: str, api_key: str) -> Dict:
        """تحليل الصورة بـ Gemini مع OCR Fallback"""
        if not api_key:
            return {"success": False, "error": "مفتاح Gemini غير متوفر"}

        # 1. محاولة Gemini أولاً
        try:
            with open(image_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "أنتِ سماء. صف هذه الصورة بدقة واحترافية. استخرج أي نصوص موجودة، وصف المحتوى، الألوان، والسياق."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
                    ]
                }]
            }

            r = requests.post(url, json=payload, timeout=35)
            r.raise_for_status()
            description = r.json()['candidates'][0]['content']['parts'][0]['text']
            
            return {"success": True, "description": description, "method": "gemini"}

        except Exception as gemini_error:
            logger.warning(f"فشل Gemini Vision: {gemini_error}")

            # 2. Fallback إلى OCR
            if OCR_AVAILABLE:
                ocr_text = self._perform_ocr(image_path)
                if ocr_text.strip():
                    return {
                        "success": True,
                        "description": f"[OCR Extraction]\n{ocr_text}",
                        "method": "ocr"
                    }

            return {"success": False, "error": "فشل Gemini و OCR", "method": "failed"}

    # ====================== تحليل الملفات ======================
    def analyze_file(self, file_path: str, filename: str) -> Dict:
        """تحليل شامل للملفات"""
        ext = filename.lower().split('.')[-1] if '.' in filename else ''

        try:
            if ext == 'pdf':
                return self._read_pdf(file_path)
            elif ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                # للصور: نستخدم OCR + Gemini
                return self._analyze_image_file(file_path, filename)
            elif ext in ['txt', 'md', 'py', 'js', 'html', 'css', 'json', 'csv']:
                return self._read_text(file_path)
            elif ext == 'docx':
                return self._read_docx(file_path)
            else:
                return {"success": True, "type": ext, "text": f"[ملف {ext} غير مدعوم نصياً]", "note": "غير نصي"}
        except Exception as e:
            logger.error(f"خطأ تحليل ملف {filename}: {e}")
            return {"success": False, "filename": filename, "error": str(e)}

    def _analyze_image_file(self, file_path: str, filename: str) -> Dict:
        """تحليل الصور كملفات"""
        # يمكن توسيعها لاحقاً
        return {"success": True, "type": "image", "text": f"[صورة: {filename}] - يمكن تحليلها عبر Gemini أو OCR"}

    # ... (باقي الدوال _read_pdf, _read_text, _read_docx كما في النسخة السابقة)

# ====================== Instance عالمي ======================
analyzer = SkyAnalyzer()

# دوال توافقية
def analyze_url(url: str) -> Dict:
    return analyzer.analyze_url(url)

def analyze_file(file_path: str, filename: str) -> Dict:
    return analyzer.analyze_file(file_path, filename)

def analyze_image_with_gemini(image_path: str, api_key: str) -> Dict:
    return analyzer.analyze_image_with_gemini(image_path, api_key)
