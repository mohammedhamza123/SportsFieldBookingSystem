# نظام حجز الملاعب الرياضية - Sports Field Booking System

**الإصدار - Version:** 2.1.0  
**آخر تحديث - Last Updated:** يناير 2025 - January 2025

[![Python](https://img.shields.io/badge/Python-3.11.9-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Render](https://img.shields.io/badge/Deploy%20on-Render-46E3B7.svg)](https://render.com/)

## نظرة عامة - Overview

نظام حجز الملاعب الرياضية هو تطبيق ويب مبني باستخدام FastAPI للخلفية و HTML/CSS/JavaScript للواجهة الأمامية. النظام مصمم خصيصاً لليبيا ويشمل مدينتي طرابلس والزاوية.

The Sports Field Booking System is a web application built with FastAPI backend and HTML/CSS/JavaScript frontend. The system is specifically designed for Libya and includes Tripoli and Al-Zawiya cities.

### 🌟 الميزات الرئيسية - Key Features
- 🎯 **سهولة الاستخدام** - User-friendly interface
- 🔒 **أمان عالي** - High security with session management
- 📱 **متجاوب** - Responsive design for all devices
- 🏃‍♂️ **أداء سريع** - Fast performance with FastAPI
- 🎫 **نظام باركود** - Barcode system for bookings
- 👨‍💼 **لوحة إدارة** - Admin dashboard
- 💳 **أكواد الدفع** - Payment codes system

## المتطلبات - Requirements

### متطلبات النظام - System Requirements
- Python 3.9.18 (مطلوب لحل مشاكل التوافق مع SQLAlchemy) - Python 3.9.18 (required for SQLAlchemy compatibility)
- متصفح ويب حديث - Modern web browser
- اتصال بالإنترنت (لتنزيل الحزم) - Internet connection (for package installation)

### التوافق - Compatibility
- ✅ Python 3.10.13
- ✅ FastAPI 0.104.1
- ✅ SQLAlchemy 1.4.53
- ✅ Render.com
- ✅ Heroku (مع تعديلات بسيطة)
- ❌ Python 3.13 (غير متوافق مع SQLAlchemy الحالي)

### الأداء - Performance
- ⚡ FastAPI يوفر أداء عالي
- 🗄️ SQLAlchemy للتعامل مع قاعدة البيانات
- 🔒 نظام أمان محسن للجلسات
- 📱 واجهة متجاوبة للهواتف

### الحزم المطلوبة - Required Packages
جميع الحزم المطلوبة مدرجة في ملف `requirements.txt`

All required packages are listed in the `requirements.txt` file

## التثبيت والإعداد - Installation & Setup

### 🚀 التثبيت السريع - Quick Installation
```bash
# استنساخ المشروع
git clone https://github.com/mohammedhamza123/SportsFieldBookingSystem.git
cd SportsFieldBookingSystem

# إنشاء البيئة الافتراضية
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# تثبيت الحزم
pip install -r requirements.txt

# تشغيل التطبيق
python main.py
```

### 1. تثبيت Python - Install Python

#### Windows
1. قم بزيارة [python.org](https://www.python.org/downloads/)
2. حمل Python 3.10.13 (مطلوب لحل مشاكل التوافق مع SQLAlchemy)
3. شغل ملف التثبيت مع تفعيل "Add Python to PATH"
4. تأكد من التثبيت:
   ```bash
   python --version
   ```

#### Linux/macOS
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# macOS (using Homebrew)
brew install python3
```

### 2. تنزيل المشروع - Download Project
```bash
# استنساخ المشروع (إذا كان على Git)
git clone <repository-url>
cd SportsFieldBookingSystem

# أو قم بفك ضغط الملف إذا كان مضغوطاً
```

### 3. إنشاء البيئة الافتراضية - Create Virtual Environment

#### Windows
```bash
# إنشاء البيئة الافتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
venv\Scripts\activate
```

#### Linux/macOS
```bash
# إنشاء البيئة الافتراضية
python3 -m venv venv

# تفعيل البيئة الافتراضية
source venv/bin/activate
```

### 4. تثبيت الحزم المطلوبة - Install Required Packages
```bash
# تأكد من تفعيل البيئة الافتراضية أولاً
pip install -r requirements.txt

# إذا واجهت مشاكل، جرب:
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## تشغيل المشروع - Running the Project

### 🎯 التشغيل السريع - Quick Start
```bash
# تفعيل البيئة الافتراضية
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# تشغيل التطبيق
python main.py

# الوصول للتطبيق
# http://localhost:8000
```

### 1. تفعيل البيئة الافتراضية - Activate Virtual Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Linux/macOS
```bash
source venv/bin/activate
```

### 2. تشغيل الخادم - Start the Server
```bash
# تشغيل الخادم
python main.py

# أو باستخدام uvicorn مباشرة
uvicorn main:app --host=0.0.0.0 --port=8000 --reload
```

### 3. الوصول للتطبيق - Access the Application
افتح المتصفح واذهب إلى:
Open your browser and go to:
```
http://localhost:8000
```

### معلومات تسجيل الدخول - Login Information
- **المدير - Admin:** `/admin`
- **اسم المستخدم - Username:** `admin`
- **كلمة المرور - Password:** `admin123`

### ⚠️ ملاحظات الأمان - Security Notes
- قم بتغيير كلمة مرور المدير الافتراضية في الإنتاج
- استخدم Environment Variables للبيانات الحساسة
- تأكد من تحديث SECRET_KEY في الإنتاج

## الميزات - Features

### للمستخدمين - For Users
- ✅ حجز الملاعب الرياضية - Book sports fields
- ✅ عرض الملاعب المتاحة - View available fields
- ✅ تأكيد الحجز مع رمز شريطي - Booking confirmation with barcode
- ✅ التحقق من الحجز بالرمز الشريطي - Verify booking with barcode
- ✅ عرض تفاصيل الحجز - View booking details

### للمديرين - For Administrators
- ✅ لوحة تحكم إدارية - Admin dashboard
- ✅ إدارة الحجوزات - Manage bookings
- ✅ إدارة الملاعب - Manage fields
- ✅ إدارة المستخدمين - Manage users
- ✅ نظام تسجيل دخول آمن - Secure login system
- ✅ تسجيل الخروج الآمن - Secure logout

## التحديثات الأخيرة - Recent Updates

### v2.1.0 - Render Deployment Fix (يناير 2025)
- ✅ إصلاح مشكلة التوافق مع Python 3.13
- ✅ تحديث إصدارات الحزم لحل مشاكل SQLAlchemy
- ✅ إضافة دعم PostgreSQL لـ Render
- ✅ تحسين معالجة الأخطاء
- ✅ إضافة ملفات النشر (render.yaml, runtime.txt)
- ✅ تحديث README مع تعليمات النشر
- ✅ إضافة ملف الترخيص MIT
- ✅ تحسين التوثيق والاستكشاف
- ✅ إضافة دعم Heroku
- ✅ تحسينات الأداء

### v2.0.0 - Admin Features (ديسمبر 2024)
- ✅ نظام إدارة متكامل
- ✅ حماية الصفحات الإدارية
- ✅ نظام تسجيل دخول آمن
- ✅ إدارة الحجوزات والمباريات
- ✅ نظام أكواد الدفع
- ✅ تحسينات الأمان

### v1.0.0 - Initial Release (نوفمبر 2024)
- ✅ نظام حجز أساسي
- ✅ واجهة مستخدم بسيطة
- ✅ نظام باركود للحجوزات
- ✅ دعم اللغة العربية
- ✅ تصميم متجاوب

## هيكل المشروع - Project Structure

```
SportsFieldBookingSystem/
├── main.py                 # نقطة البداية الرئيسية - Main entry point
├── requirements.txt        # الحزم المطلوبة - Required packages
├── README.md              # ملف القراءة - This file
├── static/                # الملفات الثابتة - Static files
│   ├── css/              # ملفات التنسيق - CSS files
│   ├── js/               # ملفات JavaScript - JavaScript files
│   └── images/           # الصور - Images
├── templates/             # قوالب HTML - HTML templates
│   ├── admin/            # قوالب لوحة التحكم - Admin templates
│   └── user/             # قوالب المستخدمين - User templates
└── data/                 # بيانات التطبيق - Application data
    └── venues.json       # بيانات الملاعب - Venues data
```

## استكشاف الأخطاء - Troubleshooting

### مشاكل شائعة - Common Issues

#### 1. خطأ "Python not found"
```bash
# تأكد من تثبيت Python
python --version
# أو
python3 --version
```

#### 2. خطأ "pip not found"
```bash
# إعادة تثبيت pip
python -m ensurepip --upgrade
```

#### 3. خطأ "Port already in use"
```bash
# إيقاف العمليات على المنفذ 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

#### 4. خطأ في تثبيت الحزم
```bash
# تحديث pip
pip install --upgrade pip

# إعادة تثبيت الحزم
pip install -r requirements.txt --force-reinstall
```

#### 5. مشاكل البيئة الافتراضية
```bash
# حذف وإعادة إنشاء البيئة الافتراضية
# Windows
rmdir /s venv
python -m venv venv
venv\Scripts\activate

# Linux/macOS
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

#### 6. خطأ SQLAlchemy مع Python 3.13
```bash
# هذا الخطأ يحدث بسبب عدم توافق SQLAlchemy مع Python 3.13
# الحل: استخدام Python 3.11
# Windows
# قم بتحميل Python 3.11.9 من python.org

# Linux/macOS
# استخدم pyenv لتثبيت Python 3.11
pyenv install 3.11.9
pyenv global 3.11.9
```

#### 7. مشاكل النشر على Render
```bash
# تأكد من أن ملف runtime.txt يحتوي على:
python-3.11.9

# تأكد من أن Procfile يحتوي على:
web: uvicorn main:app --host=0.0.0.0 --port=10000

# تأكد من إعداد Environment Variables في Render:
DATABASE_URL=sqlite:///./booking_system.db
SECRET_KEY=your-secret-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ENVIRONMENT=production
HOST=0.0.0.0
PORT=10000
```

#### 8. خطأ "Build failed" في Render
```bash
# تأكد من أن جميع الملفات موجودة:
- requirements.txt
- Procfile
- runtime.txt
- main.py

# تأكد من أن إصدارات الحزم متوافقة
# تأكد من أن Python 3.11.9 مستخدم
```

#### 9. خطأ "Application failed to start" في Render
```bash
# تحقق من سجلات التطبيق في Render
# تأكد من أن Environment Variables صحيحة
# تأكد من أن قاعدة البيانات يمكن إنشاؤها
```

## النشر على Render - Deployment on Render

### 🚀 النشر السريع - Quick Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. انقر على الزر أعلاه
2. اربط مستودع GitHub
3. اختر المشروع `SportsFieldBookingSystem`
4. اترك الإعدادات الافتراضية
5. انقر على "Deploy"

### 1. إعداد المشروع - Project Setup
1. تأكد من وجود الملفات التالية:
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `render.yaml`

### 2. إنشاء حساب على Render - Create Render Account
1. قم بزيارة [render.com](https://render.com)
2. أنشئ حساب جديد
3. اربط حساب GitHub الخاص بك

### 3. نشر المشروع - Deploy Project
1. في لوحة تحكم Render، انقر على "New +"
2. اختر "Web Service"
3. اربط مستودع GitHub الخاص بك
4. اختر المشروع `SportsFieldBookingSystem`
5. اترك الإعدادات الافتراضية أو استخدم `render.yaml`

### 4. إعداد Environment Variables - Environment Variables Setup
في إعدادات الخدمة، أضف المتغيرات التالية:
```
DATABASE_URL=sqlite:///./booking_system.db
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ENVIRONMENT=production
HOST=0.0.0.0
PORT=10000
```

### 5. تشغيل النشر - Run Deployment
1. انقر على "Create Web Service"
2. انتظر حتى يكتمل البناء والنشر
3. احصل على رابط التطبيق

### النشر السريع - Quick Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. انقر على الزر أعلاه
2. اربط مستودع GitHub
3. اختر المشروع `SportsFieldBookingSystem`
4. اترك الإعدادات الافتراضية
5. انقر على "Deploy"

### 📋 قائمة التحقق من النشر - Deployment Checklist
- [ ] تم رفع المشروع إلى GitHub
- [ ] تم إعداد Environment Variables في Render
- [ ] تم التأكد من وجود جميع الملفات المطلوبة
- [ ] تم اختبار التطبيق محلياً
- [ ] تم مراجعة سجلات النشر

## الأوامر المفيدة - Useful Commands

### 🛠️ التطوير - Development
```bash
# تشغيل في وضع التطوير
uvicorn main:app --reload --host=0.0.0.0 --port=8000

# تشغيل مع سجلات مفصلة
uvicorn main:app --reload --log-level debug

# تشغيل مع مراقبة الملفات
uvicorn main:app --reload --reload-dir templates --reload-dir static
```

### إدارة البيئة الافتراضية - Virtual Environment Management
```bash
# إنشاء بيئة افتراضية جديدة
python -m venv venv

# تفعيل البيئة الافتراضية
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# إلغاء تفعيل البيئة الافتراضية
deactivate
```

### إدارة الحزم - Package Management
```bash
# تثبيت الحزم
pip install -r requirements.txt

# تحديث الحزم
pip install --upgrade -r requirements.txt

# عرض الحزم المثبتة
pip list

# حفظ الحزم المثبتة
pip freeze > requirements.txt
```

### تشغيل الخادم - Server Management
```bash
# تشغيل الخادم
python main.py

# تشغيل في وضع التطوير
uvicorn main:app --reload --host=0.0.0.0 --port=8000

# تشغيل على منفذ مختلف
python main.py --port 8080

# تشغيل في الخلفية (Linux/macOS)
nohup python main.py &
```

### التطوير - Development
```bash
# تشغيل في وضع التطوير مع إعادة التحميل التلقائي
uvicorn main:app --reload --host=0.0.0.0 --port=8000

# تشغيل مع سجلات مفصلة
uvicorn main:app --reload --log-level debug
```

### 📊 المراقبة - Monitoring
```bash
# مراقبة استخدام الذاكرة
ps aux | grep python

# مراقبة المنافذ المفتوحة
netstat -tulpn | grep :8000

# مراقبة سجلات التطبيق
tail -f logs/app.log

# مراقبة أداء التطبيق
python -m cProfile -o profile.stats main.py
```

### 💾 النسخ الاحتياطي - Backup
```bash
# نسخ احتياطي لقاعدة البيانات
cp booking_system.db backup_$(date +%Y%m%d_%H%M%S).db

# نسخ احتياطي للمشروع
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz . --exclude=venv --exclude=__pycache__

# نسخ احتياطي تلقائي (cron job)
0 2 * * * /path/to/backup_script.sh
```

### 🔄 التحديث - Updates
```bash
# تحديث المشروع من Git
git pull origin main

# تحديث الحزم
pip install -r requirements.txt --upgrade

# إعادة تشغيل الخادم
pkill -f "python main.py"
python main.py

# تحديث تلقائي (script)
./update.sh
```

## الدعم والمساهمة - Support & Contribution

### الإبلاغ عن الأخطاء - Bug Reports
إذا واجهت أي مشاكل، يرجى:
1. التحقق من قسم "استكشاف الأخطاء" أعلاه
2. إنشاء issue في GitHub
3. تضمين تفاصيل الخطأ والخطوات لتكراره

### المساهمة - Contributing
نرحب بالمساهمات! يرجى:
1. Fork المشروع
2. إنشاء branch جديد للميزة
3. إجراء التغييرات
4. إنشاء Pull Request

### أنواع المساهمات المطلوبة - Types of Contributions Needed
- 🐛 إصلاح الأخطاء - Bug fixes
- ✨ ميزات جديدة - New features
- 📚 تحسين التوثيق - Documentation improvements
- 🎨 تحسينات الواجهة - UI improvements
- ⚡ تحسينات الأداء - Performance improvements
- 🔒 تحسينات الأمان - Security improvements
- 🌍 ترجمة للغات أخرى - Translations
- 📱 تحسينات الهاتف المحمول - Mobile improvements

### الدعم - Support
- 📧 البريد الإلكتروني: [your-email@example.com]
- 🐛 GitHub Issues: [رابط المشروع]
- 📖 التوثيق: هذا الملف README.md
- 💬 Discord: [رابط السيرفر]
- 📱 Telegram: [رابط القناة]
- 🎥 YouTube: [قناة الفيديو]
- 📚 Blog: [المدونة]

### الموارد المفيدة - Useful Resources
- 📚 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 📚 [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- 📚 [Render Documentation](https://render.com/docs)
- 🎥 [Video Tutorials](https://youtube.com/playlist?list=...)
- 📖 [Python Best Practices](https://docs.python-guide.org/)
- 🔧 [Development Tools](https://realpython.com/python-development-setup/)

## الترخيص - License

هذا المشروع مرخص تحت رخصة MIT. راجع ملف `LICENSE` للتفاصيل.

This project is licensed under the MIT License. See the `LICENSE` file for details.

### شروط الاستخدام - Terms of Use
- ✅ يمكن استخدام المشروع لأغراض تجارية
- ✅ يمكن تعديل وتوزيع المشروع
- ✅ يجب الاحتفاظ بإشعار الترخيص
- ❌ لا يتحمل المطورون المسؤولية عن أي أضرار

### الاعتراف - Acknowledgments
- شكراً لجميع المساهمين في هذا المشروع
- شكراً لمجتمع FastAPI و SQLAlchemy
- شكراً لـ Render.com لتوفير منصة النشر المجانية

---

**ملاحظة**: تأكد دائماً من تفعيل البيئة الافتراضية قبل تشغيل المشروع.
**Note**: Always ensure the virtual environment is activated before running the project.

### 🎉 شكراً لك!
إذا وجدت هذا المشروع مفيداً، يرجى:
- ⭐ إعطاء نجمة للمشروع على GitHub
- 🔄 مشاركة المشروع مع الآخرين
- 💬 ترك تعليق أو اقتراح
- 🐛 الإبلاغ عن أي أخطاء

### 📞 تواصل معنا
نحن نرحب بأسئلتك واقتراحاتك! لا تتردد في التواصل معنا عبر أي من القنوات المذكورة أعلاه.

---

**Made with ❤️ for the Libyan community**





---

