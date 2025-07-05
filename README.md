# نظام حجز الملاعب الرياضية - Sports Field Booking System

## نظرة عامة - Overview

نظام حجز الملاعب الرياضية هو تطبيق ويب مبني باستخدام FastAPI للخلفية و HTML/CSS/JavaScript للواجهة الأمامية. النظام مصمم خصيصاً لليبيا ويشمل مدينتي طرابلس والزاوية.

The Sports Field Booking System is a web application built with FastAPI backend and HTML/CSS/JavaScript frontend. The system is specifically designed for Libya and includes Tripoli and Al-Zawiya cities.

## المتطلبات - Requirements

### متطلبات النظام - System Requirements
- Python 3.8 أو أحدث - Python 3.8 or higher
- متصفح ويب حديث - Modern web browser
- اتصال بالإنترنت (لتنزيل الحزم) - Internet connection (for package installation)

### الحزم المطلوبة - Required Packages
جميع الحزم المطلوبة مدرجة في ملف `requirements.txt`

All required packages are listed in the `requirements.txt` file

## التثبيت والإعداد - Installation & Setup

### 1. تثبيت Python - Install Python

#### Windows
1. قم بزيارة [python.org](https://www.python.org/downloads/)
2. حمل أحدث إصدار من Python 3.8+
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
```

## تشغيل المشروع - Running the Project

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
```

### 3. الوصول للتطبيق - Access the Application
افتح المتصفح واذهب إلى:
Open your browser and go to:
```
http://localhost:8000
```

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

## الأوامر المفيدة - Useful Commands

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
python main.py --reload

# تشغيل على منفذ مختلف
python main.py --port 8080
```

## الدعم - Support

إذا واجهت أي مشاكل أو لديك أسئلة، يرجى:
If you encounter any issues or have questions, please:

1. تحقق من قسم استكشاف الأخطاء أعلاه
   Check the troubleshooting section above

2. تأكد من اتباع جميع خطوات التثبيت
   Ensure you followed all installation steps

3. تحقق من إصدار Python والحزم
   Check Python and package versions

## الترخيص - License

هذا المشروع مفتوح المصدر ومتاح للاستخدام العام.
This project is open source and available for public use.

---

**ملاحظة**: تأكد دائماً من تفعيل البيئة الافتراضية قبل تشغيل المشروع.
**Note**: Always ensure the virtual environment is activated before running the project.





---

