# Quishing & Session Hijacking Demo

## Disclaimer

This project is for educational purposes only. It demonstrates phishing risks and defensive techniques. Do not use it for malicious activities.

---

## Overview

This project showcases a **Quishing (QR Code Phishing) attack** combined with **Session Hijacking**, along with a protection system called **Secure Scan**.

**Quishing** involves malicious QR codes that redirect users to fake websites to steal:

* UPI PINs
* Login credentials
* Session tokens

---

## Features

### Attack Simulation

* Paytm-like UI clone
* Malicious QR code generation
* Fake payment flow
* Credential & session capture
* Attacker dashboard

### Secure Scan (Defense)

* QR threat detection
* URL & domain verification
* Risk scoring (threshold: 50)
* Real-time alerts & blocking

---

## Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript
* **Tools:** qrcode, Pillow, jsQR, ngrok

---

## Working

**Attack Flow:**
QR → Fake Page → User Input → Data Capture → Session Hijack

**Protection Flow:**
Scan → Analyze URL & Domain → Risk Score → Alert/Block

---

## Setup

### Prerequisites

* Python 3.7+
* pip
* ngrok

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/paytm-quishing-demo.git
cd paytm-quishing-demo
pip install -r requirements.txt
```

### Run

```bash
ngrok http 5000
python app.py
python qr_generator.py
```

Open the ngrok URL on your phone and scan the generated QR code.

---

## Demo

`/demo/demo_video.mp4`

---

## Note

Built to demonstrate real-world phishing risks and promote secure QR scanning practices.
