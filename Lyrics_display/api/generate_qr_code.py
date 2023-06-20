import qrcode

#Yeah, I know - I need to put relative paths evrywhere 
def generate_qr(token):
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(token)
    qr.make(fit=True)
    qr_code = qr.make_image(fill="black", back_color="white")

    qr_code.save(f"/home/michal/Documents/Python/GetAccessToLyrics/Lyrics_display/files/qr_{token}.jpg")


