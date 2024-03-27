from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        texto = request.form['texto']
        if texto:
            qr_img, filename = generar_codigo_qr(texto)
            return render_template('index.html', qr_img=qr_img, filename=filename)
    return render_template('index.html')

def generar_codigo_qr(texto):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return base64_img, 'codigo_qr.png'

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)




