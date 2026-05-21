# ============================================================
# SkyOS Backend — Dockerfile لـ Railway (معدل ومحسن)
# متوافق مع Railway + يدعم جميع الميزات السابقة
# ============================================================

# 1) استخدام نسخة بايثون مستقرة مع Debian Bullseye (متوافق مع Railway)
FROM python:3.11-slim-bullseye

# منع بايثون من كتابة ملفات pyc وتفعيل الـ Logs الفورية
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تعيين منفذ Railway (يتم استبداله تلقائياً بـ $PORT)
ENV PORT=8000

# 2) تثبيت حزم النظام الأساسية (تم تصحيح الأخطاء لـ Railway)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Tesseract OCR للتعرف على النصوص (يدعم العربية والإنجليزية)
    tesseract-ocr \
    tesseract-ocr-ara \
    tesseract-ocr-eng \
    # بديل libgl1-mesa-glx (غير متوفر في Bullseye)
    libgl1 \
    libglib2.0-0 \
    # أدوات التطوير الأساسية
    gcc \
    python3-dev \
    # مكتبات إضافية لـ OpenCV والصور
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 3) تحديد مجلد العمل الأساسي داخل الحاوية
WORKDIR /app

# 4) ترقية أداة تثبيت الحزم (Pip)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 5) نسخ ملف المتطلبات وتثبيته (لاستخدام الـ Docker Cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6) تثبيت Gunicorn صراحة (ضمان التوافق)
RUN pip install --no-cache-dir gunicorn

# 7) نسخ كافة ملفات المشروع إلى الحاوية
COPY . .

# 8) إنشاء مجلد المرفقات والصور المؤقتة مع صلاحيات كاملة
RUN mkdir -p /tmp/sky_uploads && chmod -R 777 /tmp/sky_uploads

# 9) إنشاء مجلدات static إذا لم تكن موجودة
RUN mkdir -p /app/static/css /app/static/js /app/static/icons

# 10) فتح المنفذ (Railway سيستخدم $PORT تلقائياً)
EXPOSE 8000

# 11) أمر التشغيل لـ Railway (يستخدم $PORT الديناميكي)
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120
