import qrcode
import base64
from io import BytesIO
import cv2
import numpy as np
import json
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import os

#from qrcode.console_scripts import error_correction


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
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        return "Изображение не найдено или путь указан неверно"

    blur = cv2.GaussianBlur(img, (5, 5), 0) 
    ret, bw_im = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    data = decode(bw_im, symbols=[ZBarSymbol.QRCODE])[0].data.decode('utf-8')
    os.remove(image_path)

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






#json QR хз нужен file name
def creat_jsonQR_png(json_date, file_name='qr_js_img.png'):
    try:
        js_str = json.dumps(json_date, ensure_ascii=False)
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        qr.add_data(js_str)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_name)
        print(f'✅ {file_name}')
    except Exception as e:
        print(f'❌ {e} {file_name}')


def creat_qr_bs64_json(json_data):
    try:
        json_string = json.dumps(json_data, ensure_ascii=False)

        # Создание QR-кода
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4,
        )
        qr.add_data(json_string)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffered = BytesIO()
        img.save(buffered, format="PNG")

        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        print(f'✅ bs64')
        return img_base64

    except Exception as e:
        print(f"❌ {e} base64")
        return None