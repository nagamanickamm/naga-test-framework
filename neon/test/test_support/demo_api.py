import base64
import os
from flask import Flask, request, send_file

app = Flask(__name__)

os.environ["Current_Working_Dir"] = os.getcwd()

@app.route("/server")
def index():
    return "Hellow, this Server works"

@app.route("/image/<path:filename>")
def image(filename):
    uploads = os.environ["Current_Working_Dir"]+'/neon/test/functional_tests/demo/test_suite/resources/images/'
    return send_file(uploads+filename)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      uploaded_file = request.files['file']
      path = request.form.get('path')
      if uploaded_file.filename != '':
            uploaded_file.save(path+uploaded_file.filename)
      return 'file uploaded successfully'