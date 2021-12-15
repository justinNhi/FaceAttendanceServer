import base64
from scipy.spatial.distance import cosine
import PIL
import cv2
import numpy as np
import requests as requests
from PIL import Image
from numpy import asarray
from keras_vggface.utils import preprocess_input
from database_model import *
import tensorflow as tf

def predict_guest(model, image):
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
    graph = tf.get_default_graph()
    with graph.as_default():
        emb = model.predict(samples)[0]
    label = ''
    probability = 0
    embs = data_person_label_embedding()
    for emb_person in embs:
        id_person = emb_person['ID_PERSON']
        id_number_person = emb_person['ID_NUMBER_PERSON']
        person_emb = emb_person['PERSON_EMB']
        score = cosine(emb, person_emb)
        score = round(score, 2)
        if score < 0.3:
            ind = id_person
            label = str(id_number_person)
            probability = score
            break
        else:
            ind = id_person
            label = str("Unknow")
            probability = score

    return label, probability


def get_predict(img, method, url, n= 0):
    _, im_arr = cv2.imencode('.jpg', img)  # encoding image
    im_bytes = im_arr.tobytes()  # convert to bytes
    im_b64 = str(base64.b64encode(im_bytes))  # convert byte to encode base64

    im_b64 = im_b64[1:]  # cut char "b" in string
    payload = {"image": im_b64, "n": n, "method": method}  # create json
    # print(payload)

    # Submit the request
    r = requests.post(url, json=payload, timeout=200).json()

    return r

def check_circle(x, y, center_x, center_y, radius):
    dx = abs(x - center_x)
    dy = abs(y - center_y)
    if dx ** 2 + dy ** 2 <= radius ** 2:
        return True
    else:
        return False


def check_ellipse(x, y, center_x, center_y, rx, ry):
    dx = abs(x - center_x)
    dy = abs(y - center_y)
    region = (dx ** 2) / (rx ** 2) + (dy ** 2) / (ry ** 2)
    if region <= 1:
        return True
    else:
        return False


def generate_mask(w, h):
    mask = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            # check = check_circle(j, i, int(w/2), int(h/2), 120)
            check = check_ellipse(j, i, int(w / 2), int(h / 2), 140, 180)
            if check:
                mask[i, j] = 1
    return mask


def drawline(img, pt1, pt2, color, thickness=1, gap=20):
    dist = ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** .5
    pts = []
    for i in np.arange(0, dist, gap):
        r = i / dist
        x = int((pt1[0] * (1 - r) + pt2[0] * r) + .5)
        y = int((pt1[1] * (1 - r) + pt2[1] * r) + .5)
        p = (x, y)
        pts.append(p)

    for p in pts:
        cv2.circle(img, p, thickness, color, -1)


def check_rectangle(x, y, pt1, pt2):
    if (pt1[0] <= x <= pt2[0]) and (pt1[1] <= y <= pt2[1]):
        return True
    else:
        return False


def gen_frames(camera, W, H, delta, mask_back, center_x, center_y, color, model, detector, fa, predictor):
    while camera.isOpened():
        r, img = camera.read()
        img = cv2.resize(img, (W, H))
        img = cv2.flip(img, 1)
        # img_copy = img.copy()
        # img_copy = img_copy[0:H, delta:W - delta]
        # blur = cv2.GaussianBlur(img, (15, 15), 0)
        # img[mask_back == 0] = blur[mask_back == 0]
        # cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, color, thickness=1)
        rects = detector(img)  # get face detection from Dlib
        if len(rects) > 0:
            for rect in rects:
                faceAligned = fa.align(img, rect) # processing face aligned
                shapes = predictor(img, rect) # get shape point ( 68 points dlib)
                nose_x, nose_y = shapes.part(33).x, shapes.part(33).y  # get point 33 x, y
                name, probability = predict_guest(model, faceAligned) # get prediction return label and probability
                if check_rectangle(nose_x, nose_y, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20)):
                    cv2.putText(img, str(name) + "-" + str(probability),
                                (center_x - 0, center_y - 180),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1, cv2.LINE_AA)

        # if r["success"]:
        #     # draw detect on image
        #     for (i, result) in enumerate(r["predictions"]):
        #         # cv2.rectangle(img, (result["left"], result["top"]), (result["right"], result["bottom"]),
        #         #               (255, 0, 0), 2)
        #         nose_x = result['nose_x']
        #         nose_y = result['nose_y']
        #         if check_rectangle(nose_x, nose_y, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20)):
        #             cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, (0, 255, 0), thickness=2)
        #             cv2.putText(img, str(result["name"]) + "-" + str(result["probability"]),
        #                         (center_x - 0, center_y - 180),
        #                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1, cv2.LINE_AA)
        # drawline(img, (center_x, center_y - 180), (center_x, center_y + 180), color)
        # drawline(img, (center_x - 140, center_y), (center_x + 140, center_y), color)
        # cv2.rectangle(img, (0, 0), (delta, H), color, -1)
        # cv2.rectangle(img, (W-delta, 0), (W, H), color, -1)

        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # concat frame one by one and show result

def gen_frames_register(camera, W, H, delta, mask_back, center_x, center_y, color, url):
    while camera.isOpened():
        r, img = camera.read()
        img = cv2.resize(img, (W, H))
        img = cv2.flip(img, 1)
        img_copy = img.copy()
        img_copy = img_copy[0:H, delta:W - delta]
        blur = cv2.GaussianBlur(img, (15, 15), 0)
        img[mask_back == 0] = blur[mask_back == 0]

        cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, color, thickness=1)

        r = get_predict(img, url)
        if r["success"]:
            # draw detect on image
            for (i, result) in enumerate(r["predictions"]):
                # cv2.rectangle(img, (result["left"], result["top"]), (result["right"], result["bottom"]),
                #               (255, 0, 0), 2)
                nose_x = result['nose_x']
                nose_y = result['nose_y']
                if check_rectangle(nose_x, nose_y, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20)):
                    cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, (0, 255, 0), thickness=2)
                    # cv2.putText(img, str(result["name"]) + "-" + str(result["probability"]),
                    #             (center_x - 0, center_y - 180),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1, cv2.LINE_AA)
                    #
        drawline(img, (center_x, center_y - 180), (center_x, center_y + 180), color)
        drawline(img, (center_x - 140, center_y), (center_x + 140, center_y), color)
        cv2.rectangle(img, (0, 0), (delta, H), color, -1)
        cv2.rectangle(img, (W-delta, 0), (W, H), color, -1)

        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # concat frame one by one and show result

def gen_frames_hidden(camera, W, H, delta, mask_back, center_x, center_y, color,url):
    while camera.isOpened():
        r, img = camera.read()
        img = cv2.resize(img, (W, H))
        img = cv2.flip(img, 1)
        img_copy = img.copy()
        try:
            r = get_predict(img, url)
            if r["success"]:
                # draw detect on image
                for (i, result) in enumerate(r["predictions"]):
                    img_copy = img_copy[result["top"]:result["bottom"], result["left"]:result["right"]]
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