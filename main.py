from fastapi import FastAPI, Request, Form, Depends, HTTPException, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
import uuid
import json
from typing import List, Optional
import os
from passlib.context import CryptContext
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# إنشاء التطبيق
app = FastAPI(title="نظام حجز مباريات كرة القدم")

# Middleware لمنع التخزين المؤقت للصفحات الإدارية
@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response = await call_next(request)
    
    # إضافة headers لمنع التخزين المؤقت للصفحات الإدارية
    if request.url.path.startswith("/admin"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    
    return response

# إعداد قاعدة البيانات
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./booking_system.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# إعداد قاعدة البيانات
if SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# نماذج قاعدة البيانات
class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(DateTime)
    time = Column(String)
    price_normal = Column(Float)
    price_vip = Column(Float)
    total_seats = Column(Integer, default=250)
    vip_seats = Column(Integer, default=100)
    normal_seats = Column(Integer, default=150)
    is_active = Column(Boolean, default=True)

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(String, unique=True, index=True)
    match_id = Column(Integer)
    seat_number = Column(Integer)
    is_vip = Column(Boolean)
    customer_name = Column(String)
    customer_phone = Column(String)
    customer_email = Column(String)
    payment_method = Column(String)
    total_price = Column(Float)
    booking_date = Column(DateTime, default=datetime.utcnow)
    is_confirmed = Column(Boolean, default=False)

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

class PaymentCode(Base):
    __tablename__ = "payment_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    code_type = Column(String)  # 'vip' or 'normal'
    value = Column(Float)
    is_used = Column(Boolean, default=False)
    used_by = Column(String, nullable=True)  # booking_id
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

# إعداد القوالب والملفات الثابتة
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# إعداد التشفير
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

# متغيرات الجلسة
admin_sessions = {}

# دالة للحصول على جلسة قاعدة البيانات
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# إضافة بيانات تجريبية
def add_sample_data(db: Session):
    # التحقق من وجود مباريات
    if db.query(Match).count() == 0:
        sample_matches = [
            Match(
                title="الأهلي طرابلس vs الاتحاد",
                date=datetime.now() + timedelta(days=7),
                time="20:00",
                price_normal=25.0,
                price_vip=75.0,
                total_seats=250,
                vip_seats=100,
                normal_seats=150
            ),
            Match(
                title="الأهلي بنغازي vs النصر",
                date=datetime.now() + timedelta(days=14),
                time="21:30",
                price_normal=30.0,
                price_vip=90.0,
                total_seats=250,
                vip_seats=100,
                normal_seats=150
            ),
            Match(
                title="الزاوية vs الهلال",
                date=datetime.now() + timedelta(days=21),
                time="19:00",
                price_normal=20.0,
                price_vip=60.0,
                total_seats=250,
                vip_seats=100,
                normal_seats=150
            ),
            Match(
                title="الأولمبي vs التحدي",
                date=datetime.now() + timedelta(days=28),
                time="21:00",
                price_normal=35.0,
                price_vip=105.0,
                total_seats=250,
                vip_seats=100,
                normal_seats=150
            ),
            Match(
                title="المروج vs الوحدة",
                date=datetime.now() + timedelta(days=35),
                time="17:30",
                price_normal=22.0,
                price_vip=66.0,
                total_seats=250,
                vip_seats=100,
                normal_seats=150
            )
        ]
        db.add_all(sample_matches)
        db.commit()

# إضافة مدير افتراضي
def add_default_admin(db: Session):
    if db.query(Admin).count() == 0:
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        
        admin = Admin(
            username=admin_username,
            password_hash=pwd_context.hash(admin_password)
        )
        db.add(admin)
        db.commit()

# دوال المصادقة المحسنة
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_admin(username: str, password: str, db: Session):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        return False
    if not verify_password(password, admin.password_hash):
        return False
    return admin

def create_admin_session(admin_id: int):
    session_token = secrets.token_urlsafe(64)  # زيادة طول التوكن
    session_id = secrets.token_urlsafe(32)     # معرف جلسة منفصل
    admin_sessions[session_token] = {
        "admin_id": admin_id,
        "session_id": session_id,
        "created_at": datetime.utcnow(),
        "last_activity": datetime.utcnow(),
        "ip_address": None,  # سيتم تعيينه لاحقاً
        "user_agent": None   # سيتم تعيينه لاحقاً
    }
    return session_token, session_id

def verify_admin_session(session_token: str, request: Request = None):
    if session_token not in admin_sessions:
        return None
    
    session_data = admin_sessions[session_token]
    
    # التحقق من انتهاء صلاحية الجلسة (12 ساعة)
    if datetime.utcnow() - session_data["created_at"] > timedelta(hours=12):
        del admin_sessions[session_token]
        return None
    
    # التحقق من عدم النشاط (30 دقيقة)
    if datetime.utcnow() - session_data["last_activity"] > timedelta(minutes=30):
        del admin_sessions[session_token]
        return None
    
    # تحديث آخر نشاط
    session_data["last_activity"] = datetime.utcnow()
    
    # التحقق من IP إذا كان متاحاً
    if request and session_data["ip_address"]:
        client_ip = request.client.host
        if client_ip != session_data["ip_address"]:
            del admin_sessions[session_token]
            return None
    
    return session_data["admin_id"]

def revoke_admin_session(session_token: str):
    if session_token in admin_sessions:
        del admin_sessions[session_token]
        return True
    return False

def get_active_sessions_count():
    return len(admin_sessions)

# دوال إدارة أكواد الدفع
def generate_payment_code():
    """توليد كود دفع عشوائي"""
    import random
    import string
    # تجنب الأحرف المربكة (0, O, 1, I, L)
    chars = string.ascii_uppercase.replace('O', '').replace('I', '').replace('L', '') + string.digits.replace('0', '').replace('1', '')
    code = ''.join(random.choices(chars, k=12))
    return code

def create_payment_codes(count: int, code_type: str, value: float, expiry_days: int = 30, db: Session = None):
    """إنشاء أكواد دفع جديدة"""
    codes = []
    max_attempts = 1000  # لتجنب الحلقة اللانهائية في حالة تكرار الأكواد
    
    for i in range(count):
        attempts = 0
        while attempts < max_attempts:
            code = generate_payment_code()
            # التحقق من عدم تكرار الكود في القائمة الحالية
            if not any(existing_code.code == code for existing_code in codes):
                # التحقق من عدم وجود الكود في قاعدة البيانات إذا تم تمريرها
                if db:
                    existing_db_code = db.query(PaymentCode).filter(PaymentCode.code == code).first()
                    if existing_db_code:
                        attempts += 1
                        continue
                
                payment_code = PaymentCode(
                    code=code,
                    code_type=code_type,
                    value=value,
                    expires_at=datetime.utcnow() + timedelta(days=expiry_days)
                )
                codes.append(payment_code)
                break
            attempts += 1
        
        if attempts >= max_attempts:
            raise Exception(f"فشل في إنشاء كود فريد بعد {max_attempts} محاولة")
    
    return codes

def validate_payment_code(code: str, code_type: str, db: Session):
    """التحقق من صحة كود الدفع"""
    payment_code = db.query(PaymentCode).filter(
        PaymentCode.code == code,
        PaymentCode.code_type == code_type,
        PaymentCode.is_used == False,
        PaymentCode.is_active == True,
        PaymentCode.expires_at > datetime.utcnow()
    ).first()
    return payment_code

def use_payment_code(code: str, booking_id: str, db: Session):
    """استخدام كود الدفع"""
    payment_code = db.query(PaymentCode).filter(PaymentCode.code == code).first()
    if payment_code:
        payment_code.is_used = True
        payment_code.used_by = booking_id
        payment_code.used_at = datetime.utcnow()
        db.commit()
        return True
    return False

# الصفحة الرئيسية
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    matches = db.query(Match).filter(Match.is_active == True).all()
    return templates.TemplateResponse("index.html", {"request": request, "matches": matches})

# صفحة اختيار المقعد
@app.get("/booking/{match_id}", response_class=HTMLResponse)
async def booking_page(request: Request, match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="المباراة غير موجودة")
    
    # الحصول على المقاعد المحجوزة
    booked_seats = db.query(Booking).filter(Booking.match_id == match_id).all()
    booked_seat_numbers = [booking.seat_number for booking in booked_seats]
    
    return templates.TemplateResponse("booking.html", {
        "request": request, 
        "match": match, 
        "booked_seats": booked_seat_numbers
    })

# API لحجز المقعد
@app.post("/api/book-seat")
async def book_seat(
    match_id: int = Form(...),
    seat_number: int = Form(...),
    is_vip: str = Form(...),  # سيتم تحويله إلى bool
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    customer_email: str = Form(...),
    payment_method: str = Form(...),
    payment_code: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # تحويل is_vip من string إلى bool
        is_vip_bool = is_vip.lower() in ['true', '1', 'yes', 'on']
        
        print(f"Booking request: match_id={match_id}, seat_number={seat_number}, is_vip={is_vip}->{is_vip_bool}, customer={customer_name}")
        
        # التحقق من وجود المباراة
        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise HTTPException(status_code=404, detail="المباراة غير موجودة")
        
        # التحقق من أن المقعد متاح
        existing_booking = db.query(Booking).filter(
            Booking.match_id == match_id,
            Booking.seat_number == seat_number
        ).first()
        
        if existing_booking:
            raise HTTPException(status_code=400, detail="المقعد محجوز بالفعل")
        
        # التحقق من كود الدفع إذا تم استخدامه
        if payment_method == "payment_code" and payment_code:
            code_type = "vip" if is_vip_bool else "normal"
            payment_code_obj = validate_payment_code(payment_code, code_type, db)
            if not payment_code_obj:
                raise HTTPException(status_code=400, detail="كود الدفع غير صحيح أو منتهي الصلاحية")
            
            # استخدام الكود
            if not use_payment_code(payment_code, str(uuid.uuid4()), db):
                raise HTTPException(status_code=400, detail="فشل في استخدام كود الدفع")
            
            # السعر من الكود
            price = payment_code_obj.value
        else:
            # حساب السعر العادي
            price = match.price_vip if is_vip_bool else match.price_normal
        
        # إنشاء الحجز
        booking = Booking(
            booking_id=str(uuid.uuid4()),
            match_id=match_id,
            seat_number=seat_number,
            is_vip=is_vip_bool,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            payment_method=payment_method,
            total_price=price,
            is_confirmed=True
        )
        
        db.add(booking)
        db.commit()
        db.refresh(booking)
        
        print(f"Booking created successfully: {booking.booking_id}")
        return {"success": True, "booking_id": booking.booking_id, "booking": booking}
        
    except Exception as e:
        print(f"Error in booking: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في الحجز: {str(e)}")

# صفحة تأكيد الحجز
@app.get("/confirmation/{booking_id}", response_class=HTMLResponse)
async def confirmation_page(request: Request, booking_id: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="الحجز غير موجود")
    
    match = db.query(Match).filter(Match.id == booking.match_id).first()
    
    return templates.TemplateResponse("confirmation.html", {
        "request": request,
        "booking": booking,
        "match": match
    })

# صفحة تسجيل دخول المدير
@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
async def admin_login(
    response: Response,
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # التحقق من محاولات تسجيل الدخول الفاشلة
    client_ip = request.client.host
    
    admin = authenticate_admin(username, password, db)
    if not admin:
        # تسجيل محاولة فاشلة
        print(f"Failed login attempt for username: {username} from IP: {client_ip}")
        raise HTTPException(status_code=401, detail="بيانات الدخول غير صحيحة")
    
    # إنشاء جلسة آمنة
    session_token, session_id = create_admin_session(admin.id)
    
    # تخزين معلومات الجلسة
    admin_sessions[session_token]["ip_address"] = client_ip
    admin_sessions[session_token]["user_agent"] = request.headers.get("user-agent", "")
    
    # تسجيل تسجيل الدخول الناجح
    print(f"Successful login for admin: {admin.username} from IP: {client_ip}")
    
    response = RedirectResponse(url="/admin", status_code=302)
    response.set_cookie(
        key="admin_session", 
        value=session_token, 
        httponly=True, 
        secure=False,  # True في الإنتاج مع HTTPS
        samesite="strict",
        max_age=43200  # 12 ساعة
    )
    response.set_cookie(
        key="session_id", 
        value=session_id, 
        httponly=True, 
        secure=False,  # True في الإنتاج مع HTTPS
        samesite="strict",
        max_age=43200
    )
    return response

@app.get("/admin/logout")
async def admin_logout(request: Request, response: Response):
    session_token = request.cookies.get("admin_session")
    if session_token:
        # إلغاء الجلسة
        revoke_admin_session(session_token)
        print(f"Admin logged out from IP: {request.client.host}")
    
    # توجيه لصفحة تسجيل الدخول مع رسالة تأكيد
    response = RedirectResponse(url="/admin/login?message=logged_out", status_code=302)
    response.delete_cookie(key="admin_session")
    response.delete_cookie(key="session_id")
    
    return response

@app.get("/admin/logout-confirm")
async def admin_logout_confirm(request: Request):
    session_token = request.cookies.get("admin_session")
    if not session_token or not verify_admin_session(session_token, request):
        return RedirectResponse(url="/admin/login", status_code=302)
    
    return templates.TemplateResponse("admin_logout_confirm.html", {"request": request})

# لوحة تحكم المدير
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, db: Session = Depends(get_db)):
    # التحقق من الجلسة المحسن
    session_token = request.cookies.get("admin_session")
    if not session_token or not verify_admin_session(session_token, request):
        return RedirectResponse(url="/admin/login?message=session_expired", status_code=302)
    
    matches = db.query(Match).all()
    bookings = db.query(Booking).all()
    active_sessions = get_active_sessions_count()
    
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "matches": matches,
        "bookings": bookings,
        "active_sessions": active_sessions
    })

# API لإضافة مباراة جديدة
@app.post("/api/add-match")
async def add_match(
    title: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    price_normal: float = Form(...),
    price_vip: float = Form(...),
    db: Session = Depends(get_db)
):
    match = Match(
        title=title,
        date=datetime.strptime(date, "%Y-%m-%d"),
        time=time,
        price_normal=price_normal,
        price_vip=price_vip,
        total_seats=250,
        vip_seats=100,
        normal_seats=150
    )
    
    db.add(match)
    db.commit()
    db.refresh(match)
    
    return {"success": True, "match": match}

# API للحصول على المقاعد المحجوزة
@app.get("/api/booked-seats/{match_id}")
async def get_booked_seats(match_id: int, db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.match_id == match_id).all()
    return {"booked_seats": [booking.seat_number for booking in bookings]}

# APIs إدارة المباريات
@app.delete("/api/delete-match/{match_id}")
async def delete_match(
    match_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    # التحقق من الجلسة المحسن
    session_token = request.cookies.get("admin_session")
    if not session_token or not verify_admin_session(session_token, request):
        raise HTTPException(status_code=401, detail="جلسة منتهية الصلاحية")
    
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="المباراة غير موجودة")
    
    # حذف جميع الحجوزات المرتبطة
    db.query(Booking).filter(Booking.match_id == match_id).delete()
    db.delete(match)
    db.commit()
    
    return {"success": True, "message": "تم حذف المباراة بنجاح"}

@app.put("/api/update-match/{match_id}")
async def update_match(
    match_id: int,
    title: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    price_normal: float = Form(...),
    price_vip: float = Form(...),
    is_active: bool = Form(False),
    request: Request = None,
    db: Session = Depends(get_db)
):
    # التحقق من الجلسة المحسن
    session_token = request.cookies.get("admin_session") if request else None
    if not session_token or not verify_admin_session(session_token, request):
        raise HTTPException(status_code=401, detail="جلسة منتهية الصلاحية")
    
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="المباراة غير موجودة")
    
    match.title = title
    match.date = datetime.strptime(date, "%Y-%m-%d")
    match.time = time
    match.price_normal = price_normal
    match.price_vip = price_vip
    match.is_active = is_active
    
    db.commit()
    db.refresh(match)
    
    return {"success": True, "match": match}

# APIs إدارة الحجوزات
@app.delete("/api/delete-booking/{booking_id}")
async def delete_booking(
    booking_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    # التحقق من الجلسة المحسن
    session_token = request.cookies.get("admin_session")
    if not session_token or not verify_admin_session(session_token, request):
        raise HTTPException(status_code=401, detail="جلسة منتهية الصلاحية")
    
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="الحجز غير موجود")
    
    db.delete(booking)
    db.commit()
    
    return {"success": True, "message": "تم حذف الحجز بنجاح"}

@app.put("/api/update-booking/{booking_id}")
async def update_booking(
    booking_id: str,
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    customer_email: str = Form(...),
    payment_method: str = Form(...),
    is_confirmed: bool = Form(True),
    request: Request = None,
    db: Session = Depends(get_db)
):
    # التحقق من الجلسة المحسن
    session_token = request.cookies.get("admin_session") if request else None
    if not session_token or not verify_admin_session(session_token, request):
        raise HTTPException(status_code=401, detail="جلسة منتهية الصلاحية")
    
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="الحجز غير موجود")
    
    booking.customer_name = customer_name
    booking.customer_phone = customer_phone
    booking.customer_email = customer_email
    booking.payment_method = payment_method
    booking.is_confirmed = is_confirmed
    
    db.commit()
    db.refresh(booking)
    
    return {"success": True, "booking": booking}

# APIs إدارة أكواد الدفع
@app.post("/api/generate-codes")
async def generate_payment_codes_api(
    count: int = Form(...),
    code_type: str = Form(...),  # 'vip' or 'normal'
    value: float = Form(...),
    expiry_days: int = Form(30),
    request: Request = None,
    db: Session = Depends(get_db)
):
    try:
        # التحقق من الجلسة المحسن
        session_token = request.cookies.get("admin_session") if request else None
        if not session_token or not verify_admin_session(session_token, request):
            raise HTTPException(status_code=401, detail="جلسة منتهية الصلاحية")
        
        # التحقق من صحة البيانات
        if count < 1 or count > 100:
            raise HTTPException(status_code=400, detail="عدد الأكواد يجب أن يكون بين 1 و 100")
        
        if code_type not in ['vip', 'normal']:
            raise HTTPException(status_code=400, detail="نوع الكود غير صحيح")
        
        if value <= 0:
            raise HTTPException(status_code=400, detail="قيمة الكود يجب أن تكون أكبر من صفر")
        
        if expiry_days < 1 or expiry_days > 365:
            raise HTTPException(status_code=400, detail="مدة الصلاحية يجب أن تكون بين 1 و 365 يوم")
        
        # إنشاء الأكواد
        codes = create_payment_codes(count, code_type, value, expiry_days, db)
        db.add_all(codes)
        db.commit()
        
        return {
            "success": True, 
            "message": f"تم إنشاء {count} كود بنجاح",
            "codes": [{"code": code.code, "type": code.code_type, "value": code.value} for code in codes]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating codes: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ داخلي في إنشاء الأكواد")

@app.get("/api/payment-codes")
async def get_payment_codes(
    request: Request,
    db: Session = Depends(get_db)
):
    # التحقق من الجلسة المحسن
    session_token = request.cookies.get("admin_session")
    if not session_token or not verify_admin_session(session_token, request):
        raise HTTPException(status_code=401, detail="جلسة منتهية الصلاحية")
    
    codes = db.query(PaymentCode).order_by(PaymentCode.created_at.desc()).all()
    return {"codes": codes}

@app.delete("/api/delete-code/{code_id}")
async def delete_payment_code(
    code_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    # التحقق من الجلسة المحسن
    session_token = request.cookies.get("admin_session")
    if not session_token or not verify_admin_session(session_token, request):
        raise HTTPException(status_code=401, detail="جلسة منتهية الصلاحية")
    
    code = db.query(PaymentCode).filter(PaymentCode.id == code_id).first()
    if not code:
        raise HTTPException(status_code=404, detail="الكود غير موجود")
    
    db.delete(code)
    db.commit()
    
    return {"success": True, "message": "تم حذف الكود بنجاح"}

@app.post("/api/validate-code")
async def validate_payment_code_api(
    code: str = Form(...),
    code_type: str = Form(...),
    db: Session = Depends(get_db)
):
    payment_code = validate_payment_code(code, code_type, db)
    if payment_code:
        return {
            "valid": True,
            "value": payment_code.value,
            "expires_at": payment_code.expires_at
        }
    else:
        return {"valid": False, "message": "الكود غير صحيح أو منتهي الصلاحية"}

# صفحة تحقق من الحجز بالباركود
@app.get("/barcode-check", response_class=HTMLResponse)
async def barcode_check_page(request: Request):
    return templates.TemplateResponse("barcode_check.html", {"request": request})

# API تحقق من الحجز بالباركود
@app.post("/api/barcode-check")
async def api_barcode_check(barcode: str = Form(...), db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == barcode).first()
    if not booking:
        return {"success": False, "message": "الحجز غير موجود أو الباركود غير صحيح"}
    match = db.query(Match).filter(Match.id == booking.match_id).first()
    return {
        "success": True,
        "booking": {
            "booking_id": booking.booking_id,
            "customer_name": booking.customer_name,
            "seat_number": booking.seat_number,
            "is_vip": booking.is_vip,
            "total_price": booking.total_price,
            "booking_date": booking.booking_date.strftime('%Y-%m-%d %H:%M'),
            "match_title": match.title if match else "",
            "match_date": match.date.strftime('%Y-%m-%d') if match else "",
            "match_time": match.time if match else ""
        }
    }

# تشغيل التطبيق
if __name__ == "__main__":
    import uvicorn
    
    # إضافة البيانات التجريبية
    db = SessionLocal()
    add_sample_data(db)
    add_default_admin(db)
    db.close()
    
    # استخدام Environment Variables للـ host والـ port
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(app, host=host, port=port) 