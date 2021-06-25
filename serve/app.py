import os
import sys
import logging
from PIL import Image
from flask import Flask, render_template, request

sys.path.append("../..")
from qiniu_uploader.qiniu_service import QiniuService
from qiniu_uploader.config import access_key, secret_key, domain, bucket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

qiniu = QiniuService(access_key, secret_key, domain, bucket)


@app.route("/", methods=['POST'])
def upload():
    img = Image.open(request.files['image'])
    
    tmp_file = "tmp.png"
    
    # saving file...
    img.save(tmp_file)
    
    # uploading file
    msg = qiniu.upload_picture(tmp_file)
    
    # Deleting file... 
    os.remove(tmp_file)

    if msg.get("status_code") == 200:
        logger.info(f"SUCCEED|link:{msg.get('link')}|hash:{msg.get('hash')}")
    else:
        logger.error("FAILED")  # todo add error info
        
    return msg
