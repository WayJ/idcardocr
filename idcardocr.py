# -*- coding: utf-8 -*-
# from PIL import Image
from numpy.core.fromnumeric import shape
import cv2
import numpy as np
import time
import paddleocr
import datetime
import dlib


x = 1280.00 / 3840.00
pixel_x = int(x * 3840)
print(x, pixel_x)

# mode0:识别姓名，出生日期，身份证号； mode1：识别所有信息


def idcardocr(imgname, mode=1):
    print(u'进入身份证光学识别流程...')
    t1 = round(time.time() * 1000)
    if mode >= 1:
        # generate_mask(x)
        img_data_gray, img_org = img_resize_gray(imgname)
        pic_tmp_dict = {}
        name_pic = find_name(img_data_gray, img_org)
        # cv2.imwrite('tmp/name.png',name_pic)
        # showimg(name_pic)
        # print 'name'
    #     result_dict['name'] = get_name(name_pic)
        # print result_dict['name']
        pic_tmp_dict['name'] = name_pic

    #     sex_pic = find_sex(img_data_gray, img_org)
    #     showimg(sex_pic)
        # print 'sex'
    #     result_dict['sex'] = get_sex(sex_pic)

    #     pic_tmp_dict['sex'] = sex_pic
        # print result_dict['sex']

        nation_pic = find_nation(img_data_gray, img_org)
        # showimg(nation_pic)
        # print 'nation'
    #     result_dict['nation'] = get_nation(nation_pic)

        pic_tmp_dict['nation'] = nation_pic
        # print result_dict['nation']

        address_pic = find_address(img_data_gray, img_org)
        # showimg(address_pic)
        # print 'address'
    #     result_dict['address'] = get_address(address_pic)

        pic_tmp_dict['address'] = address_pic
        # print result_dict['address']

        idnum_pic = find_idnum(img_data_gray, img_org)
        # showimg(idnum_pic)
        # print 'idnum'

        pic_tmp_dict['idNumber'] = idnum_pic

        t2 = round(time.time() * 1000)
        print(u'身份证图片处理:%s ms' % (t2 - t1))
        t1 = t2
        result_dict = paddleocr.ocrByHttp(pic_tmp_dict)
        idnumInfo = GetInformation(result_dict['idNumber'])
        result_dict['sex'] = idnumInfo.get_sex()
        result_dict['age'] = idnumInfo.get_age()
        result_dict['birthday'] = idnumInfo.get_birthday()

        
        if(mode == 2):
            result_dict['avatar'] = find_avatar(img_org)
    #     result_dict['idnum'], result_dict['birth'] = get_idnum_and_birth(idnum_pic)
        # print result_dict['idnum']
    elif mode == 0:
        # generate_mask(x)
        img_data_gray, img_org = img_resize_gray(imgname)
        pic_tmp_dict = {}

        idnum_pic = find_idnum(img_data_gray, img_org)
        pic_tmp_dict['idNumber'] = idnum_pic

        result_dict = paddleocr.ocrByHttp(pic_tmp_dict)
    else:
        print(u"模式选择错误！")

    t3 = round(time.time() * 1000)
    print(u'OCR识别:%s ms' % (t3 - t1))
    # showimg(img_data_gray)
    return result_dict


def generate_mask(x):
    name_mask_pic = cv2.UMat(cv2.imread('matchimages/name_mask.jpg'))
    sex_mask_pic = cv2.UMat(cv2.imread('matchimages/sex_mask.jpg'))
    nation_mask_pic = cv2.UMat(cv2.imread('matchimages/nation_mask.jpg'))
    birth_mask_pic = cv2.UMat(cv2.imread('matchimages/birth_mask.jpg'))
    year_mask_pic = cv2.UMat(cv2.imread('matchimages/year_mask.jpg'))
    month_mask_pic = cv2.UMat(cv2.imread('matchimages/month_mask.jpg'))
    day_mask_pic = cv2.UMat(cv2.imread('matchimages/day_mask.jpg'))
    address_mask_pic = cv2.UMat(cv2.imread('matchimages/address_mask.jpg'))
    idnum_mask_pic = cv2.UMat(cv2.imread('matchimages/idnum_mask.jpg'))
    name_mask_pic = img_resize_x(name_mask_pic)
    sex_mask_pic = img_resize_x(sex_mask_pic)
    nation_mask_pic = img_resize_x(nation_mask_pic)
    birth_mask_pic = img_resize_x(birth_mask_pic)
    year_mask_pic = img_resize_x(year_mask_pic)
    month_mask_pic = img_resize_x(month_mask_pic)
    day_mask_pic = img_resize_x(day_mask_pic)
    address_mask_pic = img_resize_x(address_mask_pic)
    idnum_mask_pic = img_resize_x(idnum_mask_pic)
    cv2.imwrite('matchimages/name_mask_%s.jpg' % pixel_x, name_mask_pic)
    cv2.imwrite('matchimages/sex_mask_%s.jpg' % pixel_x, sex_mask_pic)
    cv2.imwrite('matchimages/nation_mask_%s.jpg' % pixel_x, nation_mask_pic)
    cv2.imwrite('matchimages/birth_mask_%s.jpg' % pixel_x, birth_mask_pic)
    cv2.imwrite('matchimages/year_mask_%s.jpg' % pixel_x, year_mask_pic)
    cv2.imwrite('matchimages/month_mask_%s.jpg' % pixel_x, month_mask_pic)
    cv2.imwrite('matchimages/day_mask_%s.jpg' % pixel_x, day_mask_pic)
    cv2.imwrite('matchimages/address_mask_%s.jpg' % pixel_x, address_mask_pic)
    cv2.imwrite('matchimages/idnum_mask_%s.jpg' % pixel_x, idnum_mask_pic)

# 用于生成模板


def img_resize_x(imggray):
    # print 'dheight:%s' % dheight
    crop = imggray
    size = crop.get().shape
    dheight = int(size[0]*x)
    dwidth = int(size[1]*x)
    crop = cv2.resize(src=crop, dsize=(dwidth, dheight),
                      interpolation=cv2.INTER_CUBIC)
    return crop

#idcardocr里面resize以高度为依据, 用于get部分


def img_resize(imggray, dheight):
    # print 'dheight:%s' % dheight
    crop = imggray
    size = crop.get().shape
    height = size[0]
    width = size[1]
    width = width * dheight / height
    crop = cv2.resize(src=crop, dsize=(int(width), dheight),
                      interpolation=cv2.INTER_CUBIC)
    return crop


def img_resize_gray(imgorg):

    #imgorg = cv2.imread(imgname)
    crop = imgorg
    size = cv2.UMat.get(crop).shape
    # print size
    height = size[0]
    width = size[1]
    # 参数是根据3840调的
    height = int(height * 3840 * x / width)
    # print height
    crop = cv2.resize(src=crop, dsize=(int(3840 * x), height),
                      interpolation=cv2.INTER_CUBIC)
    return hist_equal(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)), crop


def find_name(crop_gray, crop_org):
    template = cv2.UMat(cv2.imread(
        'matchimages/name_mask_%s.jpg' % pixel_x, 0))
    # showimg(crop_org)
    w, h = cv2.UMat.get(template).shape[::-1]
    res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(max_loc)
    top_left = (max_loc[0] + w, max_loc[1] - int(20*x))
    bottom_right = (top_left[0] + int(700*x), top_left[1] + int(300*x))
    result = cv2.UMat.get(crop_org)[
        top_left[1]-10:bottom_right[1], top_left[0]-10:bottom_right[0]]
    cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
    # showimg(result)
    return cv2.UMat(result)


def find_sex(crop_gray, crop_org):
    template = cv2.UMat(cv2.imread('matchimages/sex_mask_%s.jpg' % pixel_x, 0))
    # showimg(template)
    w, h = cv2.UMat.get(template).shape[::-1]
    res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = (max_loc[0] + w, max_loc[1] - int(20*x))
    bottom_right = (top_left[0] + int(300*x), top_left[1] + int(300*x))
    result = cv2.UMat.get(crop_org)[
        top_left[1]-10:bottom_right[1], top_left[0]-10:bottom_right[0]]
    cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
    # showimg(crop_gray)
    return cv2.UMat(result)


def find_nation(crop_gray, crop_org):
    template = cv2.UMat(cv2.imread(
        'matchimages/nation_mask_%s.jpg' % pixel_x, 0))
    # showimg(template)
    w, h = cv2.UMat.get(template).shape[::-1]
    res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = (max_loc[0] + w - int(20*x), max_loc[1] - int(20*x))
    bottom_right = (top_left[0] + int(500*x), top_left[1] + int(300*x))
    result = cv2.UMat.get(crop_org)[
        top_left[1]-10:bottom_right[1], top_left[0]-10:bottom_right[0]]
    cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
    # showimg(crop_gray)
    return cv2.UMat(result)

def find_address(crop_gray, crop_org):
    template = cv2.UMat(cv2.imread(
        'matchimages/address_mask_%s.jpg' % pixel_x, 0))
    # showimg(template)
    # showimg(crop_gray)
    w, h = cv2.UMat.get(template).shape[::-1]
    #t1 = round(time.time()*1000)
    res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
    #t2 = round(time.time()*1000)
    # print 'time:%s'%(t2-t1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = (max_loc[0] + w, max_loc[1] - int(20*x))
    bottom_right = (top_left[0] + int(1700*x), top_left[1] + int(550*x))
    result = cv2.UMat.get(crop_org)[
        top_left[1]-10:bottom_right[1], top_left[0]-10:bottom_right[0]]
    cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
    # showimg(crop_gray)
    return cv2.UMat(result)


def find_idnum(crop_gray, crop_org):
    template = cv2.UMat(cv2.imread(
        'matchimages/idnum_mask_%s.jpg' % pixel_x, 0))
    # showimg(template)
    # showimg(crop_gray)
    w, h = cv2.UMat.get(template).shape[::-1]
    res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = (max_loc[0] + w, max_loc[1] - int(20*x))
    bottom_right = (top_left[0] + int(2300*x), top_left[1] + int(300*x))
    result = cv2.UMat.get(crop_org)[
        top_left[1]-10:bottom_right[1], top_left[0]-10:bottom_right[0]]
    cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
    # showimg(crop_gray)
    return cv2.UMat(result)


def find_avatar(img):
    # img = cv2.imread(img_name)
    detector = dlib.get_frontal_face_detector()  # 获得正脸检测器
    array2d = img.get()
    faces = detector(array2d, 1)  # 返回检测到的每张脸
    if faces:
        face=faces[0]
        # 用矩形画出检测到的人脸范围
        shape = array2d.shape
        top = int(shape[0]/20*3)
        bottom = int(shape[0]/20*15)
        ycenter = int((face.left()+face.right())/2)
        d = int(shape[1]/3/2)
        # cv2.rectangle(img, (ycenter-d, top), (ycenter+d, bottom), (0, 0, 255), 3)
        cropped = array2d[top:bottom, ycenter-d:ycenter+d] # 裁剪坐标为[y0:y1, x0:x1]
        return paddleocr.cv2_base64(cv2.UMat(cropped))
        # return 'data:image/jpg;base64,%s' % paddleocr.cv2_base64(cv2.UMat(cropped))
    else:
        return ''

def showimg(img):
    cv2.namedWindow("contours", 0)
    cv2.resizeWindow("contours", 1280, 720)
    cv2.imshow("contours", img)
    cv2.waitKey()

# psm model:
#  0    Orientation and script detection (OSD) only.
#  1    Automatic page segmentation with OSD.
#  2    Automatic page segmentation, but no OSD, or OCR.
#  3    Fully automatic page segmentation, but no OSD. (Default)
#  4    Assume a single column of text of variable sizes.
#  5    Assume a single uniform block of vertically aligned text.
#  6    Assume a single uniform block of text.
#  7    Treat the image as a single text line.
#  8    Treat the image as a single word.
#  9    Treat the image as a single word in a circle.
#  10    Treat the image as a single character.
#  11    Sparse text. Find as much text as possible in no particular order.
#  12    Sparse text with OSD.
#  13    Raw line. Treat the image as a single text line,
# 			bypassing hacks that are Tesseract-specific


# def punc_filter(str):
#     temp = str
#     xx = u"([\u4e00-\u9fff0-9A-Z]+)"
#     pattern = re.compile(xx)
#     results = pattern.findall(temp)
#     string = ""
#     for result in results:
#         string += result
#     return string

# 这里使用直方图拉伸，不是直方图均衡


def hist_equal(img):
    # clahe_size = 8
    # clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(clahe_size, clahe_size))
    # result = clahe.apply(img)
    # test

    #result = cv2.equalizeHist(img)

    image = img.get()  # UMat to Mat
    # result = cv2.equalizeHist(image)
    lut = np.zeros(256, dtype=image.dtype)  # 创建空的查找表
    #lut = np.zeros(256)
    hist = cv2.calcHist([image],  # 计算图像的直方图
                        [0],  # 使用的通道
                        None,  # 没有使用mask
                        [256],  # it is a 1D histogram
                        [0, 256])
    minBinNo, maxBinNo = 0, 255
    # 计算从左起第一个不为0的直方图柱的位置
    for binNo, binValue in enumerate(hist):
        if binValue != 0:
            minBinNo = binNo
            break
    # 计算从右起第一个不为0的直方图柱的位置
    for binNo, binValue in enumerate(reversed(hist)):
        if binValue != 0:
            maxBinNo = 255-binNo
            break
    # print minBinNo, maxBinNo
    # 生成查找表
    for i, v in enumerate(lut):
        if i < minBinNo:
            lut[i] = 0
        elif i > maxBinNo:
            lut[i] = 255
        else:
            lut[i] = int(255.0*(i-minBinNo)/(maxBinNo-minBinNo)+0.5)
    # 计算,调用OpenCV cv2.LUT函数,参数 image --  输入图像，lut -- 查找表
    # print lut
    result = cv2.LUT(image, lut)
    # print type(result)
    # showimg(result)
    return cv2.UMat(result)


class GetInformation(object):
    def __init__(self, id):
        self.id = id
        self.birthdayStr =  "%s-%s-%s" % (self.id[6:10], self.id[10:12], self.id[12:14])
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    def get_birthday(self):
        # 通过身份证号获取出生日期
        # birthday = "%s-%s-%s" % (self.birth_year,
        #                                 self.birth_month, self.birth_day)
        return self.birthdayStr
        # if(len(self.id)==18):
        #         return self.id[6:14]
        # else:

    def get_sex(self):
        # 男生：1 女生：0
        num = int(self.id[16:17])
        if num % 2 == 0:
            return '女'
        else:
            return '男'

    def get_age(self):
        # 获取年龄
        now = (datetime.datetime.now() + datetime.timedelta(days=1))
        year = now.year
        month = now.month
        day = now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year


if __name__ == "__main__":
    idocr = idcardocr(cv2.UMat(cv2.imread('testimages/zrh.jpg')))
    print(idocr)
    # for i in range(15):
    #     idocr = idcardocr(cv2.UMat(cv2.imread('testimages/%s.jpg'%(i+1))))
    #     print(idocr['idnum'])
