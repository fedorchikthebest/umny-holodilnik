import qrcode
import base64
from io import BytesIO
import cv2
import numpy as np


# QRidBase64
def generate_qr_base64(id_value):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(id_value)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_base64


# idPNG

def decode_qr_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return "Изображение не найдено или путь указан неверно"

    detector = cv2.QRCodeDetector()

    data, _, _ = detector.detectAndDecode(image)

    if data:
        return data
    else:
        return "QR-код не содержит корректный id"


# idBase64
def decode_qr_from_base64(base64_string):
    try:
        img_data = base64.b64decode(base64_string)
        np_arr = np.frombuffer(img_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            return "Не удалось декодировать изображение из Base64"

        detector = cv2.QRCodeDetector()

        data, _, _ = detector.detectAndDecode(image)

        if data:
            return data
        else:
            return "QR-код не содержит корректный id"

    except Exception as e:
        return f"Ошибка обработки: {str(e)}"
