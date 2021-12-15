import json
import dlib
import numpy as np
from flask import Flask, render_template, Response, request, jsonify
from keras_vggface import VGGFace
# from database_model import *
from methods import *
from FaceAligner import FaceAligner
from PIL import Image, ImageFont, ImageDraw
import tensorflow as tf

app = Flask(__name__)


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
        id_person = emb_person['ID_PERSON']
        id_number_person = emb_person['ID_NUMBER_PERSON']
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

    return render_template('index.html', data_attendances_date=data_attendances_date())


@app.route('/register')
def register():  # put application's code here
    data_attendances_date_auto_for_day()
    return render_template('register.html', data_person_image=data_person_image())

@app.route('/danhsachdiemdanh')
def danhsachdiemdanh():  # put application's code here
    data_attendances_date_auto_for_day()
    return render_template('attendaces.html', data_person_images=data_attendances_date())

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
                if check_rectangle(nose_x, nose_y, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20)):
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
        print(json_data)
        image = json_data['image_base64']
        img_base64 = image.split(',')[-1]
        print(img_base64)
        img = base64.b64decode(img_base64)

        img = Image.open(io.BytesIO(img))
        img.show()
        add_new_person_image((json_data_string))

        return json.dumps({"error_code": 0}), 200, {'ContentType': 'application/json'}
    except:
        return {}, 400, {'ContentType': 'application/json'}


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
