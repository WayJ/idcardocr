import json
import requests
import cv2
import base64
import numpy as np

url = "http://127.0.0.1:8866/predict/ocr_system"


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def ocrByHttp(pic_tmp_dict):
    # 打印values的数据类型,输出<class 'dict'>
    listKey = []
    listImage = []
    for k, v in pic_tmp_dict.items():
        listKey.append(k)
        listImage.append(cv2_base64(v))

    # base64_str = cv2_base64(umat_pic)
    data = {
        'images': listImage
    }
    # json.dump将python对象编码成json字符串
    values_json = json.dumps(data, cls=MyEncoder)
    # headers中添加上content-type这个参数，指定为json格式
    headers = {'Content-Type': 'application/json'}
    # requests库提交数据进行post请求
    req = requests.post(url, headers=headers, data=values_json)
    # 打印Unicode编码格式的json数据
    # print(req.text)
    # 使用json.dumps()时需要对象相应的类型是json可序列化的
    # change = req.json()
    # json.dumps序列化时对中文默认使用ASCII编码,如果无任何配置则打印的均为ascii字符,输出中文需要指定ensure_ascii=False
    # new_req = json.dumps(change, ensure_ascii=False)
    jsonData = json.loads(req.text)
    # 打印接口返回的数据,且以中文编码
    result_ocr = dict()
    for i in range(len(listKey)):
        valueStr = ''
        try:
            array = jsonData['results'][i]
            for x in range(len(array)):
                valueStr += array[x]['text']
        except Exception:
            valueStr = ''
        result_ocr[listKey[i]] = valueStr
    return result_ocr


# cv2转base64
def cv2_base64(image):
    base64_str = cv2.imencode('.jpg', image)[1].tostring()
    base64_str = base64.b64encode(base64_str)
    return base64_str


# base64转cv2


def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.fromstring(imgString, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image
