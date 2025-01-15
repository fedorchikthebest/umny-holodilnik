import io
import qrcode
import cv2
import numpy as np
from PIL import Image


def create_qr_code(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    byte_stream = io.BytesIO()
    img.save(byte_stream, format="PNG")
    byte_stream.seek(0)
    return byte_stream.getvalue()


def decode_qr_code(byte_sequence):
    try:
        byte_stream = io.BytesIO(byte_sequence)
        img = Image.open(byte_stream).convert("RGB")
        img_np = np.array(img)
        qr_detector = cv2.QRCodeDetector()
        data, bbox, _ = qr_detector.detectAndDecode(img_np)
        if data:
            return data
        else:
            print("QR code not detected or empty.")
            return None
    except Exception as e:
        print(f"Error decoding QR code: {e}")
        return None



