from flask import Flask, request, render_template, send_from_directory, \
    jsonify
from werkzeug.utils import secure_filename
import os
from file_hash import hash_doc


app = Flask(__name__, static_url_path="/static", static_folder="static")
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("upload_file.html")


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = os.path.join('static/', secure_filename(f.filename))
        f.save(filename)
        txn_hash = hash_doc(filename, action='store')
        res = jsonify{'hash':txn_hash}
        res.status_code = 200
        return res

@app.route("/verify", methods=["POST"])
def verify():
    if request.method == 'POST':
        f = request.files['file']
        filename = os.path.join('static/', secure_filename(f.filename))
        f.save(filename)
        args = request.get_json()
        verification = hash_doc(filename, action='verify', txn_id=args['txn_id'])
        res = jsonify{'verification': verification}
        res.status_code = 200
        return res

if __name__ == '__main__':
    app.run()