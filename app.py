import json
import dlib
import numpy as np
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from keras_vggface import VGGFace
# from database_model import *
from methods import *
from FaceAligner import FaceAligner
from PIL import Image, ImageFont, ImageDraw
import tensorflow as tf
from datetime import date, timedelta, datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True



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


@app.route('/')
def hello_world():  # put application's code here
    data_attendances_date_auto_for_day()
    page_data, to_date = data_attendances_today()
    print(page_data)
    for a in page_data:
        print(a)
    return render_template('index.html', data_attendances_date=page_data, to_date = to_date)

@app.route('/register')
def register():  # put application's code here
    data_attendances_date_auto_for_day()
    page_num = 1
    page_limit = 10

    if 'page' in request.args:
        page_num = int(request.args.get('page'))
    if 'limit' in request.args:
        page_limit = int(request.args.get('limit'))

    page_data, max_page = data_person_image(page_num, page_limit)

    paging_data = {
        'page': page_num,
        'limit': page_limit,
        'total_page': max_page
    }

    return render_template('register.html', data_person_image=page_data, paging_data=paging_data)


@app.route('/danhsachdiemdanh')
def danhsachdiemdanh():  # put application's code here
    data_attendances_date_auto_for_day()

    tab = get_default_attendances_tab()
    page_num = 1
    page_limit = 10

    if 'tab' in request.args:
        tab = request.args.get('tab')
    if 'page' in request.args:
        page_num = int(request.args.get('page'))
    if 'limit' in request.args:
        page_limit = int(request.args.get('limit'))

    page_data, max_page = data_attendances_date(page_num, page_limit)
    paging_data = {
        'tab': tab,
        'page': page_num,
        'limit': page_limit,
        'total_page': max_page
    }


    return render_template('attendaces.html', data_person_images=page_data, paging_data=paging_data)


@app.route('/bangchamcong')
def bangchamcong():  # use month to query data

    month = datetime.now().month
    year = datetime.now().year

    if 'month' in request.args:
        month = int(request.args.get('month'))  # parse int is required
    if 'year' in request.args:
        year = int(request.args.get('year'))  # parse int is required


    # if int(month) >= 2 and int(month) <= 12:
    #     if len(str(int(month) - 1)) < 2:
    #         month_1 = '0' + str(int(month) - 1)
    #     else:
    #         month_1 =str(int(month) - 1)
    #     month_2 = str(int(month))
    # else:
    #     month_1 = '12'
    #     month_2 = '01'
    #
    #
    # if len(str(month)) < 2:
    #     month = '0' + str(month)
    #
    # start_date = datetime.strptime('26/' + month_1  + '/' + str(year), '%d/%m/%Y')
    # end_date = datetime.strptime('26/' + month_2  + '/' + str(year), '%d/%m/%Y')
    #
    #
    #
    # nguyen_van_a_attendaces = []
    #
    # for _date in (start_date + timedelta(n) for n in range((end_date - start_date).days)):
    #     nguyen_van_a_attendaces.append({
    #         "date": _date.strftime('%Y-%m-%d'),
    #
    #         "sa_status": True,  # Co mat
    #         "sa_checkin": "7:00",
    #         "sa_checkout": "11:00",
    #
    #         "ch_status": False,  # Vang
    #         "ch_checkin": None,
    #         "ch_checkout": None,
    #
    #     })
    #
    # nguyen_van_b_attendaces = []
    # for _date in (start_date + timedelta(n) for n in range((end_date - start_date).days)):
    #     nguyen_van_b_attendaces.append({
    #         "date": _date.strftime('%Y-%m-%d'),
    #
    #         "sa_status": True,  # Co mat
    #         "sa_checkin": "7:00",
    #         "sa_checkout": "11:00",
    #
    #         "ch_status": True,  # Vang
    #         "ch_checkin": '13:00',
    #         "ch_checkout": '17:00',
    #
    #     })
    #
    # sample_data = {
    #     "month": month,  # filter month
    #     "year": year,  # filter year
    #     "current_year": datetime.now().year,  # current system year
    #     "start_date": '2021-02-26',
    #     "end_date": '2021-03-26',
    #     "data": [
    #         {
    #             "msnv": 1234,
    #             "name": 'Nguyen Van A',
    #             "attendances": nguyen_van_a_attendaces
    #         },
    #         {
    #             "msnv": 12345,
    #             "name": 'Nguyen Van B',
    #             "attendances": nguyen_van_b_attendaces
    #         },
    #     ]
    # }
    sample_data = data_attendances_date_month_year(month, year)
    print(sample_data)
    print(month, year)

    return render_template('month-attendaces.html', data=sample_data, data_json=json.dumps(sample_data))


@app.route('/bangchamcongcanhan/<int:id_person>')
def bangchamcongcanhan(id_person):  # use month and msnv to query data
    month = datetime.now().month
    year = datetime.now().year

    if 'month' in request.args:
        month = int(request.args.get('month'))  # parse int is required
    if 'year' in request.args:
        year = int(request.args.get('year'))  # parse int is required

    # start_date = datetime.strptime('26/11/2021', '%d/%m/%Y')
    # end_date = datetime.strptime('26/12/2021', '%d/%m/%Y')
    #
    # nguyen_van_a_attendaces = []
    # for _date in (start_date + timedelta(n) for n in range((end_date - start_date).days)):
    #     nguyen_van_a_attendaces.append({
    #         "date": _date.strftime('%Y-%m-%d'),
    #
    #         "sa_status": True,  # Co mat
    #         "sa_checkin": "7:00",
    #         "sa_checkout": "11:00",
    #
    #         "ch_status": False,  # Vang
    #         "ch_checkin": None,
    #         "ch_checkout": None,
    #
    #     })
    #
    # sample_data = {
    #     "msnv": 1234,
    #     "name": 'Nguyen Van A',
    #     "attendances": nguyen_van_a_attendaces,
    #     "month": month,  # filter month
    #     "year": year,  # filter year
    #     "current_year": datetime.now().year,  # current system year
    #     "start_date": '2021-11-26',
    #     "end_date": '2021-12-26',
    # }
    sample_data = data_attendances_personnal_date_month_year(id_person, month, year)
    print(sample_data)
    print(month, year)

    return render_template('personal-attendaces.html', data=sample_data, data_json=json.dumps(sample_data))


@app.route('/danhsachnguoidung')
def danhsachnguoidung():  # put application's code here

    page_num = 1
    page_limit = 10

    if 'page' in request.args:
        page_num = int(request.args.get('page'))
    if 'limit' in request.args:
        page_limit = int(request.args.get('limit'))

    # use 'page_num' and 'page_limit' to query data

    # page_data = [
    #     {
    #         "msnv": 1234,
    #         "name": "Nguyen Van A",
    #         "birth": '24/12/1999',
    #         "phone": "0123456789",
    #         "email": "abc@gmail.com",
    #         "avatar": url_for('static', filename='img/mta.jpg'),  # base64 resource or url
    #         "address": "123 abs street, CR, NK, CT",
    #         "birth_place": "RG, KG",
    #         "id_num": "371xxxx405",  # cmnd
    #     },
    #
    # ]
    page_data, total_page = data_person(page_num, page_limit)
    paging_data = {
        'page': 1,
        'limit': 10,
        'total_page': total_page
    }
    return render_template('user-list.html', data=page_data, data_json=json.dumps(page_data), paging_data=paging_data)


@app.route('/chinhsuanguoidung', methods=['POST'])
def chinhsuanguoidung():
    data = request.form.to_dict(flat=True)
    return jsonify(data)


@app.route('/xoanguoidung/<msnv>', methods=['POST'])
def xoanguoidung(msnv):  # delete user by msnv

    status_code = 200

    sample_response = {
        "error": False,
        "message": 'Xóa thành công'
    }

    return sample_response, status_code


def gen_frames():
    while camera.isOpened():
        r, img = camera.read()
        img = cv2.resize(img, (W, H))
        img = cv2.flip(img, 1)
        img_copy = img.copy()
        # img_copy = img_copy[0:H, delta:W - delta]
        rects = detector(img)  # get face detection from Dlib
        blur = cv2.GaussianBlur(img, (15, 15), 0)
        img[mask_back == 0] = blur[mask_back == 0]
        cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, color, thickness=1)
        if len(rects) > 0:
            for rect in rects:
                faceAligned = fa.align(img, rect)  # processing face aligned
                shapes = predictor(img, rect)  # get shape point ( 68 points dlib)
                nose_x, nose_y = shapes.part(33).x, shapes.part(33).y  # get point 33 x, y
                name, probability, id_person = predict_guest(faceAligned)  # get prediction return label and probability
                if id_person != 0:
                    add_new_person_images(id_person, fa.align(img_copy, rect))
                # if check_rectangle(nose_x, nose_y, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20)):
                #     cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, (0, 255, 0), thickness=2)
                #     font_text = ImageFont.truetype(
                #         "font/simsun.ttc", 20, encoding="utf-8")
                #     img_pil = Image.fromarray(img)
                #     draw = ImageDraw.Draw(img_pil)
                #     draw.text((center_x - 100, center_y - 200), str(name), font=font_text, fill=(255, 0, 0))
                #     img = np.array(img_pil)
                # if check_rectangle(nose_x, nose_y, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20)):
                cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, (0, 255, 0), thickness=2)
                font_text = ImageFont.truetype(
                    "font/simsun.ttc", 20, encoding="utf-8")
                img_pil = Image.fromarray(img)
                draw = ImageDraw.Draw(img_pil)
                draw.text((center_x - 100, center_y - 200), str(name), font=font_text, fill=(255, 0, 0))
                img = np.array(img_pil)
        drawline(img, (center_x, center_y - 180), (center_x, center_y + 180), color)
        drawline(img, (center_x - 140, center_y), (center_x + 140, center_y), color)
        cv2.rectangle(img, (0, 0), (delta, H), color, -1)
        cv2.rectangle(img, (W - delta, 0), (W, H), color, -1)
        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # concat frame one by one and show result


def gen_frames_register():
    while camera.isOpened():
        r, img = camera.read()
        img = cv2.resize(img, (W, H))
        img = cv2.flip(img, 1)
        rects = detector(img)
        # img_copy = img.copy()
        # img_copy = img_copy[0:H, delta:W - delta]
        blur = cv2.GaussianBlur(img, (15, 15), 0)
        img[mask_back == 0] = blur[mask_back == 0]
        cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, color, thickness=1)

        if len(rects) > 0:
            # draw detect on image
            for rect in rects:
                shapes = predictor(img, rect)  # get shape point ( 68 points dlib)
                nose_x, nose_y = shapes.part(33).x, shapes.part(33).y  # get point 33 x, y
                if check_rectangle(nose_x, nose_y, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20)):
                    cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, (0, 255, 0), thickness=2)

        drawline(img, (center_x, center_y - 180), (center_x, center_y + 180), color)
        drawline(img, (center_x - 140, center_y), (center_x + 140, center_y), color)
        cv2.rectangle(img, (0, 0), (delta, H), color, -1)
        cv2.rectangle(img, (W - delta, 0), (W, H), color, -1)

        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # concat frame one by one and show result


def gen_frames_hidden():
    while camera.isOpened():
        r, img = camera.read()
        img = cv2.resize(img, (W, H))
        img = cv2.flip(img, 1)
        rects = detector(img)
        img_copy = img.copy()
        try:
            if len(rects) > 0:
                # draw detect on image
                for rect in rects:
                    img_copy = img_copy[rect.top():rect.bottom(), rect.left():rect.right()]
                    img_copy = cv2.resize(img_copy, (224, 224))
                    # img_show = Image.fromarray(img_copy)
                    # img_show.show()
            ret, buffer = cv2.imencode('.jpg', img_copy)
            img_final = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_final + b'\r\n')  # concat frame one by one and show result
        except:
            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_register')
def video_register():
    return Response(gen_frames_register(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_register_hidden')
def video_register_hidden():
    return Response(gen_frames_hidden(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/add_person_image', methods=['POST'])
def add_person_image():
    try:
        json_data_string = request.form['data']
        json_data = json.loads(json_data_string)
        image = json_data['image_base64']
        PERSON_ID_NUMBER = json_data['PERSON_ID_NUMBER']
        NAME = json_data['LAST_NAME']
        FIRST_NAME = json_data['FIRST_NAME']
        slit_name = NAME.split(' ')
        if len(slit_name) > 1:
            LAST_NAME = NAME.split(' ')[0]
            MIDDLE_NAME = NAME.split(' ')[-1]
            json_add_new_person = {
                "PERSON_ID_NUMBER": PERSON_ID_NUMBER,
                "PERSON_FIRST_NAME": FIRST_NAME,
                "PERSON_MIDLE_NAME": MIDDLE_NAME,
                "PERSON_LAST_NAME": LAST_NAME,
            }
        else:
            LAST_NAME = NAME
            json_add_new_person = {
                "PERSON_ID_NUMBER": PERSON_ID_NUMBER,
                "PERSON_FIRST_NAME": FIRST_NAME,
                "PERSON_MIDLE_NAME": None,
                "PERSON_LAST_NAME": LAST_NAME,
            }

        add_new_person(json_add_new_person)

        PERSON_ID = get_person_PERSON_ID(PERSON_ID_NUMBER)

        img_base64 = image.split(',')[-1]

        #image
        img = base64.b64decode(img_base64)
        img_save = Image.open(io.BytesIO(img)).convert("RGB")
        buffered = BytesIO()
        img_save.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        json_add_new_person_image = {
            'PERSON_ID': PERSON_ID,
            "PERSON_IMAGE_BASE64": img_str,
            'PERSON_IMAGE':img_str,
            "USED_STATUS": 1
        }
        add_new_person_image(json_add_new_person_image)

        #emb
        img = Image.open(io.BytesIO(img)).convert("RGB")
        image_arr = img.resize((224, 224))
        face_array = asarray(image_arr)
        faces = []
        faces.append(face_array)
        samples = asarray(faces, 'float32')
        samples = preprocess_input(samples, version=2)
        with graph.as_default():
            emb = model.predict(samples)[0]
        emb_byte = emb.tobytes()
        json_add_new_person_emb = {
            'PERSON_ID': PERSON_ID,
            'PERSON_EMB_NO': 1,
            "PERSON_EMB_BASE64": emb_byte,
            'PERSON_EMB':emb_byte,
            "PERSON_IMAGE_BASE64": img_str,
            'PERSON_EMB_CREATE_DATE': datetime.today().strftime("%d/%m/%Y %H:%M:%S"),
            "USED_STATUS": 1
        }
        add_new_person_emb(json_add_new_person_emb)

        return json.dumps({"error_code": 0}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        return {}, 400, {'ContentType': 'application/json'}


@app.route('/api_face_recognition', methods=['POST'])
def api_face_recognition():
    person_id = 0
    person_name = ''
    error_code = 404
    msg = " fail to call .... "
    try:
        json = request.get_json()
        # print(json)
        data = json['data']
        print(data)
        student_image = data['SEND_IMAGE']
        # print(student_image)
        str_base64 = student_image.split(',')[-1]
        str_decode_base64 = base64.b64decode(str_base64)

        # im_file = BytesIO(str_decode_base64)  # convert image to file-like object
        # img = Image.open(im_file)

        im_arr = np.frombuffer(str_decode_base64, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        img = cv2.resize(img, (W, H))
        img = cv2.flip(img, 1)
        img_copy = img.copy()
        # img_copy = img_copy[0:H, delta:W - delta]
        rects = detector(img)  # get face detection from Dlib
        blur = cv2.GaussianBlur(img, (15, 15), 0)
        img[mask_back == 0] = blur[mask_back == 0]
        cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, color, thickness=1)
        if len(rects) > 0:
            for rect in rects:
                faceAligned = fa.align(img, rect)  # processing face aligned
                # shapes = predictor(img, rect)  # get shape point ( 68 points dlib)
                # nose_x, nose_y = shapes.part(33).x, shapes.part(33).y  # get point 33 x, y
                name, probability, id_person = predict_guest(faceAligned)  # get prediction return label and probability
                person_name = name
                person_id = id_person
        #
        #         if id_person != 0:
        #             add_new_person_images(id_person, fa.align(img_copy, rect))
        #         # if check_rectangle(nose_x, nose_y, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20)):
        #         #     cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, (0, 255, 0), thickness=2)
        #         #     font_text = ImageFont.truetype(
        #         #         "font/simsun.ttc", 20, encoding="utf-8")
        #         #     img_pil = Image.fromarray(img)
        #         #     draw = ImageDraw.Draw(img_pil)
        #         #     draw.text((center_x - 100, center_y - 200), str(name), font=font_text, fill=(255, 0, 0))
        #         #     img = np.array(img_pil)
        #         # if check_rectangle(nose_x, nose_y, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20)):
        #         cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, (0, 255, 0), thickness=2)
        #         font_text = ImageFont.truetype(
        #             "font/simsun.ttc", 20, encoding="utf-8")
        #         img_pil = Image.fromarray(img)
        #         draw = ImageDraw.Draw(img_pil)
        #         draw.text((center_x - 100, center_y - 200), str(name), font=font_text, fill=(255, 0, 0))
        #         img = np.array(img_pil)
        # drawline(img, (center_x, center_y - 180), (center_x, center_y + 180), color)
        # drawline(img, (center_x - 140, center_y), (center_x + 140, center_y), color)
        # cv2.rectangle(img, (0, 0), (delta, H), color, -1)
        # cv2.rectangle(img, (W - delta, 0), (W, H), color, -1)
        # ret, buffer = cv2.imencode('.jpg', img)
        # img = buffer.tobytes()
        # error_code = 200
        # msg = 'successful !'
        # im_b64 = base64.b64encode(img)


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        error_code = 400
        msg = 'Bad Request None STUDENT_ID_NUMBER ' + str(e)
        im_b64 = ''

    return {"errorCode": error_code, "message": msg, "data": {
        'PERSON_ID': person_id,
        'PERSON_NAME': person_name,
    }}




if __name__ == '__main__':
    data_attendances_date_auto_for_day()
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

