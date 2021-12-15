import dlib
from keras_vggface import VGGFace
from methods import *
from FaceAligner import FaceAligner
from PIL import Image

mask_back = generate_mask(640, 480)
W = 640
H = 480
delta = 150
center_x = int(W / 2)
center_y = int(H / 2)
color = (255, 255, 255)
model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
model.summary()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()
fa = FaceAligner(desiredFaceWidth=150, desiredLeftEye=(0.28, 0.28))

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
    # graph = tf.get_default_graph()
    # with graph.as_default():
    #     emb = model.predict(samples)[0]
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

camera = cv2.VideoCapture(0)
while camera.isOpened():
    r, img = camera.read()
    img = cv2.resize(img, (W, H))
    img = cv2.flip(img, 1)
    # img_copy = img.copy()
    # img_copy = img_copy[0:H, delta:W - delta]
    # blur = cv2.GaussianBlur(img, (15, 15), 0)
    # img[mask_back == 0] = blur[mask_back == 0]
    cv2.ellipse(img, (center_x, center_y), (140, 180), 0, 0, 360, color, thickness=1)
    rects = detector(img)  # get face detection from Dlib
    if len(rects) > 0:
        for rect in rects:
            cv2.rectangle(img, (rect.left(), rect.top()), (rect.right(), rect.bottom()),
                          (255, 0, 0), 2)
            faceAligned = fa.align(img, rect)  # processing face aligned
            shapes = predictor(img, rect)  # get shape point ( 68 points dlib)
            nose_x, nose_y = shapes.part(33).x, shapes.part(33).y  # get point 33 x, y
            name, probability = predict_guest(model, faceAligned)  # get prediction return label and probability
            print(name, probability)
            # name, probability = '', 0 # get prediction return label and probability
            if check_rectangle(nose_x, nose_y, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20)):
                cv2.putText(img, str(name) + "-" + str(probability),
                            (center_x - 0, center_y - 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()