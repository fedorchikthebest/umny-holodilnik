import qrcode
from base64 import b64encode
from io import BytesIO
from PIL import Image


def generate_qr_code(id: int) -> str:
    data = str(id)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return b64encode(buffer.getvalue()).decode("utf-8")


def bytes_to_image(byte_sequence, output_file):
    print(byte_sequence)
    try:

        image_stream = BytesIO(byte_sequence)

        image = Image.open(image_stream)

        image.save(output_file)
        print(f"{output_file}")
    except Exception as e:
        print(f"{e}")

print(generate_qr_code(1488))
