import flask

from keras_vggface import VGGFace

app = flask.Flask(__name__)



if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
    model.summary()
    app.run(host="0.0.0.0", port=60006,  debug=True, use_reloader=False)
