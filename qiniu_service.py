# -*- coding: utf-8 -*-
# flake8: noqa
import logging

from qiniu import Auth, put_file, etag
import qiniu.config
from datetime import datetime

logger = logging.getLogger(__name__)


class QiniuService(object):
    
    def __init__(self, ak, sk, domain, bucket):
        self.auth = Auth(ak, sk)
        self.domain = domain
        self.bucket = bucket
    
    def _build_upload_token(self, target_name, bucket, expire=3600):
        token = self.auth.upload_token(bucket, target_name, expire)
        return token
    
    def upload_picture(
        self, src_path, bucket=None, target_name=None, version="v2"
    ):
        if not bucket:
            if not self.bucket:
                raise Exception("bucket must be specified!")
            bucket = self.bucket
        
        if target_name:
            target_name = str(target_name)
        else:  # construct target name by timestamp
            target_name = "-".join(str(datetime.now()).split()) + ".png"
            
        token = self._build_upload_token(target_name, bucket=bucket)
        result, info = put_file(token, target_name, src_path, version=version)
        
        code = info.status_code
        
        if code != 200:
            return {"status_code": code}
        
        link = self.domain + "/" + result["key"]
        
        message = {
            "status_code": code,
            "hash": result["hash"],
            "upload_name": result["key"],
            "link": link,
            "markdown_link": f"![{target_name}]({link})",
            "html_link": f"<img src='{link}' alt='{target_name}' "
                          "style='zoom:67%;' />"
        }
        
        return message
