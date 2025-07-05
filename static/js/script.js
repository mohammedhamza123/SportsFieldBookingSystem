// Basic JavaScript for Sports Field Booking System

// Seat selection functionality
function selectSeat(seatElement, seatNumber, isVip) {
    // Remove previous selection
    document.querySelectorAll('.seat.selected').forEach(seat => {
        seat.classList.remove('selected');
    });
    
    // Select new seat
    seatElement.classList.add('selected');
    
    // Update form fields
    document.getElementById('seat_number').value = seatNumber;
    document.getElementById('is_vip').value = isVip ? 'true' : 'false';
    
    // Update price display
    updatePrice(isVip);
}

// Update price based on seat type
function updatePrice(isVip) {
    const priceElement = document.getElementById('price-display');
    if (priceElement) {
        const normalPrice = parseFloat(document.getElementById('normal_price').value) || 0;
        const vipPrice = parseFloat(document.getElementById('vip_price').value) || 0;
        const price = isVip ? vipPrice : normalPrice;
        priceElement.textContent = `السعر: ${price} دينار ليبي`;
    }
}

// Form validation
function validateForm() {
    const requiredFields = ['customer_name', 'customer_phone', 'customer_email'];
    let isValid = true;
    
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field && !field.value.trim()) {
            field.style.borderColor = 'red';
            isValid = false;
        } else if (field) {
            field.style.borderColor = '';
        }
    });
    
    return isValid;
}

// Show/hide payment code field
function togglePaymentCode() {
    const paymentMethod = document.getElementById('payment_method').value;
    const codeField = document.getElementById('payment_code_field');
    
    if (paymentMethod === 'code') {
        codeField.style.display = 'block';
    } else {
        codeField.style.display = 'none';
    }
}

// Print barcode
function printBarcode() {
    window.print();
}

// Admin functions
function deleteMatch(matchId) {
    if (confirm('هل أنت متأكد من حذف هذه المباراة؟')) {
        fetch(`/api/delete-match/${matchId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('حدث خطأ في حذف المباراة');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('حدث خطأ في حذف المباراة');
        });
    }
}

function editMatch(matchId) {
    // Get match data from table row
    const row = document.querySelector(`[data-match-id="${matchId}"]`);
    if (row) {
        const title = row.getAttribute('data-title');
        const date = row.getAttribute('data-date');
        const time = row.getAttribute('data-time');
        const priceNormal = row.getAttribute('data-price-normal');
        const priceVip = row.getAttribute('data-price-vip');
        
        // Fill modal with data
        document.getElementById('edit_title').value = title;
        document.getElementById('edit_date').value = date;
        document.getElementById('edit_time').value = time;
        document.getElementById('edit_price_normal').value = priceNormal;
        document.getElementById('edit_price_vip').value = priceVip;
        document.getElementById('edit_match_id').value = matchId;
        
        // Show modal
        document.getElementById('editMatchModal').style.display = 'block';
    }
}

function updateMatch() {
    const matchId = document.getElementById('edit_match_id').value;
    const formData = new FormData();
    
    formData.append('title', document.getElementById('edit_title').value);
    formData.append('date', document.getElementById('edit_date').value);
    formData.append('time', document.getElementById('edit_time').value);
    formData.append('price_normal', document.getElementById('edit_price_normal').value);
    formData.append('price_vip', document.getElementById('edit_price_vip').value);
    
    fetch(`/api/update-match/${matchId}`, {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('حدث خطأ في تحديث المباراة');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('حدث خطأ في تحديث المباراة');
    });
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Initialize payment method toggle
    const paymentMethodSelect = document.getElementById('payment_method');
    if (paymentMethodSelect) {
        paymentMethodSelect.addEventListener('change', togglePaymentCode);
        togglePaymentCode(); // Initial call
    }
    
    // Initialize form validation
    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                alert('يرجى ملء جميع الحقول المطلوبة');
            }
        });
    }
    
    // Close modals when clicking outside
    window.onclick = function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
    
    // Close modals with X button
    const closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(button => {
        button.onclick = function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
            }
        }
    });
}); 