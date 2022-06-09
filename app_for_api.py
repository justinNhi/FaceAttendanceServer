import json
import dlib
import numpy as np
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from keras_vggface import VGGFace
# from database_model import
import new_data_models
from methods import *
from FaceAligner import FaceAligner
from PIL import Image, ImageFont, ImageDraw
import tensorflow as tf
from datetime import date, timedelta, datetime

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
            label = str(id_number_person) + ' ' + full_name
            probability = (1 - score) * 100
            break
        else:
            ind_id = 0
            label = str("Unknow")
            probability = (1 - score) * 100

    return label, probability, ind_id


@app.route('/return_date_today_attendance', methods=['POST'])
def return_date_today_attendance():
    json_send = get_json_all_check_in()
    print(json_send)
    return json.dumps(json_send)
    # return json_send


@app.route('/return_date_today_check_out', methods=['POST'])
def return_date_today_check_out():
    json_send = get_json_all_check_out()
    print(json_send)
    return json.dumps(json_send)
    # return json_send

@app.route('/api_face_recognition_check_in', methods=['POST'])
def api_face_recognition_check_in():
    person_id = 0
    person_name = ''
    error_code = 400
    msg = "Bad Request"
    get_reload = 0
    try:
        json = request.get_json()
        data = json['data']
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
                name, probability, id_person = predict_guest(faceAligned)  # get prediction return label and probability
                if id_person == 0:
                    error_code = 404
                    msg = 'Not Found'
                    get_reload = 0
                else:
                    rs = insert_check_in(id_person, face_img_base64)
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
        'PERSON_ID': person_id,
        'PERSON_NAME': person_name,
        'GET_RELOAD': get_reload
    }}
    print(js_return)
    return js_return

@app.route('/api_face_recognition_check_out', methods=['POST'])
def api_face_recognition_check_out():
    person_id = 0
    person_name = ''
    error_code = 400
    msg = "Bad Request"
    get_reload = 0
    try:
        json = request.get_json()
        data = json['data']
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
                name, probability, id_person = predict_guest(faceAligned)  # get prediction return label and probability
                if id_person == 0:
                    error_code = 404
                    msg = 'Not Found'
                    get_reload = 0
                else:
                    rs = insert_check_out(id_person, face_img_base64)
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
        'PERSON_ID': person_id,
        'PERSON_NAME': person_name,
        'GET_RELOAD': get_reload
    }}
    print(js_return)
    return js_return


@app.route('/return_list_of_users', methods=['POST'])
def return_list_of_users():
    json_send = get_list_of_usets()
    print(json_send)
    return json.dumps(json_send)
    # return json_send
#
# @app.route('/user registration', methods=['POST'])
# def registration():
#     person_id = 0
#     person_name = ''
#     error_code = 400
#     msg = "Bad Request"
#     get_reload = 0
#     try:
#         json = request.get_json()
#         data = json['data']
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
#                 name, probability, id_person = predict_guest(faceAligned)  # get prediction return label and probability
#                 if id_person == 0:
#                     error_code = 404
#                     msg = 'Not Found'
#                     get_reload = 0
#                 else:
#                     rs = insert_check_out(id_person, face_img_base64)
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
#         'PERSON_ID': person_id,
#         'PERSON_NAME': person_name,
#         'GET_RELOAD': get_reload
#     }}
#     print(js_return)
#     return js_return



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
