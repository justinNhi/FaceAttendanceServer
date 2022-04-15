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

engine = create_engine("mssql+pyodbc://sa:123456@192.168.1.179:49999/face_attendance_8_11_2021?driver=SQL+Server")
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
# for base in Base.classes:
#     print(base)
SessionSql = sessionmaker()
SessionSql.configure(bind=engine)

Person = Base.classes.PERSON
Person_columns = Person.__table__.columns.keys()

Person_Image = Base.classes.PERSON_IMAGE
Person_Image_columns = Person_Image.__table__.columns.keys()

Person_EMB = Base.classes.PERSON_EMBEDDING
PERSON_EMB_columns = Person_EMB.__table__.columns.keys()

Person_Images = Base.classes.PERSON_IMAGES
Person_Images_columns = Person_Images.__table__.columns.keys()



def fill_example_data():
    session_sql = SessionSql()
    for year in [2020,2021,2022]:
        for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
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
                year_1 = year - 1
                year_2 = year

            start_date = datetime.datetime.strptime('26/' + month_1 + '/' + str(year_1), '%d/%m/%Y')
            end_date = datetime.datetime.strptime('26/' + month_2 + '/' + str(year_2), '%d/%m/%Y')


            for _date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days)):
                string_date = _date.strftime('%A')
                # print(month, year, _date, _date.strftime('%A'))
                try:
                    img = Image.open('blank.jpg').resize((50, 50))
                    # img.show()
                    im_file = BytesIO()
                    img.save(im_file, format="PNG")
                    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
                    im_b64 = base64.b64encode(im_bytes)
                    if string_date != 'Sunday':
                        if string_date != 'Saturday':
                            all_person = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
                            for row in all_person:
                                id_person = int(getattr(row, 'ID_PERSON'))
                                rs_session = session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                                                     Person_Images.DATE == _date).all()
                                if len(rs_session) == 0:
                                    json_add_1 = {
                                        'ID_PERSON': id_person,
                                        'IMAGE_PATH': im_b64,
                                        'DATE': _date,
                                        'CHECK_SESSION': 1,
                                        'STATUS': 1,
                                        'STRING_STATUS': 'Đã Check-In',
                                        'TIME': '7:00:00'
                                    }
                                    json_add_2 = {
                                        'ID_PERSON': id_person,
                                        'IMAGE_PATH': im_b64,
                                        'DATE': _date,
                                        'CHECK_SESSION': 2,
                                        'STATUS': 2,
                                        'STRING_STATUS': 'Đã Check-Out',
                                        'TIME': '11:00:00'
                                    }
                                    json_add_3 = {
                                        'ID_PERSON': id_person,
                                        'IMAGE_PATH': im_b64,
                                        'DATE': _date,
                                        'CHECK_SESSION': 3,
                                        'STATUS': 3,
                                        'STRING_STATUS': 'Đã Check-In',
                                        'TIME': '13:00:00',

                                    }
                                    json_add_4 = {
                                        'ID_PERSON': id_person,
                                        'IMAGE_PATH': im_b64,
                                        'DATE': _date,
                                        'CHECK_SESSION': 4,
                                        'STATUS': 4,
                                        'STRING_STATUS': 'Đã Check-Out',
                                        'TIME': '17:00:00'
                                    }
                                    objects = [json_add_1, json_add_2, json_add_3, json_add_4]
                                    for json_add in objects:
                                        print(json_add)
                                        obj = Person_Images(**json_add)
                                        session_sql.add(obj)
                                        session_sql.commit()
                        else:
                            all_person = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
                            for row in all_person:
                                id_person = int(getattr(row, 'ID_PERSON'))
                                rs_session = session_sql.query(Person_Images).filter(
                                    Person_Images.ID_PERSON == id_person,
                                    Person_Images.DATE == _date).all()
                                if len(rs_session) == 0:
                                    json_add_1 = {
                                        'ID_PERSON': id_person,
                                        'IMAGE_PATH': im_b64,
                                        'DATE': _date,
                                        'CHECK_SESSION': 1,
                                        'STATUS': 1,
                                        'STRING_STATUS': 'Đã Check-In',
                                        'TIME': '7:00:00'
                                    }
                                    json_add_2 = {
                                        'ID_PERSON': id_person,
                                        'IMAGE_PATH': im_b64,
                                        'DATE': _date,
                                        'CHECK_SESSION': 2,
                                        'STATUS': 2,
                                        'STRING_STATUS': 'Đã Check-Out',
                                        'TIME': '11:00:00'
                                    }
                                    objects = [json_add_1, json_add_2]
                                    for json_add in objects:
                                        print(json_add)
                                        obj = Person_Images(**json_add)
                                        session_sql.add(obj)
                                        session_sql.commit()

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(e, exc_type, fname, exc_tb.tb_lineno)
    session_sql.close()


def data_attendances_date_auto_check_for_not_attendance():
    session_sql = SessionSql()
    date = datetime.date.today()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    hour, minue, second = current_time.split(':')

    if int(hour) > 8 and int(hour) <= 10:
        all_person = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
        for row in all_person:
            id_person = int(getattr(row, 'ID_PERSON'))
            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 1).first()[0]
            print(1, time_session)
            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 1).update({'STATUS': 9,
                                                                                                  'STRING_STATUS': 'Vắng'})
                session_sql.commit()
    elif int(hour) > 11 and int(hour) <= 12:
        all_person = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
        for row in all_person:
            id_person = int(getattr(row, 'ID_PERSON'))

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 1).first()[0]
            print(2,1, time_session)

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 1).update({'STATUS': 9,
                                                                                                  'STRING_STATUS': 'Vắng'})


            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 2).first()[0]
            print(2,2, time_session)
            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 2).update({'STATUS': 10,
                                                                                                  'STRING_STATUS': 'Chưa Check Out'})
                session_sql.commit()
    elif int(hour) > 14 and int(hour) <= 16:
        all_person = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
        for row in all_person:
            id_person = int(getattr(row, 'ID_PERSON'))

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 1).first()[0]
            print(3,1, time_session)

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 1).update({'STATUS': 9,
                                                                                                  'STRING_STATUS': 'Vắng'})

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 2).first()[0]
            print(3,1, time_session)

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 2).update({'STATUS': 9,
                                                                                                  'STRING_STATUS': 'Vắng'})

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 3).first()[0]
            print(3,1, time_session)

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 3).update({'STATUS': 9,
                                                                                                  'STRING_STATUS': 'Vắng'})
                session_sql.commit()
    elif int(hour) > 17 and int(hour) <= 18:
        all_person = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
        for row in all_person:
            id_person = int(getattr(row, 'ID_PERSON'))

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 1).first()[0]
            print(3,1, time_session)

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 1).update({'STATUS': 9,
                                                                                                  'STRING_STATUS': 'Vắng'})

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 2).first()[0]
            print(4,2, time_session)

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 2).update({'STATUS': 10,
                                                                                                  'STRING_STATUS': 'Chưa Check Out'})

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 3).first()[0]
            print(4,3, time_session)

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 3).update({'STATUS': 9,
                                                                                                  'STRING_STATUS': 'Vắng'})

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 4).first()[0]
            print(4,4, time_session)

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 4).update({'STATUS': 10,
                                                                                                  'STRING_STATUS': 'Chưa Check Out'})
                session_sql.commit()
    elif int(hour) > 18:
        all_person = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
        for row in all_person:
            id_person = int(getattr(row, 'ID_PERSON'))

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 1).first()[0]

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 1).update({'STATUS': 9,
                                                                                                  'STRING_STATUS': 'Vắng'})

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 2).first()[0]

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 2).update({'STATUS': 10,
                                                                                                  'STRING_STATUS': 'Chưa Check Out'})

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 3).first()[0]

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 3).update({'STATUS': 9,
                                                                                                  'STRING_STATUS': 'Vắng'})

            time_session = session_sql.query(Person_Images.TIME).filter(Person_Images.ID_PERSON == id_person,
                                                                        Person_Images.DATE == date,
                                                                        Person_Images.CHECK_SESSION == 4).first()[0]

            if time_session is None:
                session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                        Person_Images.DATE == date,
                                                        Person_Images.CHECK_SESSION == 4).update({'STATUS': 9,
                                                                                                  'STRING_STATUS': 'Vắng'})
                session_sql.commit()


    session_sql.close()

def data_attendances_date_auto_for_day():
    session_sql = SessionSql()
    date = datetime.date.today()
    try:
        img = Image.open('blank.jpg').resize((50, 50))
        # img.show()
        im_file = BytesIO()
        img.save(im_file, format="PNG")
        im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
        im_b64 = base64.b64encode(im_bytes)



        all_person = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
        for row in all_person:
            id_person = int(getattr(row, 'ID_PERSON'))
            rs_session = session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                                 Person_Images.DATE == date).all()
            if len(rs_session) == 0:
                json_add_1 = {
                    'ID_PERSON': id_person,
                    'IMAGE_PATH': im_b64,
                    'DATE': date,
                    'CHECK_SESSION': 1,
                    'STATUS': 8,
                    'STRING_STATUS': 'Chưa xác định'
                }
                json_add_2 = {
                    'ID_PERSON': id_person,
                    'IMAGE_PATH': im_b64,
                    'DATE': date,
                    'CHECK_SESSION': 2,
                    'STATUS': 8,
                    'STRING_STATUS': 'Chưa xác định'
                }
                json_add_3 = {
                    'ID_PERSON': id_person,
                    'IMAGE_PATH': im_b64,
                    'DATE': date,
                    'CHECK_SESSION': 3,
                    'STATUS': 8,
                    'STRING_STATUS': 'Chưa xác định'
                }
                json_add_4 = {
                    'ID_PERSON': id_person,
                    'IMAGE_PATH': im_b64,
                    'DATE': date,
                    'CHECK_SESSION': 4,
                    'STATUS': 8,
                    'STRING_STATUS': 'Chưa xác định'
                }
                objects = [json_add_1, json_add_2, json_add_3, json_add_4]
                for json_add in objects:
                    print(json_add)
                    obj = Person_Images(**json_add)
                    session_sql.add(obj)
                    session_sql.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
    session_sql.close()
    data_attendances_date_auto_check_for_not_attendance()

def data_attendances_today():
    session_sql = SessionSql()
    rs_persons = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
    data = []
    # print("rs_persons", rs_persons)
    if len(rs_persons) > 0:
        for row_person in rs_persons:
            rs_person_images = session_sql.query(Person_Images).filter(
                Person_Images.ID_PERSON == row_person.ID_PERSON,
                Person_Images.DATE == datetime.datetime.today().strftime('%Y-%m-%d'),
                Person_Images.STRING_STATUS != 'Chưa xác định').all()
            # print('rs_person_images', rs_person_images)
            if len(rs_person_images) > 0:
                for row_rs_person_images in rs_person_images:
                    sample_data = {}
                    sample_data['ID_PERSON'] = str(getattr(row_person, "ID_PERSON"))
                    sample_data['ID_NUMBER_PERSON'] = getattr(row_person, "ID_NUMBER_PERSON")
                    if getattr(row_person, "MIDDLE_NAME") is not None:
                        sample_data['NAME'] = getattr(row_person, "LAST_NAME") + ' ' + \
                                              getattr(row_person, "MIDDLE_NAME") + " " + \
                                              getattr(row_person, "FIRST_NAME")
                    else:
                        sample_data['NAME'] = getattr(row_person, "LAST_NAME") + ' ' + \
                                              getattr(row_person, "FIRST_NAME")
                    sample_data['TIME'] = getattr(row_rs_person_images, 'TIME')
                    check_session = str(getattr(row_rs_person_images, 'CHECK_SESSION'))
                    if check_session == "1" or check_session == "2" :
                        sample_data['DAY_SESSION'] = 'Sáng'
                    # elif check_session == "2":
                    #     sample_data['DAY_SESSION'] = 'Sáng'
                    else:
                        sample_data['DAY_SESSION'] = 'Chiều'

                    sample_data['STRING_STATUS'] = getattr(row_rs_person_images, 'STRING_STATUS')

                    img = base64.decodebytes(getattr(row_rs_person_images, 'IMAGE_PATH'))
                    img = Image.open(io.BytesIO(img))
                    # img.show(title=getattr(person, 'ID_PERSON'))
                    img = img.resize((50, 50))
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
                    sample_data['IMAGE_SOURCE'] = img_str
                    data.append(sample_data)

    session_sql.close()
    return data

def data_attendances_date(page_num, page_size):
    session_sql = SessionSql()
    data_return_2 = []
    data_return_1 = []
    max_page = 0
    date = datetime.date.today()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    # hour, minue, second = current_time.split(':')
    # print("Current Time =", current_time, hour, minue, second)
    # if hour <= 12:
    #     day_session = 1
    # elif hour > 12 and hour <= 17 and minue <= 30:
    #     day_session = 2
    # else:
    #     day_session = 3
    try:
        max_page = (session_sql.query(Person).filter(Person.USED_STATUS == 1).count() // page_size) + 1
        # rs = session_sql.query(Person_Image).all()
        if page_num > max_page or page_num < 1:
            raise Exception("Page number is out of range")

        all_person = session_sql.query(Person).filter(Person.USED_STATUS == 1).order_by(Person.ID_PERSON).offset((page_num - 1) * page_size).limit(
            page_size).all()

        # all_person = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()

        for row_person in all_person:
            json_people_1 = {}
            json_people_2 = {}
            for col in Person_columns:
                json_people_1[col] = getattr(row_person, col)
                json_people_2[col] = getattr(row_person, col)

            rs_check_sesssion_1 = session_sql.query(Person_Images).filter(
                Person_Images.ID_PERSON == getattr(row_person, "ID_PERSON"), Person_Images.DATE == date,
                Person_Images.CHECK_SESSION == 1
            ).first()
            rs_check_sesssion_2 = session_sql.query(Person_Images).filter(
                Person_Images.ID_PERSON == getattr(row_person, "ID_PERSON"), Person_Images.DATE == date,
                Person_Images.CHECK_SESSION == 2).all()[0]
            rs_check_sesssion_3 = session_sql.query(Person_Images).filter(
                Person_Images.ID_PERSON == getattr(row_person, "ID_PERSON"), Person_Images.DATE == date,
                Person_Images.CHECK_SESSION == 3).all()[0]
            rs_check_sesssion_4 = session_sql.query(Person_Images).filter(
                Person_Images.ID_PERSON == getattr(row_person, "ID_PERSON"), Person_Images.DATE == date,
                Person_Images.CHECK_SESSION == 4).all()[0]

            json_people_1['TIME_CHECK_IN'] = getattr(rs_check_sesssion_1, 'TIME')
            json_people_1['TIME_CHECK_OUT'] = getattr(rs_check_sesssion_2, 'TIME')
            json_people_2['TIME_CHECK_IN'] = getattr(rs_check_sesssion_3, 'TIME')
            json_people_2['TIME_CHECK_OUT'] = getattr(rs_check_sesssion_4, 'TIME')

            img_check_sesssion_1 = getattr(rs_check_sesssion_1, 'IMAGE_PATH')
            img_check_sesssion_2 = getattr(rs_check_sesssion_2, 'IMAGE_PATH')
            img_check_sesssion_3 = getattr(rs_check_sesssion_3, 'IMAGE_PATH')
            img_check_sesssion_4 = getattr(rs_check_sesssion_4, 'IMAGE_PATH')

            if img_check_sesssion_1 is not None:
                img = base64.decodebytes(img_check_sesssion_1)
                img = Image.open(io.BytesIO(img))
                img = img.resize((50, 50))
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
                json_people_1['IMAGE_CHECK_IN'] =img_str
            else:
                json_people_1['IMAGE_CHECK_IN'] = img_check_sesssion_1

            if img_check_sesssion_2 is not None:
                img = base64.decodebytes(img_check_sesssion_2)
                img = Image.open(io.BytesIO(img))
                img = img.resize((50, 50))
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
                json_people_1['IMAGE_CHECK_OUT'] = img_str

            else:
                json_people_1['IMAGE_CHECK_OUT'] = img_check_sesssion_2

            if img_check_sesssion_3 is not None:
                img = base64.decodebytes(img_check_sesssion_3)
                img = Image.open(io.BytesIO(img))
                img = img.resize((50, 50))
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
                json_people_2['IMAGE_CHECK_IN'] = img_str

            else:
                json_people_2['IMAGE_CHECK_IN'] = img_check_sesssion_3

            if img_check_sesssion_4 is not None:
                img = base64.decodebytes(img_check_sesssion_4)
                img = Image.open(io.BytesIO(img))
                img = img.resize((50, 50))
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
                json_people_2['IMAGE_CHECK_OUT'] = img_str

            else:
                json_people_2['IMAGE_CHECK_OUT'] = img_check_sesssion_4


            json_people_1['STATUS_CHECK_IN'] = getattr(rs_check_sesssion_1, 'STRING_STATUS')
            json_people_1['STATUS_CHECK_OUT'] = getattr(rs_check_sesssion_2, 'STRING_STATUS')
            json_people_2['STATUS_CHECK_IN'] = getattr(rs_check_sesssion_3, 'STRING_STATUS')
            json_people_2['STATUS_CHECK_OUT'] = getattr(rs_check_sesssion_4, 'STRING_STATUS')

            data_return_1.append(json_people_1)
            data_return_2.append(json_people_2)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)

    session_sql.close()
    date = str(date).split('-')
    # print(date)
    date_return = date[2] + '/' + date[1] + '/'+ date[0]
    # print(date_return)
    return [data_return_1, data_return_2, date_return], max_page

def data_attendances_date_month_year(month, year):
    session_sql = SessionSql()

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
        year_1 = year - 1
        year_2 = year

    start_date = datetime.datetime.strptime('26/' + month_1 + '/' + str(year_1), '%d/%m/%Y')
    end_date = datetime.datetime.strptime('26/' + month_2 + '/' + str(year_2), '%d/%m/%Y')

    rs_persons = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
    sample_data = {
        "month": month,  # filter month
        "year": year,  # filter year
        "current_year": datetime.datetime.now().year,  # current system year
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
    }
    if len(rs_persons) > 0:
        data = []
        for row_person in rs_persons:
            json1_person = {}
            json1_person['id_person'] = str(getattr(row_person, "ID_PERSON"))
            json1_person['msnv'] = getattr(row_person, "ID_NUMBER_PERSON")
            if getattr(row_person, "MIDDLE_NAME") is not None:
                json1_person['name'] = getattr(row_person, "LAST_NAME") + ' ' + \
                                      getattr(row_person, "MIDDLE_NAME") + " " + \
                                      getattr(row_person, "FIRST_NAME")
            else:
                json1_person['name'] = getattr(row_person, "LAST_NAME") + ' ' + \
                                      getattr(row_person, "FIRST_NAME")


            person_date_data = []
            count_attendances = 0
            for _date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days)):
                rs_person_images = session_sql.query(Person_Images).filter(
                    Person_Images.ID_PERSON == row_person.ID_PERSON, Person_Images.DATE == _date).all()
                json_person = {}
                json_person['date'] = _date.strftime('%Y-%m-%d')
                status_1, status_2, status_3, status_4 = '', '', '', ''
                time_1, time_2, time_3, time_4 = '00:00', '00:00', '00:00', '00:00'

                if len(rs_person_images) == 4:
                    for row_person_images in rs_person_images:
                        if str(getattr(row_person_images, "CHECK_SESSION")) == "1":
                            status_1 = str(getattr(row_person_images, "STATUS"))
                            time_1 = str(getattr(row_person_images, "TIME"))
                        elif str(getattr(row_person_images, "CHECK_SESSION")) == "2":
                            status_2 = str(getattr(row_person_images, "STATUS"))
                            time_2 = str(getattr(row_person_images, "TIME"))
                        elif str(getattr(row_person_images, "CHECK_SESSION")) == "3":
                            status_3 = str(getattr(row_person_images, "STATUS"))
                            time_3 = str(getattr(row_person_images, "TIME"))
                        else:
                            status_4 = str(getattr(row_person_images, "STATUS"))
                            time_4 = str(getattr(row_person_images, "TIME"))

                    if str(status_1) == str(1):
                        if str(status_2) == str(2):
                            json_person['sa_status'] = True
                            json_person['sa_checkin'] = time_1,
                            json_person['sa_checkout'] = time_2,
                            count_attendances += 1
                        else:
                            json_person['sa_status'] = False
                            json_person['sa_checkin'] = time_1,
                            json_person['sa_checkout'] = time_2,
                    else:
                        json_person['sa_status'] = False
                        json_person['sa_checkin'] = time_1,
                        json_person['sa_checkout'] = time_2,

                    if str(status_3) == str(3):
                        if str(status_4) == str(4):
                            json_person['ch_status'] = True
                            json_person['ch_checkin'] = time_3,
                            json_person['ch_checkout'] = time_4,
                            count_attendances += 1
                        else:
                            json_person['ch_status'] = False
                            json_person['ch_checkin'] = time_3,
                            json_person['ch_checkout'] = time_4,
                    else:
                        json_person['ch_status'] = False
                        json_person['ch_checkin'] = time_3,
                        json_person['ch_checkout'] = time_4,
                elif len(rs_person_images) == 2:
                    for row_person_images in rs_person_images:
                        if str(getattr(row_person_images, "CHECK_SESSION")) == "1":
                            status_1 = str(getattr(row_person_images, "STATUS"))
                            time_1 = str(getattr(row_person_images, "TIME"))
                        elif str(getattr(row_person_images, "CHECK_SESSION")) == "2":
                            status_2 = str(getattr(row_person_images, "STATUS"))
                            time_2 = str(getattr(row_person_images, "TIME"))
                        elif str(getattr(row_person_images, "CHECK_SESSION")) == "3":
                            status_3 = str(getattr(row_person_images, "STATUS"))
                            time_3 = str(getattr(row_person_images, "TIME"))
                        else:
                            status_4 = str(getattr(row_person_images, "STATUS"))
                            time_4 = str(getattr(row_person_images, "TIME"))

                    if str(status_1) == str(1):
                        if str(status_2) == str(2):
                            json_person['sa_status'] = True
                            json_person['sa_checkin'] = time_1,
                            json_person['sa_checkout'] = time_2,
                            count_attendances += 1
                        else:
                            json_person['sa_status'] = False
                            json_person['sa_checkin'] = time_1,
                            json_person['sa_checkout'] = time_2,
                    else:
                        json_person['sa_status'] = False
                        json_person['sa_checkin'] = time_1,
                        json_person['sa_checkout'] = time_2,

                    if str(status_3) == str(3):
                        if str(status_4) == str(4):
                            json_person['ch_status'] = True
                            json_person['ch_checkin'] = time_3,
                            json_person['ch_checkout'] = time_4,
                            count_attendances += 1
                        else:
                            json_person['ch_status'] = False
                            json_person['ch_checkin'] = time_3,
                            json_person['ch_checkout'] = time_4,
                    else:
                        json_person['ch_status'] = False
                        json_person['ch_checkin'] = time_3,
                        json_person['ch_checkout'] = time_4,
                else:
                    json_person['sa_status'] = False
                    json_person['sa_checkin'] = time_1,
                    json_person['sa_checkout'] = time_2,

                    json_person['ch_status'] = False
                    json_person['ch_checkin'] = time_3,
                    json_person['ch_checkout'] = time_4,
                person_date_data.append(json_person)

            json1_person['attendances'] = person_date_data
            json1_person['count_attendances'] = count_attendances

            data.append(json1_person)
        sample_data['data'] = data
    session_sql.close()
    return sample_data

def data_attendances_personnal_date_month_year(id_person, month, year):
    session_sql = SessionSql()

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
        year_1 = year - 1
        year_2 = year

    start_date = datetime.datetime.strptime('26/' + month_1 + '/' + str(year_1), '%d/%m/%Y')
    end_date = datetime.datetime.strptime('26/' + month_2 + '/' + str(year_2), '%d/%m/%Y')

    rs_persons = session_sql.query(Person).filter(Person.USED_STATUS == 1, Person.ID_PERSON == id_person).all()
    sample_data = {
        "month": month,  # filter month
        "year": year,  # filter year
        "current_year": datetime.datetime.now().year,  # current system year
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
    }
    if len(rs_persons) > 0:
        for row_person in rs_persons:
            sample_data['id_person'] = str(getattr(row_person, "ID_PERSON"))
            sample_data['msnv'] = getattr(row_person, "ID_NUMBER_PERSON")
            if getattr(row_person, "MIDDLE_NAME") is not None:
                sample_data['name'] = getattr(row_person, "LAST_NAME") + ' ' + \
                                      getattr(row_person, "MIDDLE_NAME") + " " + \
                                      getattr(row_person, "FIRST_NAME")
            else:
                sample_data['name'] = getattr(row_person, "LAST_NAME") + ' ' + \
                                      getattr(row_person, "FIRST_NAME")


            person_date_data = []
            count_attendances = 0
            for _date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days)):
                rs_person_images = session_sql.query(Person_Images).filter(
                    Person_Images.ID_PERSON == row_person.ID_PERSON, Person_Images.DATE == _date).all()
                json_person = {}
                json_person['date'] = _date.strftime('%Y-%m-%d')
                status_1, status_2, status_3, status_4 = '', '', '', ''
                time_1, time_2, time_3, time_4 = '00:00', '00:00', '00:00', '00:00'

                if len(rs_person_images) == 4:
                    for row_person_images in rs_person_images:
                        if str(getattr(row_person_images, "CHECK_SESSION")) == "1":
                            status_1 = str(getattr(row_person_images, "STATUS"))
                            time_1 = str(getattr(row_person_images, "TIME"))
                        elif str(getattr(row_person_images, "CHECK_SESSION")) == "2":
                            status_2 = str(getattr(row_person_images, "STATUS"))
                            time_2 = str(getattr(row_person_images, "TIME"))
                        elif str(getattr(row_person_images, "CHECK_SESSION")) == "3":
                            status_3 = str(getattr(row_person_images, "STATUS"))
                            time_3 = str(getattr(row_person_images, "TIME"))
                        else:
                            status_4 = str(getattr(row_person_images, "STATUS"))
                            time_4 = str(getattr(row_person_images, "TIME"))

                    if str(status_1) == str(1):
                        if str(status_2) == str(2):
                            json_person['sa_status'] = True
                            json_person['sa_checkin'] = time_1,
                            json_person['sa_checkout'] = time_2,
                            count_attendances += 1
                        else:
                            json_person['sa_status'] = False
                            json_person['sa_checkin'] = time_1,
                            json_person['sa_checkout'] = time_2,
                    else:
                        json_person['sa_status'] = False
                        json_person['sa_checkin'] = time_1,
                        json_person['sa_checkout'] = time_2,

                    if str(status_3) == str(3):
                        if str(status_4) == str(4):
                            json_person['ch_status'] = True
                            json_person['ch_checkin'] = time_3,
                            json_person['ch_checkout'] = time_4,
                            count_attendances += 1
                        else:
                            json_person['ch_status'] = False
                            json_person['ch_checkin'] = time_3,
                            json_person['ch_checkout'] = time_4,
                    else:
                        json_person['ch_status'] = False
                        json_person['ch_checkin'] = time_3,
                        json_person['ch_checkout'] = time_4,
                elif len(rs_person_images) == 2:
                    for row_person_images in rs_person_images:
                        if str(getattr(row_person_images, "CHECK_SESSION")) == "1":
                            status_1 = str(getattr(row_person_images, "STATUS"))
                            time_1 = str(getattr(row_person_images, "TIME"))
                        elif str(getattr(row_person_images, "CHECK_SESSION")) == "2":
                            status_2 = str(getattr(row_person_images, "STATUS"))
                            time_2 = str(getattr(row_person_images, "TIME"))
                        elif str(getattr(row_person_images, "CHECK_SESSION")) == "3":
                            status_3 = str(getattr(row_person_images, "STATUS"))
                            time_3 = str(getattr(row_person_images, "TIME"))
                        else:
                            status_4 = str(getattr(row_person_images, "STATUS"))
                            time_4 = str(getattr(row_person_images, "TIME"))

                    if str(status_1) == str(1):
                        if str(status_2) == str(2):
                            json_person['sa_status'] = True
                            json_person['sa_checkin'] = time_1,
                            json_person['sa_checkout'] = time_2,
                            count_attendances += 1
                        else:
                            json_person['sa_status'] = False
                            json_person['sa_checkin'] = time_1,
                            json_person['sa_checkout'] = time_2,
                    else:
                        json_person['sa_status'] = False
                        json_person['sa_checkin'] = time_1,
                        json_person['sa_checkout'] = time_2,

                    if str(status_3) == str(3):
                        if str(status_4) == str(4):
                            json_person['ch_status'] = True
                            json_person['ch_checkin'] = time_3,
                            json_person['ch_checkout'] = time_4,
                            count_attendances += 1
                        else:
                            json_person['ch_status'] = False
                            json_person['ch_checkin'] = time_3,
                            json_person['ch_checkout'] = time_4,
                    else:
                        json_person['ch_status'] = False
                        json_person['ch_checkin'] = time_3,
                        json_person['ch_checkout'] = time_4,
                else:
                    json_person['sa_status'] = False
                    json_person['sa_checkin'] = time_1,
                    json_person['sa_checkout'] = time_2,

                    json_person['ch_status'] = False
                    json_person['ch_checkin'] = time_3,
                    json_person['ch_checkout'] = time_4,
                person_date_data.append(json_person)

            sample_data['attendances'] = person_date_data
            sample_data['count_attendances'] = count_attendances

    session_sql.close()
    return sample_data


def get_default_attendances_tab():
    DEFAULT_SA_END = 11
    DEFAULT_CH_END = 17

    now = datetime.datetime.now()
    today_sa_end = now.replace(hour=DEFAULT_SA_END, minute=0, second=0, microsecond=0)
    today_ch_end = now.replace(hour=DEFAULT_CH_END, minute=0, second=0, microsecond=0)

    if now < today_ch_end:
        return 'sa'
    else:
        return 'ch'

def get_max_id_number(object, cols, id_name):
    session_sql = SessionSql()
    rs = session_sql.query(object).all()
    session_sql.close()
    max_id = 0
    for row in rs:
        for col in cols:
            if str(col) == str(id_name):
                id_col = int(getattr(row, col))
                if id_col >= max_id:
                    max_id = id_col

    return max_id + 1


#
# id_max = get_max_id_number(Person, Person_columns, "ID_PERSON")
#
# print(id_max)

# add new Person

def add_new_person(json_add):
    json_add['ID_PERSON'] = get_max_id_number(Person, Person_columns, 'ID_PERSON')
    json_add['USED_STATUS'] = 1
    session_sql = SessionSql()
    try:
        obj = Person(**json_add)
        session_sql.add(obj)
        session_sql.commit()
        session_sql.close()
        print(json_add)
        return 1
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        session_sql.close()
        return 0

def get_person_id_person(ID_NUMBER_PERSON):
    session_sql = SessionSql()
    ID_PERSON = session_sql.query(Person.ID_PERSON).filter(Person.ID_NUMBER_PERSON==ID_NUMBER_PERSON).first()
    if ID_PERSON is not None:
        ID_PERSON = ID_PERSON[0]
    else:
        ID_PERSON = 0
    session_sql.close()
    return ID_PERSON



def add_new_person_image(json_add):
    session_sql = SessionSql()
    try:
        obj = Person_Image(**json_add)
        session_sql.add(obj)
        session_sql.commit()
        session_sql.close()
        print(json_add)
        return 1
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        session_sql.close()
        return 0


def add_new_person_emb(json_add):
    session_sql = SessionSql()
    try:
        obj = Person_EMB(**json_add)
        session_sql.add(obj)
        session_sql.commit()
        session_sql.close()
        print(json_add)
        return 1
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        session_sql.close()
        return 0


def delete_person(id_person):
    session_sql = SessionSql()
    try:
        session_sql.query(Person).filter(Person.ID_PERSON == id_person).delete()
        session_sql.commit()
        session_sql.close()
        return 1
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        session_sql.close()
        return 0


def data_person_image(page_num, page_size):
    session_sql = SessionSql()
    array_data = []
    max_page = 0
    try:
        rs = session_sql.query(Person_Image).filter(Person_Image.ID_PERSON == Person.ID_PERSON, Person.USED_STATUS == 1).all()
        max_page = (len(rs) // page_size) + 1
        # rs = session_sql.query(Person_Image).all()
        if page_num > max_page or page_num < 1:
            raise Exception("Page number is out of range")

        rs  = session_sql.query(Person_Image, Person).filter(Person_Image.ID_PERSON == Person.ID_PERSON, Person.USED_STATUS == 1).order_by(Person_Image.ID_PERSON).offset((page_num-1)*page_size).limit(page_size).all()
        for row, person in rs:
            person = session_sql.query(Person).filter(Person.ID_PERSON == int(getattr(row, 'ID_PERSON'))).first()
            img = base64.decodebytes(getattr(row, 'PERSON_IMG'))
            img = Image.open(io.BytesIO(img))
            # img.show(title=getattr(person, 'ID_PERSON'))
            img = img.resize((50,50))
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
            json_row = {
                'ID_PERSON': getattr(person, 'ID_PERSON'),
                'ID_NUMBER_PERSON': getattr(person, 'ID_NUMBER_PERSON'),
                'LAST_NAME': getattr(person, 'LAST_NAME'),
                'MIDDLE_NAME': getattr(person, 'MIDDLE_NAME'),
                'FIRST_NAME': getattr(person, 'FIRST_NAME'),
                'ADDRESS': getattr(person, 'ADDRESS'),
                'IMAGE_SOURCE':img_str
            }
            for col in Person_Image_columns:
                json_row[col] = getattr(row, col)
            array_data.append(json_row)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
    session_sql.close()
    return array_data, max_page

def data_person(page_num, page_size):
    session_sql = SessionSql()
    array_data = []
    max_page = 0
    try:
        rs = session_sql.query(Person_Image).filter(Person_Image.ID_PERSON == Person.ID_PERSON, Person.USED_STATUS == 1).all()
        max_page = (len(rs) // page_size) + 1
        # rs = session_sql.query(Person_Image).all()
        if page_num > max_page or page_num < 1:
            raise Exception("Page number is out of range")

        rs  = session_sql.query(Person_Image, Person).filter(Person_Image.ID_PERSON == Person.ID_PERSON, Person.USED_STATUS == 1).order_by(Person_Image.ID_PERSON).offset((page_num-1)*page_size).limit(page_size).all()
        for row, person in rs:
            # person = session_sql.query(Person).filter(Person.ID_PERSON == int(getattr(row, 'ID_PERSON'))).first()
            img = base64.decodebytes(getattr(row, 'PERSON_IMG'))
            img = Image.open(io.BytesIO(img))
            # img.show(title=getattr(person, 'ID_PERSON'))
            img = img.resize((50,50))
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
            if getattr(person, 'MIDDLE_NAME') is None:
                person_name = getattr(person, 'LAST_NAME') + ' ' +getattr(person, 'FIRST_NAME')
            else:
                person_name = getattr(person, 'LAST_NAME') + ' ' + getattr(person, 'MIDDLE_NAME') + ' ' + getattr(person, 'FIRST_NAME')

            json_row = {
                'ID_PERSON': int(getattr(person, 'ID_PERSON')),
                'msnv': str(getattr(person, 'ID_NUMBER_PERSON')),
                'name': person_name,
                "birth" : getattr(person, 'DATE_OF_BIRTH'),
                "phone": getattr(person, 'PHONE_NUMBER'),
                "email": getattr(person, 'EMAIL'),
                "avatar": img_str,  # base64 resource or url
                "address": getattr(person, 'ADDRESS'),
                "birth_place": getattr(person, 'PLACE_OF_BIRTH'),
                "id_num": getattr(person, 'ID_NUMBER'),
                'used_status': str(getattr(person, 'USED_STATUS'))
            }
            # for col in Person_Image_columns:
            #     json_row[col] = getattr(row, col

            array_data.append(json_row)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
    session_sql.close()
    return array_data, max_page

def data_person_label_embedding():
    session_sql = SessionSql()
    all_persons = session_sql.query(Person, Person_EMB).filter(Person.USED_STATUS == 1,
        Person.ID_PERSON == Person_EMB.ID_PERSON).all()
    array_return = []
    for row in all_persons:
        row_person = row[0]
        row_person_emb = row[1]
        if getattr(row_person, 'MIDDLE_NAME') == '' or getattr(row_person, 'MIDDLE_NAME') is None:
            full_name = getattr(row_person, 'LAST_NAME') + ' ' + getattr(row_person, 'FIRST_NAME')
        else:
            full_name = getattr(row_person, 'LAST_NAME') + ' ' + getattr(row_person, 'MIDDLE_NAME') + ' ' + getattr(
                row_person, 'FIRST_NAME')

        json_return = {
            'ID_PERSON': getattr(row_person, 'ID_PERSON'),
            'ID_NUMBER_PERSON': getattr(row_person, 'ID_NUMBER_PERSON'),
            'FULL_NAME': full_name,
            'PERSON_EMB': np.frombuffer(getattr(row_person_emb, 'PERSON_EMB'), dtype="float32")
        }
        array_return.append(json_return)
    session_sql.close()
    return array_return


def add_new_person_images(id_person, img):
    session_sql = SessionSql()
    date = datetime.date.today()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    hour, minue, second = current_time.split(':')
    hour = int(hour)
    if hour >= 7 and hour <= 10:
        check_session = 1
        status = 1
        status_string = 'Đã Check-In'
    elif hour > 10 and hour <= 12:
        check_session = 2
        status = 2
        status_string = 'Đã Check-Out'
    elif hour > 12 and hour <= 16:
        check_session = 3
        status = 3
        status_string = 'Đã Check-In'
    elif hour > 16 and hour <= 18:
        check_session = 4
        status = 4
        status_string = 'Đã Check-Out'
    else:
        check_session = 5
        status = 7
        status_string = 'Ngoài giờ'

    try:
        if len(session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                     Person_Images.DATE == date,
                                                     Person_Images.CHECK_SESSION == check_session,
                                                        Person_Images.STRING_STATUS == 'Chưa xác định').all()) == 1:

            img = Image.fromarray(img).resize((50, 50))
            # img.show()
            im_file = BytesIO()
            img.save(im_file, format="PNG")
            im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
            im_b64 = base64.b64encode(im_bytes)

            # img_numpy = np.asarray(img_load)
            # image_64_encode = base64.encodebytes(img_numpy)

            rs = session_sql.query(Person_Images).filter(Person_Images.ID_PERSON == id_person,
                                                         Person_Images.DATE == date,
                                                         Person_Images.CHECK_SESSION == check_session).update({
                'TIME': current_time,
                'IMAGE_PATH': im_b64,
                'CHECK_SESSION': check_session,
                'STATUS': status,
                'STRING_STATUS': status_string

            })
            if rs == 1:
                session_sql.commit()
            session_sql.close()
            return 1
        else:

            session_sql.close()
            return 1
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        session_sql.close()
        return 0


if __name__ == '__main__':
    pass
    # fill_example_data()
    # data_attendances_date_month_year(1, 2021)

    # get_person_id_person("212121")
    # a = data_attendances_date_auto_for_day()
    # b = data_attendances_date_auto_check_for_not_attendance()
    #
    # b = data_attendances_date()
    # c, d = b
    # print(c)
    # print(d)

    # pass
    # A = data_person_label_embedding()
    # # # for a in A:
    # # #     print(a)
    # #
    # for emb_person in A:
    #     id_person = emb_person['ID_PERSON']
    #     id_number_person = emb_person['ID_NUMBER_PERSON']
    #     person_emb = emb_person['PERSON_EMB']
    #     print(person_emb.shape)
    #     print(id_person, id_number_person, person_
