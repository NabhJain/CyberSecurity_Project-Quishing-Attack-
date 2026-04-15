**This project is for Educational Demo Only**

PROJECT OVERVIEW

This project demonstrates a complete Quishing (QR Code Phishing) attack combined with Session Hijacking, along with a defensive mechanism called "Secure Scan".

What is Quishing?
Quishing = QR Code + Phishing

Attackers generate malicious QR codes that appear legitimate. When scanned, they redirect users to fake websites designed to steal sensitive information such as:

UPI PINs
Session tokens
Login credentials
WHAT THIS PROJECT DEMONSTRATES

ATTACK SIMULATION:

Realistic Paytm UI clone
Malicious QR code generation with branding
Fake payment flow (Amount → PIN → Success)
Credential capture system
Session token theft simulation
Attacker dashboard

PROTECTION MECHANISM (SECURE SCAN):

Secure QR scanner with threat detection
URL pattern analysis
Domain verification (paytm.com only)
Risk scoring system (Threshold: 50 points)
Real-time phishing alerts
Reporting mechanism
UI FEATURES
Balance hide/show toggle
Transaction history
Mobile recharge and bill payments
Bank transfer simulation
Bottom navigation:
Pay | Cashback | Shopping | Credit Card | Loan
TECH STACK

Backend : Python 3.7+, Flask
Frontend : HTML5, CSS3, JavaScript (ES6)
QR Generation : qrcode, Pillow (PIL)
QR Scanning : jsQR Library
HTTPS Tunnel : ngrok
Camera Access : getUserMedia API
Session Handling : Flask Sessions

HOW IT WORKS

ATTACK FLOW:

Attacker generates a malicious QR code
Victim scans the QR code
Redirects to fake Paytm page
Victim enters payment details
Credentials and session token are captured
Attacker reuses session (Session Hijacking)

PROTECTION FLOW:

User scans QR using Secure Scan
System analyzes:
URL pattern
Domain authenticity
Risk score
If risk exceeds threshold:
Alert is shown
Access is blocked

DEMO
Location: /demo/demo_video.mp4

Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip package manager
- ngrok account (free) - https://ngrok.com)
- iPhone or Android phone (for testing)
- Same WiFi network for laptop and phone

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/paytm-quishing-demo.git
cd paytm-quishing-demo

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Start ngrok (New Terminal)
ngrok http 5000
Copy the HTTPS URL (e.g., https://abc123.ngrok.io)

Step 4: Start Flask Server (New Terminal)
python app.py

Step 5: Generate Malicious QR Code (New Terminal)
python qr_generator.py

Step 6: On iPhone
Open Chrome browser
Go to your ngrok HTTPS URL
Tap Share → Add to Home Screen → Name "Paytm"
Open from home screen
Tap "Scan QR Code" → "Start Camera"
Scan the QR code on laptop
Enter amount () and UPI PIN ()
Check terminal - PIN captured!

This project is for Educational Demo Only
