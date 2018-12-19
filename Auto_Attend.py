# -*- coding: utf-8 -*-

import cv2
import os
import re
import sys
import shutil
from PIL import Image
import pyocr.builders
import numpy as np
import pand
# 読み込んだファイル数をカウント
def count_file():

    """

    :return: <int> The number of file
    """

    # ファイルリスト
    files = os.listdir('./SubmitForm')

    # ファイル数
    count = 0

    for file in files:
        index = re.search(".jpg", file)
        if index:
            count += 1

    return count


# 塗りつぶされている箇所を切り取る
def cut_image(img, tmp_img, a, b):

    result = cv2.matchTemplate(img, tmp_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    raw_top_left = max_loc
    width, height = tmp_img.shape[::-1]
    bottom_right = (raw_top_left[0] + width + a, raw_top_left[1] + height + b)
    crop_img = img[raw_top_left[1]:bottom_right[1], raw_top_left[0]:bottom_right[0]]
    return crop_img


# ２値化
def binarization(crop_img):
    """

    :param crop_img: Cropped Image
    :return: Binary image
    """
    THRESHOLD = 200
    ret, binary_img = cv2.threshold(crop_img, THRESHOLD, 255, cv2.THRESH_BINARY)
    return binary_img


# 塗られている場所を抽出
def get_marked_point(binary_img, binary_tmp_img):

    """

    :param binary_img: Binary images
    :param binary_tmp_img: Binary template image
    :return: <list> Top Left Coordinates
    """
    results = cv2.matchTemplate(binary_img, binary_tmp_img, cv2.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where(results >= threshold)
    top_left = []
    count = 0

    # 同じ箇所をマッチングしているデータをひつだけにする
    for coordinate in zip(*loc[::-1]):

        # リストが空の場合
        if not top_left:
            top_left.append([coordinate[0], coordinate[1]])

        # 縦方向で判断
        elif abs(coordinate[1] - top_left[count][1]) > 50:
            top_left.append([coordinate[0], coordinate[1]])
            count += 1

    return top_left


# マークされている距離（横方向）から番号を決める
def get_student_num(top_left):

    """

    :param top_left: <list> Top Left Coordinates
    :return: <str> Student Number
    """

    # 学籍番号
    student_num = ''

    # 左端からの各番号までの距離
    #              0    1   2    3    4    5    6    7    8    9
    number_dis = [760, 70, 145, 220, 300, 375, 450, 530, 600, 680]

    # 誤差が15以下の箇所を番号とする
    for w, h in top_left:
        for i in range(len(number_dis)):
            mistake = abs(number_dis[i] - w)
            if mistake <= 15:
                student_num += str(i)
                break

    return student_num


# ファイル名を変更と無記名の用紙を移動
def rename_file(student_num, paper_num, late_num, num):

    """

    :param student_num: <str> Student number
    :param paper_num: <int> Number of Paper
    :param late_num: <int> Late Number
    :param num: <int> File Number
    """

    # 学籍番号がマークされているか判断
    if not student_num:
        # 無記名者は無記名ディレクトリへ移動
        shutil.move('./SubmitForm/%s.jpg' % num, './SubmitForm/Anonymous/%s_%s.jpg' % (paper_num, num))
    elif paper_num > late_num:
        # ファイル名を学籍番号へ変更
        os.rename('./SubmitForm/%s.jpg' % num, './SubmitForm/%s_1%s.jpg' % (paper_num, student_num))
    else:
        # 遅刻者は別ディレクトリへ移動
        os.rename('./SubmitForm/%s.jpg' % num, './SubmitForm/LateArrival/%s_1%s.jpg' % (paper_num, student_num))


# 紙番号をも読み取る
def check_paper_num(crop_img):

    """

    :param crop_img: Cropped Image
    :return: <int> Paper number
    """
    img_pil = Image.fromarray(crop_img).convert('RGB')
    tools = pyocr.get_available_tools()

    if len(tools) == 0:
        print('No OCR tool found')
        sys.exit(1)

    tool = tools[0]
    num = tool.image_to_string(
        img_pil,
        lang='eng',
        builder=pyocr.builders.DigitBuilder(tesseract_layout=6)
    )

    return int(num)


def check_attendance(paper_num, late_num):
    if not student_num:
        return 2
    elif paper_num > late_num:
        return 0
    else:
        return 1


def input_csv(student_num, date_num, attendance):
    df = pd.read_csv('Computer_configuration_theory.csv', encoding='utf_8', index_col=0)
    df.at[student_num, date_num] = attendance


if __name__ == '__main__':

    try:
        late_num = int(sys.argv[1])
        date_num = str(sys.argv[2])

    except IndexError:
        print()
        print('\n Please input both the late number and the date as the argument. \n')
        sys.exit(1)

    # ファイル
    Number_of_Paper = count_file()

    # マークシート部分のフォーマット（グレースケール）
    tmp_img = cv2.imread('./TemplateForm/student_number_form.jpg', 0)

    # マークを黒塗りした部分の画像（グレースケール）
    binary_tmp_img = cv2.imread('./TemplateForm/marked_point_img.png', 0)

    # 紙番号読み込みフォーマット
    paper_num_img = cv2.imread('./TemplateForm/00.png', 0)

    for i in range(1, Number_of_Paper + 1):

        # 答案用紙（グレースケール）
        img = cv2.imread('./SubmitForm/%s.jpg' % i, 0)

        # マークシート部分の画像
        crop_img = cut_image(img, tmp_img, 0, 0)

        # ２値化した画像
        binary_img = binarization(crop_img)

        #
        top_left = get_marked_point(binary_img, binary_tmp_img)

        # 学籍番号
        student_num = get_student_num(top_left)

        # 紙番号
        paper_num = check_paper_num(cut_image(img, paper_num_img, 70, 0))

        # ファイル名を紙番号と学籍番号へ変更
        rename_file(student_num, paper_num, late_num, i)

        attendance = check_attendance(paper_num, late_num)
        input_csv('1' + student_num, late_num, attendance)