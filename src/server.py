from flask import Flask, request, send_file

import generator

import os

app = Flask(__name__)


@app.route("/")
def root():
    # return json response
    return {
        "status": True,
        "code": 200,
        "message": "Welcome to the API!"
    }

# post request to /api/v1/generate


@app.route("/api/v1/generate", methods=["POST"])
def generate():
    # get the request body
    body = request.json

    folders = [] if "folders" not in body else body["folders"]
    output_size = (2048, 2048) if "output_size" not in body else body["output_size"]
    image_size =  (32, 32) if "image_size" not in body else body["image_size"]
    countable = (20, 30) if "countable" not in body else body["countable"]
    to_find = [] if "find" not in body else body["find"]

    if len(folders) == 0:
        return {
            "status": False,
            "code": 400,
            "message": "Folders must be provided!"
        }

    if len(output_size) != 2:
        return {
            "status": False,
            "code": 400,
            "message": "Output size must be provided!"
        }

    if len(image_size) != 2:
        return {
            "status": False,
            "code": 400,
            "message": "Image size must be provided!"
        }

    if len(countable) != 2:
        return {
            "status": False,
            "code": 400,
            "message": "Countable must be provided!"
        }

    if len(to_find) == 0:
        return {
            "status": False,
            "code": 400,
            "message": "Find must be provided!"
        }

    _to_find = {}

    for item in to_find:
        _to_find[item] = (0, 0)

    try:
        # generate the image
        image, to_find = generator.generate(
            folders,
            output_size,
            image_size,
            countable,
            _to_find
        )

        # return json response
        return {
            "status": True,
            "code": 200,
            "message": "Image generated!",
            "data": {
                "image": image,
                "find": to_find
            }
        }
    except Exception as e:
        print(e)
        # return json response
        return {
            "status": False,
            "code": 500,
            "message": "Internal Server Error"
        }

# get output file
@app.route("/files/output/<filename>", methods=["GET"])
def get(filename):
    output_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "..", "output", filename)
    
    if not os.path.exists(output_file):
        return {
            "status": False,
            "code": 404,
            "message": "File not found!"
        }
    else:
        return send_file(output_file, mimetype="image/jpg")