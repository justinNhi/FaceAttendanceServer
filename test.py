# import flask
#
# from keras_vggface import VGGFace
#
# app = flask.Flask(__name__)
#
#
#
# if __name__ == "__main__":
#     print(("* Loading Keras model and Flask starting server..."
#            "please wait until server has fully started"))
#     model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
#     model.summary()
#     app.run(host="0.0.0.0", port=60006,  debug=True, use_reloader=False)

import base64
import datetime
import io
import os
import sys

import numpy as np
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

import base64
from io import BytesIO

month = 1
y = 2021

if int(month) >= 2 and int(month) <= 12:
    if len(str(int(month) - 1)) < 2:
        month_1 = '0' + str(int(month) - 1)
    else:
        month_1 = str(int(month) - 1)
    month_2 = str(int(month))
    year_1 = year
    year_2 = year
else:
    month_1 = '12'
    month_2 = '01'

start_date = datetime.datetime.strptime('26/' + month_1 + '/' + str(year), '%d/%m/%Y')
end_date = datetime.datetime.strptime('26/' + month_2 + '/' + str(year), '%d/%m/%Y')



for _date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days)):
    rs_person_images = session_sql.query(Person_Images).filter(
        Person_Images.ID_PERSON == row_person.ID_PERSON, Person_Images.DATE == _date).all()
    json_person = {}
    json_person['date'] = _date.strftime('%Y-%m-%d')
    status_1, status_2, status_3, status_4 = '', '', '', ''
    if len(rs_person_images) == 4:
        for row_person_images in rs_person_images:
            if str(getattr(row_person_images, "CHECK_SESSION")) == "1":
                status_1 = str(getattr(row_person_images, "STATUS"))
            elif str(getattr(row_person_images, "CHECK_SESSION")) == "2":
                status_2 = str(getattr(row_person_images, "STATUS"))
            elif str(getattr(row_person_images, "CHECK_SESSION")) == "3":
                status_3 = str(getattr(row_person_images, "STATUS"))
            else:
                status_4 = str(getattr(row_person_images, "STATUS"))
        if str(status_1) == str(1):
            if str(status_2) == str(2):
                json_person['sa_status'] = True
                json_person['sa_checkin'] = '7:00',
                json_person['sa_checkout'] = '11:00',
            else:
                json_person['sa_status'] = True
                json_person['sa_checkin'] = '7:00',
                json_person['sa_checkout'] = '11:00',
        else:
            json_person['sa_status'] = False
            json_person['sa_checkin'] = "0:00",
            json_person['sa_checkout'] = "0:00",

        if str(status_3) == str(3):
            if str(status_4) == str(4):
                json_person['ch_status'] = True
                json_person['ch_checkin'] = '13:00',
                json_person['ch_checkout'] = "17:00",
            else:
                json_person['ch_status'] = True
                json_person['ch_checkin'] = '13:00',
                json_person['ch_checkout'] = '17:00',
        else:
            json_person['ch_status'] = False
            json_person['ch_checkin'] = "0:00",
            json_person['ch_checkout'] = "0:00",
    else:
        json_person['sa_status'] = False
        json_person['sa_checkin'] = "0:00",
        json_person['sa_checkout'] = "0:00",

        json_person['ch_status'] = False
        json_person['ch_checkin'] = "0:00",
        json_person['ch_checkout'] = "0:00",
    person_date_data.append(json_person)
