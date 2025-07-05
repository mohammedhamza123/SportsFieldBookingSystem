import requests
import json

def test_booking():
    url = "http://localhost:8000/api/book-seat"
    
    # بيانات الحجز
    data = {
        'match_id': 2,
        'seat_number': 50,
        'is_vip': 'true',
        'customer_name': 'أحمد محمد',
        'customer_phone': '+966501234567',
        'customer_email': 'ahmed@example.com',
        'payment_method': 'cash'
    }
    
    print("Testing booking with data:")
    for key, value in data.items():
        print(f"  {key}: {value}")
    
    try:
        response = requests.post(url, data=data)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Booking successful!")
            print(f"Booking ID: {result.get('booking_id')}")
            print(f"Success: {result.get('success')}")
            
            # اختبار صفحة التأكيد
            confirmation_url = f"http://localhost:8000/confirmation/{result.get('booking_id')}"
            print(f"\nTesting confirmation page: {confirmation_url}")
            
            conf_response = requests.get(confirmation_url)
            print(f"Confirmation Status: {conf_response.status_code}")
            
        else:
            print(f"\n❌ Booking failed!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")

if __name__ == "__main__":
    test_booking() 