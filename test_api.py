import requests
import json

def test_admin_login():
    """اختبار تسجيل دخول المدير"""
    url = "http://localhost:8000/admin/login"
    
    data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(url, data=data, allow_redirects=False)
        print(f"Login Status Code: {response.status_code}")
        
        if response.status_code == 302:  # نجح تسجيل الدخول
            # الحصول على الكوكيز
            cookies = response.cookies
            session_cookie = None
            for cookie in cookies:
                if cookie.name == 'admin_session':
                    session_cookie = cookie.value
                    break
            
            if session_cookie:
                print(f"Session Cookie: {session_cookie}")
                return session_cookie
            else:
                print("No session cookie found")
                return None
        else:
            print(f"Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"Login Exception: {e}")
        return None

def test_generate_codes(session_cookie):
    """اختبار إنشاء الأكواد"""
    url = "http://localhost:8000/api/generate-codes"
    
    # بيانات الاختبار
    data = {
        'count': 2,
        'code_type': 'vip',
        'value': 50.0,
        'expiry_days': 30
    }
    
    # إعداد الكوكيز
    cookies = {'admin_session': session_cookie}
    
    # إرسال الطلب
    try:
        response = requests.post(url, data=data, cookies=cookies)
        print(f"Generate Codes Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success')}")
            print(f"Message: {result.get('message')}")
            if 'codes' in result:
                print("Generated Codes:")
                for code in result['codes']:
                    print(f"  - {code['code']} ({code['type']} - {code['value']} دينار)")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def test_get_payment_codes(session_cookie):
    """اختبار الحصول على قائمة الأكواد"""
    url = "http://localhost:8000/api/payment-codes"
    
    cookies = {'admin_session': session_cookie}
    
    try:
        response = requests.get(url, cookies=cookies)
        print(f"Get Codes Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Total Codes: {len(result.get('codes', []))}")
            for code in result.get('codes', [])[:5]:  # عرض أول 5 أكواد فقط
                print(f"  - {code['code']} ({code['code_type']} - {code['value']} دينار) - Used: {code['is_used']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    print("=== اختبار نظام أكواد الدفع ===\n")
    
    # 1. تسجيل الدخول
    print("1. تسجيل دخول المدير...")
    session_cookie = test_admin_login()
    
    if session_cookie:
        print("\n2. إنشاء أكواد جديدة...")
        test_generate_codes(session_cookie)
        
        print("\n3. الحصول على قائمة الأكواد...")
        test_get_payment_codes(session_cookie)
    else:
        print("فشل في تسجيل الدخول") 