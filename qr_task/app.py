from flask import Flask, render_template, request, redirect
import qrcode
from io import BytesIO
import base64

import qrcode.constants

app = Flask(__name__)

current_url = "http://127.0.0.1"

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data=data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

qr_code = generate_qr_code("http://127.0.0.1/redirect")

@app.route("/", methods=["GET", "POST"])
def index():
    global current_url
    if request.method == "POST":
        new_url = request.form.get("url")
        current_url = new_url

    return render_template('index.html', current_url=current_url, qr_code=qr_code)

@app.route("/redirect")
def redirect_to_current():
    return redirect(current_url)

if __name__ == "__main__":
    app.run(debug=True)