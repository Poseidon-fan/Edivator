import io
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR, draw_ocr  # type: ignore
import base64

import urllib
import requests

# from intelli.ocr.test_base64_img_sample import base64_str

API_KEY = ""
SECRET_KEY = ""


def pattern_recognition(base64_image):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token=" + get_access_token()

    payload = 'image=' + base64_image + '&baike_num=5'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials",
              "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


class OCRbot():
    def __init__(self, language='ch') -> None:

        self.ocr_service = PaddleOCR(use_angle_cls=True, lang=language)

    def infer_img_base64(self, base64_img_code: str):
        img = base64.urlsafe_b64decode(base64_img_code)
        image = Image.open(io.BytesIO(img))
        image = np.array(image)
        result = self.ocr_service.ocr(image)
        return result[0]

    def infer_img_path(self, img_path: str):
        result = self.ocr_service.ocr(img_path)
        return result

    def infer_img_and_return(self, base64_img_code: str):
        result = self.infer_img_base64(base64_img_code)
        image = base64.b64decode(base64_img_code)
        image = Image.open(io.BytesIO(image)).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        im_show = draw_ocr(image, boxes, txts,
                           font_path='./fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        return im_show, txts

    def recognize_pattern(self, base64_img_code: str):
        result = pattern_recognition(base64_img_code)
        return result
