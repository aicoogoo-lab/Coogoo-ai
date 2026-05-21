# 1) استخدام نسخة بايثون خفيفة ومستقرة ومناسبة للإنتاج
FROM python:3.11-slim

# منع بايثون من كتابة ملفات pyc لتقليل المساحة وضمان التدفق الفوري للـ Logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2) تثبيت حزم النظام الأساسية (Tesseract OCR للمعالجة ومكتبات الـ OpenCV للرؤية)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-ara \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 3) تحديد مجلد العمل الأساسي داخل الحاوية
WORKDIR /app

# 4) ترقية أداة تثبيت الحزم (Pip) لضمان التوافقية وسرعة البناء
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 5) نسخ ملف المتطلبات وتثبيته مستقلًا للاستفادة القصوى من الـ Docker Cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6) تثبيت Gunicorn صراحة داخل الحاوية لضمان عدم اعتماده على ملف المتطلبات الخارجي
RUN pip install --no-cache-dir gunicorn

# 7) نسخ كافة ملفات المشروع ونظام التشغيل SkyOS إلى الحاوية
COPY . .

# 8) إنشاء مجلد المرفقات والصور المؤقت مع منح الصلاحيات الكاملة للـ Workers
RUN mkdir -p /tmp/sky_uploads && chmod -R 777 /tmp/sky_uploads

# 9) فتح المنفذ 10000 المخصص لمنصة Render السحابية
EXPOSE 10000

# 10) أمر التشغيل الفائق والمستقر باستخدام Gunicorn (مع معالجة الوقت المستغرق للطلبات الثقيلة)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--workers", "2", "--threads", "2", "--timeout", "120", "app:app"]
