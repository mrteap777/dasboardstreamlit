from PIL import Image
from flask import Flask, request, jsonify
from model import predict_class


app = Flask(__name__)

@app.route("/img_upload_check", methods=["POST"])
def process_image():
    file = request.files['image']
    img = Image.open(file.stream)

    return jsonify({'msg': 'success', 'size': [img.width, img.height]})

@app.route("/get_breed_by_img",methods=["POST"])
def predict_by_image():
    file = request.files['image']
    file.save(file.filename)
    return predict_class(file.filename)


if __name__ == "__main__":
    app.run(debug=True, port=3000,host='127.0.0.1')