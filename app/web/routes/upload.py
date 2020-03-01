from flask import request, jsonify, Blueprint
from flask_login import login_required
from ..config import UPLOAD_URL_PREFIX, UPLOAD_FOLDER_SOURCE, UPLOAD_FOLDER_IMAGE_MINIMIZATION
from PIL import Image
from datetime import datetime
from io import BytesIO
import os

bp = Blueprint('upload', __name__, url_prefix=UPLOAD_URL_PREFIX)

basedir = os.path.abspath(os.path.dirname(__file__))

IMG_WIDTH = 300
IMG_TYPES = ['image/jpeg', 'image/png', 'image/jpg']


@bp.route('/message/file', methods=['POST'])
@login_required
def upload_message_file():
    date = datetime.now().strftime("%Y-%m-%d")

    upload_source_dir = os.path.join(basedir, '..', UPLOAD_FOLDER_SOURCE, date)
    upload_min_dir = os.path.join(basedir, '..', UPLOAD_FOLDER_IMAGE_MINIMIZATION, date)

    if not os.path.exists(upload_source_dir.strip()):
        os.makedirs(upload_source_dir)

    if not os.path.exists(upload_min_dir.strip()):
        os.makedirs(upload_min_dir)

    files = request.files.getlist("file")
    file_info = []
    for file in files:
        file.save(os.path.join(upload_source_dir, file.filename))
        file_info.append({'name': file.filename, 'url': os.path.join(date, file.filename), 'type': file.content_type})

        if file.content_type in IMG_TYPES:
            file.seek(0)
            image_bytes = BytesIO(file.read())
            img = Image.open(image_bytes)
            w_percent = IMG_WIDTH / float(img.size[0])
            h_size = int((float(img.size[1])) * float(w_percent))
            image = img.resize((IMG_WIDTH, h_size), Image.ANTIALIAS)
            image.save(os.path.join(upload_min_dir, file.filename))

    return jsonify(files=file_info)
