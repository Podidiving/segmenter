import base64
import io
import pathlib
import random
import warnings

import flask
import requests
import torch
from PIL import Image
from torch.nn import functional as F

warnings.filterwarnings("ignore")


def fetch_image_list():
    root_dir = "./data"
    paths = pathlib.Path(root_dir).rglob("*.jpg")
    paths = [x.name for x in paths]
    return paths


# ==================== [CONFIG] ====================

app = flask.Flask(__name__)
image_list = fetch_image_list()


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


@app.route("/api/random_image")
def image_list_handler():
    global image_list
    if not len(image_list):
        image_list = fetch_image_list()
    if not len(image_list):
        return "No images", 501
    random_filename = random.choice(image_list)
    return flask.send_from_directory("data", random_filename)


@app.route("/api/run_model", methods=["POST"])
def run_model():
    def _make_serving_request(preprocessed_image_bytes):
        url = "http://serve:8080/predictions/deeplabv3_resnet_101"
        req = requests.post(url, data=preprocessed_image_bytes)
        if req.status_code == 200:
            output = req.json()
            t = torch.FloatTensor(output)
            return t
        return req.status_code

    original_image = flask.request.json.get("image")

    if not isinstance(original_image, str):
        return "bad request", 400

    original_image = original_image.split("base64,")[1]
    original_image = base64.b64decode(original_image)

    original_image = Image.open(io.BytesIO(original_image))
    original_image = original_image.convert("RGB")

    raw_image_bytes = io.BytesIO()
    original_image.save(raw_image_bytes, format="PNG")
    raw_image_bytes.seek(0)

    try:
        result = _make_serving_request(raw_image_bytes.read())
        if isinstance(result, int):
            return "Serving error", result
    except Exception:
        return "Serving error", 501
    mask = (
        F.interpolate(
            result.permute(2, 0, 1).unsqueeze(0), original_image.size[::-1]
        )
        .squeeze(0)
        .argmax(0)
    )
    mask = Image.fromarray(
        ((1 - mask.squeeze(0).byte().numpy()) * 127) + 127
    ).convert("L")

    original_image.putalpha(mask)
    buffer = io.BytesIO()
    original_image.save(buffer, format="PNG")
    original_image = base64.b64encode(buffer.getvalue())
    original_image = "data:image/png;base64," + original_image.decode()
    return original_image


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337, debug=True)
