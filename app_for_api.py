import json
import os
import sys

from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
import dlib
import numpy as np
from keras_vggface import VGGFace
# from database_model import
# import new_data_models
from FaceAligner import FaceAligner
from PIL import Image, ImageFont, ImageDraw
import tensorflow as tf
from datetime import date, timedelta, datetime
from methods import *
# from new_data_models import *
from app_for_api_data_model import get_check_all, data_person_label_embedding, insert_auto_attendance, insert_person, get_person, data_attendances_date_month_year, person_attendance_table

from methods_account import check_account_log_in
from methods_by_hieu import get_data_history
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SQLALCHEMY_ECHO"] = True



def predict_guest(image):
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_arr = Image.fromarray(np.uint8(imageRGB))  # array to image
    image_arr = image_arr.resize((224, 224))
    face_array = asarray(image_arr)
    # img_show = PIL.Image.fromarray(face_array)
    # img_show.show()
    faces = []
    faces.append(face_array)
    # image_arr = img_to_array(image_arr)
    # image_np = np.expand_dims(image_arr, axis=0)
    samples = asarray(faces, 'float32')
    samples = preprocess_input(samples, version=2)
    with graph.as_default():
        emb = model.predict(samples)[0]
    label = ''
    label2 = ''
    probability = 0
    ind_id = 0
    embs = data_person_label_embedding()
    for emb_person in embs:
        id_person = emb_person['PERSON_ID']
        id_number_person = emb_person['PERSON_ID_NUMBER']
        person_emb = emb_person['PERSON_EMB']
        full_name = emb_person['FULL_NAME']
        score = cosine(emb, person_emb)
        score = round(score, 2)
        if score < 0.3:
            ind_id = id_person
            label = str(id_number_person)
            label2 = str(full_name)
            probability = (1 - score) * 100
            break
        else:
            ind_id = 0
            label = str("Unknow")
            label2 = str("Unknow")
            probability = (1 - score) * 100

    return label,label2 , probability, ind_id

def get_emb(image):
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_arr = Image.fromarray(np.uint8(imageRGB))  # array to image
    image_arr = image_arr.resize((224, 224))
    face_array = asarray(image_arr)
    # img_show = PIL.Image.fromarray(face_array)
    # img_show.show()
    faces = []
    faces.append(face_array)
    # image_arr = img_to_array(image_arr)
    # image_np = np.expand_dims(image_arr, axis=0)
    samples = asarray(faces, 'float32')
    samples = preprocess_input(samples, version=2)
    with graph.as_default():
        emb = model.predict(samples)[0]
    emb_byte = emb.tobytes()

    return emb_byte


# @app.route('/return_attendance_table_date', methods=['POST'])
# def return_attendance_table_date():
#     json_get = request.get_json()
#     print(json_get)
#     # data = json_get['data']
#     # date_send = data['date_send']
#     date_send = datetime.today().strftime('%Y-%m-%d')
#
#     # print(date_send)
#     json_send = attendance_table(date_send)
#     print(json_send)
#     return json.dumps(json_send)
#
#
# @app.route('/return_date_today_attendance', methods=['POST'])
# def return_date_today_attendance():
#     date_insert = date.today().strftime('%Y-%m-%d')
#     json_send = get_check_in(date_insert)
#     print(json_send)
#     return json.dumps(json_send)
#     # return json_send
#
# @app.route('/return_date_today_check_out', methods=['POST'])
# def return_date_today_check_out():
#     date_insert = datetime.today().strftime('%Y-%m-%d')
#     json_send = get_check_out(date_insert)
#     print(json_send)
#     return json.dumps(json_send)
#     # return json_send
#
# @app.route('/api_face_recognition_check_in', methods=['POST'])
# def api_face_recognition_check_in():
#     person_id = 0
#     person_name = ''
#     person_id_number = ''
#     error_code = 400
#     msg = "Bad Request"
#     get_reload = 0
#     data_insert_return = {}
#     try:
#         json_get = request.get_json()
#         data = json_get['data']
#         student_image = data['SEND_IMAGE']
#         str_base64 = student_image.split(',')[-1]
#         str_decode_base64 = base64.b64decode(str_base64)
#         im_arr = np.frombuffer(str_decode_base64, dtype=np.uint8)  # im_arr is one-dim Numpy array
#         img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
#         img = cv2.resize(img, (W, H))
#         img = cv2.flip(img, 1)
#         rects = detector(img)  # get face detection from Dlib
#         if len(rects) > 0:
#             for rect in rects:
#                 faceAligned = fa.align(img, rect)  # processing face aligned
#                 retval, buffer = cv2.imencode('.jpg', faceAligned)
#                 face_img_base64 = base64.b64encode(buffer)
#                 person_id_number, name, probability, id_person = predict_guest(faceAligned)  # get prediction return label and probability
#                 if id_person == 0:
#                     error_code = 404
#                     msg = 'Not Found'
#                     get_reload = 0
#                 else:
#                     rs , data_insert_return = insert_check_in(id_person, face_img_base64)
#                     error_code = 200
#                     if rs == 200:
#                         msg = 'ReLoad'
#                         get_reload = 1
#                     else:
#                         msg = 'Successful'
#                         get_reload = 0
#
#                 person_name = name
#                 person_id = int(id_person)
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(e, exc_type, fname, exc_tb.tb_lineno)
#         error_code = 400
#         msg = 'Bad Request None STUDENT_ID_NUMBER ' + str(e)
#         im_b64 = ''
#     js_return = {"errorCode": error_code, "message": msg, "data": {
#         'PERSON_ID_NUMBER': person_id_number,
#         'PERSON_NAME': person_name,
#         'GET_RELOAD': get_reload,
#         'DATA_RETURN': data_insert_return
#     }}
#     print(js_return)
#     return js_return
#
# @app.route('/api_face_recognition_check_out', methods=['POST'])
# def api_face_recognition_check_out():
#     person_id = 0
#     person_name = ''
#     person_id_number = ''
#     error_code = 400
#     msg = "Bad Request"
#     get_reload = 0
#     data_insert_return = {}
#     try:
#         json_get = request.get_json()
#         data = json_get['data']
#         student_image = data['SEND_IMAGE']
#         str_base64 = student_image.split(',')[-1]
#         str_decode_base64 = base64.b64decode(str_base64)
#         im_arr = np.frombuffer(str_decode_base64, dtype=np.uint8)  # im_arr is one-dim Numpy array
#         img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
#         img = cv2.resize(img, (W, H))
#         img = cv2.flip(img, 1)
#         rects = detector(img)  # get face detection from Dlib
#         if len(rects) > 0:
#             for rect in rects:
#                 faceAligned = fa.align(img, rect)  # processing face aligned
#                 retval, buffer = cv2.imencode('.jpg', faceAligned)
#                 face_img_base64 = base64.b64encode(buffer)
#                 person_id_number, name, probability, id_person = predict_guest(faceAligned)  # get prediction return label and probability
#                 if id_person == 0:
#                     error_code = 404
#                     msg = 'Not Found'
#                     get_reload = 0
#                 else:
#                     rs, data_insert_return = insert_check_out(id_person, face_img_base64)
#                     error_code = 200
#                     if rs == 200:
#                         msg = 'ReLoad'
#                         get_reload = 1
#                     else:
#                         msg = 'Successful'
#                         get_reload = 0
#
#                 person_name = name
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(e, exc_type, fname, exc_tb.tb_lineno)
#         error_code = 400
#         msg = 'Bad Request None STUDENT_ID_NUMBER ' + str(e)
#         im_b64 = ''
#     js_return = {"errorCode": error_code, "message": msg, "data": {
#         'PERSON_ID_NUMBER': person_id_number,
#         'PERSON_NAME': person_name,
#         'GET_RELOAD': get_reload,
#         'DATA_RETURN': data_insert_return
#     }}
#     print(js_return)
#     return js_return


@app.route('/return_list_of_users', methods=['POST'])
def return_list_of_users():
    json_send = get_person()
    print(json_send)
    return json.dumps(json_send)
    # return json_send
# #
# # @app.route('/user registration', methods=['POST'])
# # def registration():
# #     person_id = 0
# #     person_name = ''
# #     error_code = 400
# #     msg = "Bad Request"
# #     get_reload = 0
# #     try:
# #         json = request.get_json()
# #         data = json['data']
# #         student_image = data['SEND_IMAGE']
# #         str_base64 = student_image.split(',')[-1]
# #         str_decode_base64 = base64.b64decode(str_base64)
# #         im_arr = np.frombuffer(str_decode_base64, dtype=np.uint8)  # im_arr is one-dim Numpy array
# #         img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
# #         img = cv2.resize(img, (W, H))
# #         img = cv2.flip(img, 1)
# #         rects = detector(img)  # get face detection from Dlib
# #         if len(rects) > 0:
# #             for rect in rects:
# #                 faceAligned = fa.align(img, rect)  # processing face aligned
# #                 retval, buffer = cv2.imencode('.jpg', faceAligned)
# #                 face_img_base64 = base64.b64encode(buffer)
# #                 name, probability, id_person = predict_guest(faceAligned)  # get prediction return label and probability
# #                 if id_person == 0:
# #                     error_code = 404
# #                     msg = 'Not Found'
# #                     get_reload = 0
# #                 else:
# #                     rs = insert_check_out(id_person, face_img_base64)
# #                     error_code = 200
# #                     if rs == 200:
# #                         msg = 'ReLoad'
# #                         get_reload = 1
# #                     else:
# #                         msg = 'Successful'
# #                         get_reload = 0
# #
# #                 person_name = name
# #                 person_id = int(id_person)
# #     except Exception as e:
# #         exc_type, exc_obj, exc_tb = sys.exc_info()
# #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
# #         print(e, exc_type, fname, exc_tb.tb_lineno)
# #         error_code = 400
# #         msg = 'Bad Request None STUDENT_ID_NUMBER ' + str(e)
# #         im_b64 = ''
# #     js_return = {"errorCode": error_code, "message": msg, "data": {
# #         'PERSON_ID': person_id,
# #         'PERSON_NAME': person_name,
# #         'GET_RELOAD': get_reload
# #     }}
# #     print(js_return)
# #     return js_return
#
@app.route('/api_registration', methods=['POST'])
def api_registration():
    error_code = 400
    msg = "Bad Request"
    js_return = {}
    try:
        json_get = request.get_json()
        json_data = json_get['data']
        person_id_number = json_data['PERSON_ID_NUMBER']
        first_name= json_data['FIRST_NAME']
        middle_name = json_data['MIDDLE_NAME']
        last_name = json_data['LAST_NAME']
        image_base64 = json_data['image_base64']
        str_base64 = image_base64.split(',')[-1]
        # im = Image.open(BytesIO(base64.b64decode(str_base64)))
        # im.show()
        str_decode_base64 = base64.b64decode(str_base64)
        im_arr = np.frombuffer(str_decode_base64, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        img = cv2.resize(img, (W, H))
        img = cv2.flip(img, 1)
        # cv2.imshow('graycsale image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        rects = detector(img)  # get face detection from Dlib
        if len(rects) > 0:
            # for rect in rects:
            rect = rects[0]
            faceAligned = fa.align(img, rect)  # processing face aligned
            retval, buffer = cv2.imencode('.jpg', faceAligned)
            face_img_base64 = base64.b64encode(buffer)
            face_emb = get_emb(faceAligned)  # get prediction return label and probability
            error_code, js_return = insert_person(person_id_number, last_name, middle_name, first_name, face_img_base64,
                                      face_emb)
            msg = 'Successful'
            print(error_code, js_return)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        error_code = 400
        msg = 'Bad Request None STUDENT_ID_NUMBER ' + str(e)
        im_b64 = ''
    return {"errorCode": error_code, "message": msg,
            "data": js_return}

@app.route('/return_person_attendance_table', methods=['POST'])
def return_person_attendance_table():
    error_code = 400
    msg = "Bad Request"
    js_return = {}
    json_get = request.get_json()
    json_data = json_get['data']
    person_id = json_data['PERSON_ID']
    month= json_data['MONTH']
    year = json_data['YEAR']
    # json_send = {}
    json_send = person_attendance_table(person_id, month, year)
    print(json_send)
    return json_send

@app.route('/return_date_auto_attendance', methods=['POST'])
def return_date_auto_attendance():
    date_insert = date.today().strftime('%Y-%m-%d')

    morning_time_start_in = datetime.now().replace(hour=6, minute=0, second=0).strftime("%H:%M:%S")

    morning_time_stop_in = datetime.now().replace(hour=7, minute=30, second=0).strftime("%H:%M:%S")

    morning_time_start_out = datetime.now().replace(hour=10, minute=45, second=0).strftime("%H:%M:%S")

    morning_time_stop_out = datetime.now().replace(hour=11, minute=30, second=0).strftime("%H:%M:%S")

    afternoon_time_start_in = datetime.now().replace(hour=12, minute=30, second=0).strftime("%H:%M:%S")

    afternoon_time_stop_in = datetime.now().replace(hour=14, minute=0, second=0).strftime("%H:%M:%S")

    afternoon_time_start_out = datetime.now().replace(hour=16, minute=0, second=0).strftime("%H:%M:%S")

    afternoon_time_stop_out = datetime.now().replace(hour=18, minute=0, second=0).strftime("%H:%M:%S")

    datatime_now = datetime.now()

    time_now = datatime_now.strftime("%H:%M:%S")

    DATE = date.today()
    TIME = time_now
    DATETIME = datetime.now()
    json_query = {
        'DATE' : DATE,
        'TIME': TIME,
        'DATETIME': DATETIME,
    }
    print(json_query)
    if time_now >= morning_time_start_in and time_now <= morning_time_stop_in:
        json_query['SESSION_CHECK_ID'] = 1
        json_query['SESSION_ID'] =1
    elif time_now >= morning_time_start_out and time_now <= morning_time_stop_out:
        json_query['SESSION_CHECK_ID'] = 2
        json_query['SESSION_ID'] = 1
    elif time_now >= afternoon_time_start_in and time_now <= afternoon_time_stop_in:
        json_query['SESSION_CHECK_ID'] = 1
        json_query['SESSION_ID'] = 2
    elif time_now >= afternoon_time_start_out and time_now <= afternoon_time_stop_out:
        json_query['SESSION_CHECK_ID'] = 2
        json_query['SESSION_ID'] = 2
    else:
        json_query['SESSION_CHECK_ID'] = 3
        json_query['SESSION_ID'] = 3

    json_send = get_check_all(json_query)


    print(json_send)
    return json.dumps(json_send)
    # return json_send

@app.route('/return_data_attendances_date_month_year', methods=['POST'])
def return_data_attendances_date_month_year():
    error_code = 400
    msg = "Bad Request"
    js_return = {}
    json_get = request.get_json()
    json_data = json_get['data']
    month= json_data['MONTH']
    year = json_data['YEAR']
    # json_send = {}
    json_send = data_attendances_date_month_year(month, year)
    print(json_send)
    return json_send

@app.route('/api_face_recognition_auto_attendance_ipad', methods=['POST'])
def api_face_recognition_auto_attendance_ipad():
    person_id = 0
    person_name = ''
    person_id_number = ''
    error_code = 400
    msg = "Bad Request"
    get_reload = 0
    data_insert_return = {}
    try:
        json_get = request.get_json()
        data = json_get['data']
        student_image = data['SEND_IMAGE']
        str_base64 = student_image.split(',')[-1]
        str_decode_base64 = base64.b64decode(str_base64)
        im_arr = np.frombuffer(str_decode_base64, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        img = cv2.resize(img, (W, H))
        img = cv2.flip(img, 1)
        rects = detector(img)  # get face detection from Dlib
        if len(rects) > 0:
            for rect in rects:
                faceAligned = fa.align(img, rect)  # processing face aligned
                retval, buffer = cv2.imencode('.jpg', faceAligned)
                face_img_base64 = base64.b64encode(buffer)
                person_id_number, name, probability, id_person = predict_guest(faceAligned)  # get prediction return label and probability
                if id_person == 0:
                    error_code = 404
                    msg = 'Not Found'
                    get_reload = 0
                else:
                    rs , data_insert_return = insert_auto_attendance(id_person, face_img_base64)
                    error_code = 200
                    if rs == 200:
                        msg = 'ReLoad'
                        get_reload = 1
                    else:
                        msg = 'Successful'
                        get_reload = 0
                person_name = name
                person_id = int(id_person)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        error_code = 400
        msg = 'Bad Request None STUDENT_ID_NUMBER ' + str(e)
        im_b64 = ''
    js_return = {"errorCode": error_code, "message": msg, "data": {
        'PERSON_ID_NUMBER': person_id_number,
        'PERSON_NAME': person_name,
        'GET_RELOAD': get_reload,
        'DATA_RETURN': data_insert_return
    }}
    print(js_return)
    return js_return

@app.route('/return_person_profile', methods=['POST'])
def return_person_profile():
    error_code = 400
    msg = "Bad Request"
    js_return = {}
    json_get = request.get_json()
    json_data = json_get['data']

    person_id = json_data['PERSON_ID']
    try:
        month = json_data['MONTH']
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        month =  None
    try:
        year = json_data['YEAR']
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        year = None
    print(person_id, month, year)
    json_send = {}
    # json_send = data_personal_profile(person_id, month, year)
    print(json_send)
    return json_send

@app.route('/return_history', methods=['POST'])
def return_history():
    error_code = 400
    msg = "Bad Request"
    js_return = {}
    json_send = []
    try:
        json_get = request.get_json()
        json_data = json_get['data']
        # json_send = []
        try:
            today = json_data['TODAY']
            json_to_method = {
                'TODAY': today,
            }
            json_send = get_data_history(today)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, fname, exc_tb.tb_lineno)
            try:
                month = json_data['MONTH']
                year = json_data['YEAR']
                json_to_method = {
                    'MONTH': month,
                    'YEAR': year,

                }
                json_send = get_data_history(month, year)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(e, exc_type, fname, exc_tb.tb_lineno)
                try:
                    year = json_data['YEAR']
                    json_to_method = {
                        'YEAR': year,

                    }
                    json_send = get_data_history(year)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(e, exc_type, fname, exc_tb.tb_lineno)
                    json_send = []
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        json_send = []
    print("json_send", json_send)
    print(type(json_send))
    js_return = {'data_send': json_send}
    return js_return

@app.route('/check_log_in', methods=['POST'])
def check_log_in():
    error_code = 400
    msg = "Bad Request"
    json_account = {}
    try:
        json_get = request.get_json()
        json_data = json_get['data']
        account_name = str(json_data['account_name']).lower()
        account_password = str(json_data['account_password'])
        print(account_name, account_password)
        json_account = check_account_log_in(account_name, account_password)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)

    # js_return = {'data_send': json_account}
    # return json.dumps(json_account)
    return json_account


if __name__ == '__main__':
    graph = tf.get_default_graph()
    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')

    mask_back = generate_mask(640, 480)
    W = 640
    H = 480
    delta = 150
    center_x = int(W / 2)
    center_y = int(H / 2)
    color = (255, 255, 255)
    camera = cv2.VideoCapture(0)
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    detector = dlib.get_frontal_face_detector()
    fa = FaceAligner(desiredFaceWidth=150, desiredLeftEye=(0.28, 0.28))
    print(app.url_map)
    app.run(host='0.0.0.0', port=7770, debug=True, use_reloader=False)
