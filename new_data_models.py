import base64
import datetime
import io
import os
import random
import sys

import numpy as np
from PIL import Image
from sqlalchemy import create_engine, func, desc
from sqlalchemy.ext.automap import automap_base

# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

import base64
from io import BytesIO

# engine = create_engine("mssql+pyodbc://sa:123456@192.168.1.179:49999/face_attendance_8_11_2021?driver=SQL+Server")
# engine = create_engine("mssql+pyodbc://sa:nhi874755@192.168.1.179/OFFICE_ATTENDANCE?driver=SQL+Server", echo=True)
engine = create_engine("mssql+pyodbc://sa:nhi874755@192.168.1.179/OFFICE_ATTENDANCE?driver=SQL+Server")

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

# Person_Attendance = Base.classes.PERSON_ATTENDANCE
# Person_Attendance_columns = Person_Attendance.__table__.columns.keys()

# Person_Session_1 = Base.classes.PERSON_SESSION_1
# Person_Session_1_columns = Person_Session_1.__table__.columns.keys()
#
# Person_Session_2 = Base.classes.PERSON_SESSION_2
# Person_Session_2_columns = Person_Session_2.__table__.columns.keys()
#
# Person_Session_3 = Base.classes.PERSON_SESSION_3
# Person_Session_3_columns = Person_Session_3.__table__.columns.keys()

# Person_Check_In = Base.classes.PERSON_CHECK_IN
# Person_Check_In_columns = Person_Check_In.__table__.columns.keys()
#
# Person_Check_Out = Base.classes.PERSON_CHECK_OUT
# Person_Check_Out_columns = Person_Check_Out.__table__.columns.keys()

Person_Check = Base.classes.PERSON_CHECK
Person_Check_columns = Person_Check.__table__.columns.keys()

from datetime import date, timedelta, datetime


# graph = tf.get_default_graph()
# model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
#
# mask_back = generate_mask(640, 480)
# W = 640
# H = 480
# delta = 150
# center_x = int(W / 2)
# center_y = int(H / 2)
# color = (255, 255, 255)
# camera = cv2.VideoCapture(0)
# predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# detector = dlib.get_frontal_face_detector()
# fa = FaceAligner(desiredFaceWidth=150, desiredLeftEye=(0.28, 0.28))

# def get_check_in(date_insert):
# #     session_sql = SessionSql()
# #     array_return = []
# #     try:
# #         rs = session_sql.query(Person, Person_Check_In).filter(
# #             Person_Check_In.PERSON_ID == Person.PERSON_ID,
# #             Person.USED_STATUS == 1,
# #             Person_Check_In.DATE == date_insert
# #         ).order_by(desc(Person_Check_In.TIME))
# #         print(rs)
# #         rs = rs.all()
# #         if len(rs) > 0:
# #             for person, person_check_in in rs:
# #                 json_return = {}
# #                 json_return['PERSON_ID_NUMBER'] = getattr(person, 'PERSON_ID_NUMBER')
# #                 json_return['PERSON_FULL_NAME'] = get_full_name(
# #                     getattr(person, 'PERSON_LAST_NAME'),
# #                     getattr(person, 'PERSON_MIDDLE_NAME'),
# #                     getattr(person, 'PERSON_FIRST_NAME')
# #                 )
# #                 json_return['TIME'] = getattr(person_check_in, 'TIME').strftime("%H:%M:%S")
# #                 json_return['SESSION_NAME'] = getattr(person_check_in, 'SESSION_NAME')
# #                 json_return['SESSION_NAME_EN'] = getattr(person_check_in, 'SESSION_NAME_EN')
# #                 json_return['SESSION_STATUS_NAME'] = getattr(person_check_in, 'SESSION_STATUS_NAME')
# #                 json_return['SESSION_STATUS_NAME_EN'] = getattr(person_check_in, 'SESSION_STATUS_NAME_EN')
# #                 json_return['SESSION_IMAGE_BASE64'] = getattr(person_check_in, 'SESSION_IMAGE_BASE64').decode("utf-8")
# #
# #                 array_return.append(json_return)
# #
# #     except Exception as e:
# #         exc_type, exc_obj, exc_tb = sys.exc_info()
# #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
# #         print(e, exc_type, fname, exc_tb.tb_lineno)
# #
# #     session_sql.close()
# #
# #     return array_return
#
#
# def get_check_out(date_insert):
#     session_sql = SessionSql()
#     array_return = []
#     try:
#         rs = session_sql.query(Person, Person_Check_Out).filter(
#             Person_Check_Out.PERSON_ID == Person.PERSON_ID,
#             Person.USED_STATUS == 1,
#             Person_Check_Out.DATE == date_insert
#         ).order_by(desc(Person_Check_Out.TIME)).all()
#         if len(rs) > 0:
#             for person, person_check_out in rs:
#                 json_return = {}
#                 json_return['PERSON_ID_NUMBER'] = getattr(person, 'PERSON_ID_NUMBER')
#                 json_return['PERSON_FULL_NAME'] = get_full_name(
#                     getattr(person, 'PERSON_LAST_NAME'),
#                     getattr(person, 'PERSON_MIDDLE_NAME'),
#                     getattr(person, 'PERSON_FIRST_NAME')
#                 )
#                 json_return['TIME'] = getattr(person_check_out, 'TIME').strftime("%H:%M:%S")
#                 json_return['SESSION_NAME'] = getattr(person_check_out, 'SESSION_NAME')
#                 json_return['SESSION_NAME_EN'] = getattr(person_check_out, 'SESSION_NAME_EN')
#                 json_return['SESSION_STATUS_NAME'] = getattr(person_check_out, 'SESSION_STATUS_NAME')
#                 json_return['SESSION_STATUS_NAME_EN'] = getattr(person_check_out, 'SESSION_STATUS_NAME_EN')
#                 json_return['SESSION_IMAGE_BASE64'] = getattr(person_check_out, 'SESSION_IMAGE_BASE64').decode("utf-8")
#
#                 array_return.append(json_return)
#
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(e, exc_type, fname, exc_tb.tb_lineno)
#
#     session_sql.close()
#
#     return array_return
#
#
# def insert_check_in(person_id, image_base64):
#     error_code = 400
#     session_sql = SessionSql()
#     array_return = []
#     try:
#         morning_time = datetime.now().replace(hour=6, minute=0, second=0).strftime("%H:%M:%S")
#         afternoon_time = datetime.now().replace(hour=11, minute=0, second=0).strftime("%H:%M:%S")
#         evening_time = datetime.now().replace(hour=17, minute=0, second=0).strftime("%H:%M:%S")
#         time_now = datetime.now().strftime("%H:%M:%S")
#         if time_now >= morning_time and time_now <= afternoon_time:
#             session_id = 1
#             session_name = 'Buổi Sáng'
#             session_name_en = "Morning Shift"
#         elif time_now > afternoon_time and time_now <= evening_time:
#             session_id = 2
#             session_name = 'Buổi Chiều'
#             session_name_en = "Afternoon Shift"
#         # elif time_now > evening_time:
#         else:
#             session_id = 3
#             session_name = 'Buổi Tối'
#             session_name_en = "Evening Shift"
#         # date_insert = datetime.today().strftime('%d/%m/%Y')
#         time_insert = datetime.now().strftime("%H:%M:%S")
#         date_insert = date.today().strftime('%Y-%m-%d')
#         # time_insert = datetime.now()
#
#         rs_check = session_sql.query(Person_Check_In).filter(
#             Person_Check_In.PERSON_ID == person_id,
#             Person_Check_In.DATE == date_insert,
#             Person_Check_In.SESSION_ID == session_id).all()
#         if len(rs_check) == 0:
#             if person_id is not None and int(person_id) > 0:
#                 try:
#                     json_insert = {
#                         "PERSON_ID": person_id,
#                         "DATE": date_insert,
#                         "TIME": time_insert,
#                         "SESSION_ID": session_id,
#                         "SESSION_NAME": session_name,
#                         "SESSION_NAME_EN": session_name_en,
#                         "SESSION_STATUS_NAME": 'Đã điểm danh',
#                         "SESSION_STATUS_NAME_EN": 'Attend',
#                         "SESSION_IMAGE_BASE64": image_base64,
#                         "USED_STATUS": 1,
#                         "USED_STATUS_NAME": "In Use",
#                     }
#                     session_sql.add(Person_Check_In(**json_insert))
#                     session_sql.commit()
#                     error_code = 200
#                     array_return = get_check_in(date_insert)
#                 except:
#                     error_code = 201
#                 print('Kiem tra try ex', error_code, array_return)
#
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(e, exc_type, fname, exc_tb.tb_lineno)
#
#     session_sql.close()
#
#     return error_code, array_return
#
#
# def insert_check_out(person_id, image_base64):
#     error_code = 400
#     session_sql = SessionSql()
#     array_return = []
#     try:
#         morning_time = datetime.now().replace(hour=7, minute=0, second=0).strftime("%H:%M:%S")
#         afternoon_time = datetime.now().replace(hour=13, minute=0, second=0).strftime("%H:%M:%S")
#         evening_time = datetime.now().replace(hour=18, minute=0, second=0).strftime("%H:%M:%S")
#         time_now = datetime.now().strftime("%H:%M:%S")
#         date_insert = datetime.today().strftime('%Y-%m-%d')
#         # time_now = datetime.now()
#         # date_insert = date.today()
#
#         if time_now >= morning_time and time_now <= afternoon_time:
#             session_id = 1
#             session_name = 'Buổi Sáng'
#             session_name_en = "Morning Shift"
#         elif time_now > afternoon_time and time_now <= evening_time:
#             session_id = 2
#             session_name = 'Buổi Chiều'
#             session_name_en = "Afternoon Shift"
#         # elif time_now > evening_time:
#         else:
#             session_id = 3
#             session_name = 'Buổi Tối'
#             session_name_en = "Evening Shift"
#
#         rs_check = session_sql.query(Person_Check_Out).filter(
#             Person_Check_Out.PERSON_ID == person_id,
#             Person_Check_Out.DATE == date_insert,
#             Person_Check_Out.SESSION_ID == session_id).all()
#         if len(rs_check) == 0:
#             if person_id is not None and int(person_id) > 0:
#                 try:
#                     json_insert = {
#                         "PERSON_ID": person_id,
#                         "DATE": date_insert,
#                         "TIME": datetime.now().strftime("%H:%M:%S"),
#                         "SESSION_ID": session_id,
#                         "SESSION_NAME": session_name,
#                         "SESSION_NAME_EN": session_name_en,
#                         "SESSION_STATUS_NAME": 'Đã hoàn thành buổi làm',
#                         "SESSION_STATUS_NAME_EN": 'Done a Shift',
#                         "SESSION_IMAGE_BASE64": image_base64,
#                         "USED_STATUS": 1,
#                         "USED_STATUS_NAME": "In Use",
#                     }
#                     session_sql.add(Person_Check_Out(**json_insert))
#                     error_code = 200
#                     session_sql.commit()
#                     array_return = get_check_out(date_insert)
#                 except:
#                     error_code = 201
#
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(e, exc_type, fname, exc_tb.tb_lineno)
#
#     session_sql.close()
#     return error_code, array_return
#
#
# def get_json_person_check_in(person_id, date, session_process=1):
#     # 1 check in morning
#     # 2 check in afternoon
#     # 3 check in evening
#     session_sql = SessionSql()
#     json_return = {}
#     try:
#         if person_id is not None and date is not None:
#             date = datetime.datetime.strptime(date, '%d/%m/%Y')
#             if int(session_process) == 1:
#                 results_of_check = session_sql.query(Person_Check_In).filter(
#                     Person_Check_In.PERSON_ID == person_id,
#                     Person_Check_In.DATE == date,
#                     Person_Check_In.USED_STATUS == 1
#                 ).all()
#                 if results_of_check is not None and len(results_of_check) > 0:
#                     json_return['SESSION_NAME'] = getattr(results_of_check, 'SESSION_NAME')
#                     json_return['SESSION_NAME_EN'] = getattr(results_of_check, 'SESSION_NAME_EN')
#                     json_return['SESSION_STATUS_NAME'] = getattr(results_of_check, 'SESSION_STATUS_NAME')
#                     json_return['SESSION_STATUS_NAME_EN'] = getattr(results_of_check, 'SESSION_STATUS_NAME_EN')
#                     json_return['SESSION_IMAGE_BASE64'] = getattr(results_of_check, 'SESSION_IMAGE_BASE64')
#                     json_return['USED_STATUS_NAME'] = getattr(results_of_check, 'USED_STATUS_NAME')
#                 else:
#                     pass
#         else:
#             pass
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(e, exc_type, fname, exc_tb.tb_lineno)
#     session_sql.close()
#     return json_return
#
#
# def get_json_person_check_out(person_id, date, session_process=1):
#     # 1 check in morning
#     # 2 check in afternoon
#     # 3 check in evening
#     session_sql = SessionSql()
#     json_return = {}
#     try:
#         if person_id is not None and date is not None:
#             date = datetime.datetime.strptime(date, '%d/%m/%Y')
#             if int(session_process) == 1:
#                 results_of_check = session_sql.query(Person_Check_Out).filter(
#                     Person_Check_Out.PERSON_ID == person_id,
#                     Person_Check_Out.DATE == date,
#                     Person_Check_Out.USED_STATUS == 1
#                 ).all()
#                 if results_of_check is not None and len(results_of_check) > 0:
#                     json_return['SESSION_NAME'] = getattr(results_of_check, 'SESSION_NAME')
#                     json_return['SESSION_NAME_EN'] = getattr(results_of_check, 'SESSION_NAME_EN')
#                     json_return['SESSION_STATUS_NAME'] = getattr(results_of_check, 'SESSION_STATUS_NAME')
#                     json_return['SESSION_STATUS_NAME_EN'] = getattr(results_of_check, 'SESSION_STATUS_NAME_EN')
#                     json_return['SESSION_IMAGE_BASE64'] = getattr(results_of_check, 'SESSION_IMAGE_BASE64')
#                     json_return['USED_STATUS_NAME'] = getattr(results_of_check, 'USED_STATUS_NAME')
#                 else:
#                     pass
#         else:
#             pass
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(e, exc_type, fname, exc_tb.tb_lineno)
#     session_sql.close()
#     return json_return


# def get_json_all_check_in():
#     # 1 check in morning
#     # 2 check in afternoon
#     # 3 check in evening
#     session_sql = SessionSql()
#     array_return = []
#     try:
#         date = datetime.datetime.today().strftime('%Y-%d-%m')
#         results_of_check = session_sql.query(Person_Check_In).filter(
#             # Person_Check_In.PERSON_ID == person_id,
#             Person_Check_In.DATE == date,
#             Person_Check_In.USED_STATUS == 1
#         ).all()
#         if results_of_check is not None and len(results_of_check) > 0:
#             for row in results_of_check:
#                 json_return = {}
#
#                 rs_person = session_sql.query(Person).filter(Person.PERSON_ID == getattr(row, 'PERSON_ID')).first()
#                 json_return['PERSON_ID'] = int(getattr(rs_person, 'PERSON_ID'))
#                 json_return['PERSON_ID_NUMBER'] = getattr(rs_person, 'PERSON_ID_NUMBER')
#                 json_return['PERSON_FULL_NAME'] = get_full_name(
#                     getattr(rs_person, 'PERSON_LAST_NAME'),
#                     getattr(rs_person, 'PERSON_MIDDLE_NAME'),
#                     getattr(rs_person, 'PERSON_FIRST_NAME')
#                 )
#                 json_return['TIME'] = getattr(row, 'TIME').strftime("%H:%M:%S")
#                 json_return['SESSION_NAME'] = getattr(row, 'SESSION_NAME')
#                 json_return['SESSION_NAME_EN'] = getattr(row, 'SESSION_NAME_EN')
#                 json_return['SESSION_STATUS_NAME'] = getattr(row, 'SESSION_STATUS_NAME')
#                 json_return['SESSION_STATUS_NAME_EN'] = getattr(row, 'SESSION_STATUS_NAME_EN')
#                 json_return['SESSION_IMAGE_BASE64'] = getattr(row, 'SESSION_IMAGE_BASE64').decode("utf-8")
#                 json_return['USED_STATUS_NAME'] = getattr(row, 'USED_STATUS_NAME')
#                 array_return.append(json_return)
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(e, exc_type, fname, exc_tb.tb_lineno)
#     session_sql.close()
#     return array_return


# def get_json_all_check_out():
#     # 1 check in morning
#     # 2 check in afternoon
#     # 3 check in evening
#     session_sql = SessionSql()
#     array_return = []
#     try:
#         date = datetime.datetime.today().strftime('%Y-%d-%m')
#         results_of_check = session_sql.query(Person_Check_Out).filter(
#             # Person_Check_In.PERSON_ID == person_id,
#             Person_Check_In.DATE == date,
#             Person_Check_In.USED_STATUS == 1
#         ).all()
#         if results_of_check is not None and len(results_of_check) > 0:
#             for row in results_of_check:
#                 json_return = {}
#
#                 rs_person = session_sql.query(Person).filter(Person.PERSON_ID == getattr(row, 'PERSON_ID')).first()
#                 json_return['PERSON_ID'] = int(getattr(rs_person, 'PERSON_ID'))
#                 json_return['PERSON_ID_NUMBER'] = getattr(rs_person, 'PERSON_ID_NUMBER')
#                 json_return['PERSON_FULL_NAME'] = get_full_name(
#                     getattr(rs_person, 'PERSON_LAST_NAME'),
#                     getattr(rs_person, 'PERSON_MIDDLE_NAME'),
#                     getattr(rs_person, 'PERSON_FIRST_NAME')
#                 )
#                 json_return['TIME'] = getattr(row, 'TIME').strftime("%H:%M:%S")
#                 json_return['SESSION_NAME'] = getattr(row, 'SESSION_NAME')
#                 json_return['SESSION_NAME_EN'] = getattr(row, 'SESSION_NAME_EN')
#                 json_return['SESSION_STATUS_NAME'] = getattr(row, 'SESSION_STATUS_NAME')
#                 json_return['SESSION_STATUS_NAME_EN'] = getattr(row, 'SESSION_STATUS_NAME_EN')
#                 json_return['SESSION_IMAGE_BASE64'] = getattr(row, 'SESSION_IMAGE_BASE64').decode("utf-8")
#                 json_return['USED_STATUS_NAME'] = getattr(row, 'USED_STATUS_NAME')
#                 array_return.append(json_return)
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(e, exc_type, fname, exc_tb.tb_lineno)
#     session_sql.close()
#     return array_return


def get_full_name(last, middle, first):
    if middle is not None or middle != '':
        full_name = last + ' ' + middle + ' ' + first
    else:
        full_name = last + ' ' + first

    return str(full_name)


def data_person_label_embedding():
    session_sql = SessionSql()
    all_persons = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
    array_return = []
    for row in all_persons:
        json_return = {
            'PERSON_ID': str(getattr(row, 'PERSON_ID')),
            'PERSON_ID_NUMBER': str(getattr(row, 'PERSON_ID_NUMBER')),
            'FULL_NAME': get_full_name(
                getattr(row, 'PERSON_LAST_NAME'),
                getattr(row, 'PERSON_MIDDLE_NAME'),
                getattr(row, 'PERSON_FIRST_NAME')
            ),
            'PERSON_EMB': np.frombuffer(getattr(row, 'PERSON_EMB_BASE64'), dtype="float32")
        }
        array_return.append(json_return)
    session_sql.close()
    return array_return


def get_list_of_users():
    session_sql = SessionSql()
    result_users = session_sql.query(Person).filter(
        Person.USED_STATUS == 1,
    ).all()
    array_return = []
    if len(result_users) > 0:
        for person in result_users:
            json_return = {}
            json_return['PERSON_ID_NUMBER'] = getattr(person, "PERSON_ID_NUMBER")
            json_return['PERSON_FULL_NAME'] = get_full_name(
                getattr(person, "PERSON_LAST_NAME"),
                getattr(person, "PERSON_MIDDLE_NAME"),
                getattr(person, "PERSON_FIRST_NAME")
            )
            json_return['PERSON_IMAGE_BASE64'] = getattr(person, "PERSON_IMAGE_BASE64").decode("utf-8")

            array_return.append(json_return)
    session_sql.close()
    return array_return


def max_person_id():
    session_sql = SessionSql()
    try:
        rs_max_id = session_sql.query(func.max(Person.PERSON_ID)).first()[0]
    except:
        rs_max_id = None
    if rs_max_id is not None:
        max_id = int(rs_max_id) + 1
    else:
        max_id = 1
    session_sql.close()
    return max_id


def get_person():
    session_sql = SessionSql()
    array_return = []
    rs = session_sql.query(Person).filter(Person.USED_STATUS != 0).order_by(desc(Person.PERSON_ID_NUMBER)).all()
    try:
        if len(rs) > 0:
            for row in rs:
                json_return = {}
                # for col in Person_columns:
                #     json_return[col] = getattr(row, col)
                json_return['PERSON_ID'] = str(getattr(row, 'PERSON_ID'))
                json_return['PERSON_ID_NUMBER'] = str(getattr(row, 'PERSON_ID_NUMBER'))
                json_return['FULL_NAME'] = get_full_name(
                    getattr(row, "PERSON_LAST_NAME"),
                    getattr(row, "PERSON_MIDDLE_NAME"),
                    getattr(row, "PERSON_FIRST_NAME")
                )
                json_return['PERSON_IMAGE_BASE64'] = getattr(row, 'PERSON_IMAGE_BASE64').decode("utf-8")
                json_return['DATE_TIME_CREATE'] = getattr(row, 'DATE_TIME_CREATE').strftime("%m/%d/%Y %H:%M:%S")
                array_return.append(json_return)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)

    session_sql.close()
    return array_return


def insert_person(person_id_number, last, middle, first, image_base64, emb_base64):
    error_code = 400
    session_sql = SessionSql()
    json_return = {}
    try:
        # date_insert = datetime.date.today().strftime('%d/%m/%Y')
        # time_insert = datetime.datetime.now().strftime("%H:%M:%S")
        # date_time_create = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        date_time_create = datetime.today()

        json_insert = {
            "PERSON_ID": max_person_id(),
            "PERSON_ID_NUMBER": person_id_number,
            "PERSON_LAST_NAME": last,
            "PERSON_MIDDLE_NAME": middle,
            "PERSON_FIRST_NAME": first,
            "PERSON_IMAGE_BASE64": image_base64,
            "PERSON_EMB_BASE64": emb_base64,
            "USED_STATUS": 1,
            "USED_STATUS_NAME": "In Use",
            "DATE_TIME_CREATE": date_time_create
        }
        print(json_insert)
        session_sql.add(Person(**json_insert))
        session_sql.commit()
        error_code = 200

        json_return = get_person()

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)

    session_sql.close()

    return error_code, json_return


# def attendance_table(date_query):
#     session_sql = SessionSql()
#     array_return = []
#     try:
#         rs_persons = session_sql.query(Person).filter(
#             Person.USED_STATUS == 1
#         ).all()
#
#         if len(rs_persons) > 0:
#             for row in rs_persons:
#                 json_return = {
#                     'PERSON_ID_NUMBER': getattr(row, 'PERSON_ID_NUMBER'),
#                     'PERSON_FULL_NAME': get_full_name(
#                         getattr(row, 'PERSON_LAST_NAME'),
#                         getattr(row, 'PERSON_MIDDLE_NAME'),
#                         getattr(row, 'PERSON_FIRST_NAME')
#                     ),
#                     'DATE': datetime.strptime(date_query, '%Y-%m-%d').strftime('%d/%m/%Y')
#                 }
#                 try:
#                     rs_check_in_session = session_sql.query(Person_Check_In).filter(
#                         Person_Check_In.PERSON_ID == getattr(row, 'PERSON_ID'),
#                         Person_Check_In.SESSION_ID == 1,
#                         Person_Check_In.DATE == date_query,
#                         Person_Check_In.USED_STATUS == 1,
#                     ).first()
#
#                     json_return['TIME_IN_1'] = getattr(rs_check_in_session, "TIME").strftime('%H:%M:%S')
#                     json_return['SESSION_NAME_EN_IN_1'] = getattr(rs_check_in_session, "SESSION_NAME_EN")
#                     json_return['SESSION_STATUS_NAME_EN_IN_1'] = getattr(rs_check_in_session, "SESSION_STATUS_NAME_EN")
#                     json_return['SESSION_IMAGE_BASE64_IN_1'] = getattr(rs_check_in_session,
#                                                                        "SESSION_IMAGE_BASE64").decode('utf-8')
#                 except:
#                     json_return['TIME_IN_1'] = '0:00:00'
#                     json_return['SESSION_NAME_EN_IN_1'] = 'Morning Shift'
#                     json_return['SESSION_STATUS_NAME_EN_IN_1'] = 'Not Yet Update'
#                     json_return['SESSION_IMAGE_BASE64_IN_1'] = ''
#
#                 try:
#                     rs_check_in_session = session_sql.query(Person_Check_Out).filter(
#                         Person_Check_Out.PERSON_ID == getattr(row, 'PERSON_ID'),
#                         Person_Check_Out.SESSION_ID == 1,
#                         Person_Check_Out.DATE == date_query,
#                         Person_Check_Out.USED_STATUS == 1,
#                     ).first()
#
#                     json_return['TIME_OUT_1'] = getattr(rs_check_in_session, "TIME").strftime('%H:%M:%S')
#                     json_return['SESSION_NAME_EN_OUT_1'] = getattr(rs_check_in_session, "SESSION_NAME_EN")
#                     json_return['SESSION_STATUS_NAME_EN_OUT_1'] = getattr(rs_check_in_session, "SESSION_STATUS_NAME_EN")
#                     json_return['SESSION_IMAGE_BASE64_OUT_1'] = getattr(rs_check_in_session,
#                                                                         "SESSION_IMAGE_BASE64").decode('utf-8')
#                 except:
#                     json_return['TIME_OUT_1'] = '0:00:00'
#                     json_return['SESSION_NAME_EN_OUT_1'] = 'Morning Shift'
#                     json_return['SESSION_STATUS_NAME_EN_OUT_1'] = 'Not Yet Update'
#                     json_return['SESSION_IMAGE_BASE64_OUT_1'] = ''
#
#                 try:
#                     rs_check_in_session = session_sql.query(Person_Check_In).filter(
#                         Person_Check_In.PERSON_ID == getattr(row, 'PERSON_ID'),
#                         Person_Check_In.SESSION_ID == 2,
#                         Person_Check_In.DATE == date_query,
#                         Person_Check_In.USED_STATUS == 1,
#                     ).first()
#
#                     json_return['TIME_IN_2'] = getattr(rs_check_in_session, "TIME").strftime('%H:%M:%S')
#                     json_return['SESSION_NAME_EN_IN_2'] = getattr(rs_check_in_session, "SESSION_NAME_EN")
#                     json_return['SESSION_STATUS_NAME_EN_IN_2'] = getattr(rs_check_in_session, "SESSION_STATUS_NAME_EN")
#                     json_return['SESSION_IMAGE_BASE64_IN_2'] = getattr(rs_check_in_session,
#                                                                        "SESSION_IMAGE_BASE64").decode('utf-8')
#                 except:
#                     json_return['TIME_IN_2'] = '0:00:00'
#                     json_return['SESSION_NAME_EN_IN_2'] = 'Afternoon Shift'
#                     json_return['SESSION_STATUS_NAME_EN_IN_2'] = 'Not Yet Update'
#                     json_return['SESSION_IMAGE_BASE64_IN_2'] = ''
#
#                 try:
#                     rs_check_in_session = session_sql.query(Person_Check_Out).filter(
#                         Person_Check_Out.PERSON_ID == getattr(row, 'PERSON_ID'),
#                         Person_Check_Out.SESSION_ID == 2,
#                         Person_Check_Out.DATE == date_query,
#                         Person_Check_Out.USED_STATUS == 1,
#                     ).first()
#
#                     json_return['TIME_OUT_2'] = getattr(rs_check_in_session, "TIME").strftime('%H:%M:%S')
#                     json_return['SESSION_NAME_EN__OUT_2'] = getattr(rs_check_in_session, "SESSION_NAME_EN")
#                     json_return['SESSION_STATUS_NAME_EN_OUT_2'] = getattr(rs_check_in_session, "SESSION_STATUS_NAME_EN")
#                     json_return['SESSION_IMAGE_BASE64_OUT_2'] = getattr(rs_check_in_session,
#                                                                         "SESSION_IMAGE_BASE64").decode('utf-8')
#                 except:
#                     json_return['TIME_OUT_2'] = '0:00:00'
#                     json_return['SESSION_NAME_EN_OUT_2'] = 'Afternoon Shift'
#                     json_return['SESSION_STATUS_NAME_EN_OUT_2'] = 'Not Yet Update'
#                     json_return['SESSION_IMAGE_BASE64_OUT_2'] = ''
#
#                 array_return.append(json_return)
#
#
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(e, exc_type, fname, exc_tb.tb_lineno)
#
#     session_sql.close()
#     print(date_query, array_return)
#     return array_return


def person_attendance_table(person_id, month, year):
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

    start_date = datetime.strptime('26/' + month_1 + '/' + str(year_1), '%d/%m/%Y')
    end_date = datetime.strptime('26/' + month_2 + '/' + str(year_2), '%d/%m/%Y')
    json_return = {}
    try:
        rs_persons = session_sql.query(Person).filter(
            Person.PERSON_ID == person_id,
            Person.USED_STATUS == 1
        ).first()

        json_return = {
            'msnv': getattr(rs_persons, 'PERSON_ID_NUMBER'),
            'name': get_full_name(
                getattr(rs_persons, 'PERSON_LAST_NAME'),
                getattr(rs_persons, 'PERSON_MIDDLE_NAME'),
                getattr(rs_persons, 'PERSON_FIRST_NAME')
            ),
            "month": month,  # filter month
            "year": year,  # filter year
            "current_year": datetime.now().year,  # current system year
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
        }
        array_date = []
        for _date in (start_date + timedelta(n) for n in range((end_date - start_date).days)):
            print(_date)
            json_date = {}
            json_date['date'] = _date.strftime('%Y-%m-%d')
            for session_id in [1, 2]:
                rs_person_check_in = session_sql.query(Person_Check_In).filter(
                    Person_Check_In.PERSON_ID == person_id,
                    Person_Check_In.SESSION_ID == session_id,
                    Person_Check_In.DATE == _date).first()

                rs_person_check_out = session_sql.query(Person_Check_Out).filter(
                    Person_Check_Out.PERSON_ID == person_id,
                    Person_Check_Out.SESSION_ID == session_id,
                    Person_Check_Out.DATE == _date).first()
                print(_date, session_id, rs_person_check_in, rs_person_check_out)
                if session_id == 1:
                    if rs_person_check_in is not None:
                        json_date['sa_status'] = True
                        json_date['sa_checkin'] = rs_person_check_in.TIME.strftime('%H:%M:%S')
                    else:
                        json_date['sa_status'] = False
                        json_date['sa_checkin'] = '0:00:00'

                    if rs_person_check_out is not None:
                        json_date['sa_checkout'] = rs_person_check_out.TIME.strftime('%H:%M:%S')
                    else:
                        json_date['sa_status'] = False
                        json_date['sa_checkout'] = '0:00:00'

                    # if json_date['sa_status'] == True:
                    #     json_date += 1
                else:
                    if rs_person_check_in is not None:
                        json_date['ch_status'] = True
                        json_date['ch_checkin'] = rs_person_check_in.TIME.strftime('%H:%M:%S')
                    else:
                        json_date['ch_status'] = False
                        json_date['ch_checkin'] = '0:00:00'

                    if rs_person_check_out is not None:
                        json_date['ch_checkout'] = rs_person_check_out.TIME.strftime('%H:%M:%S')
                    else:
                        json_date['ch_status'] = False
                        json_date['ch_checkout'] = '0:00:00'

                    # if json_date['ch_status'] == True:
                    #     json_date += 1
            # try:
            #     rs_check_in_session_in = session_sql.query(Person_Check_In).filter(
            #         Person_Check_In.PERSON_ID == person_id,
            #         Person_Check_In.SESSION_ID == 1,
            #         Person_Check_In.DATE == _date,
            #         Person_Check_In.USED_STATUS == 1,
            #     ).first()
            #
            #     rs_check_in_session_out = session_sql.query(Person_Check_Out).filter(
            #         Person_Check_Out.PERSON_ID == person_id,
            #         Person_Check_Out.SESSION_ID == 1,
            #         Person_Check_Out.DATE == _date,
            #         Person_Check_Out.USED_STATUS == 1,
            #     ).first()
            #
            #     json_date['sa_checkin'] = getattr(rs_check_in_session_in, "TIME").strftime('%H:%M:%S')
            #     json_date['sa_checkout'] = getattr(rs_check_in_session_out, "TIME").strftime('%H:%M:%S')
            #     json_date['sa_status'] = True
            # except:
            #     json_date['sa_checkin'] = '0:00:00'
            #     json_date['sa_checkout'] = '0:00:00'
            #     json_date['sa_status'] = False
            #
            # try:
            #     rs_check_in_session_in = session_sql.query(Person_Check_In).filter(
            #         Person_Check_In.PERSON_ID == person_id,
            #         Person_Check_In.SESSION_ID == 2,
            #         Person_Check_In.DATE == _date,
            #         Person_Check_In.USED_STATUS == 1,
            #     ).first()
            #
            #     rs_check_in_session_out = session_sql.query(Person_Check_Out).filter(
            #         Person_Check_Out.PERSON_ID == person_id,
            #         Person_Check_Out.SESSION_ID == 2,
            #         Person_Check_Out.DATE == _date,
            #         Person_Check_Out.USED_STATUS == 1,
            #     ).first()
            #
            #     json_date['ch_checkin'] = getattr(rs_check_in_session_in, "TIME").strftime('%H:%M:%S')
            #     json_date['ch_checkout'] = getattr(rs_check_in_session_out, "TIME").strftime('%H:%M:%S')
            #     json_date['ch_status'] = True
            # except:
            #     json_date['ch_checkin'] = '0:00:00'
            #     json_date['ch_checkout'] = '0:00:00'
            #     json_date['ch_status'] = False
            array_date.append(json_date)
        json_return['attendances'] = array_date
        json_return['count_attendances'] = 1


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)

    session_sql.close()
    return json_return
#
#
# def insert_auto_attendance(person_id, image_base64):
#     error_code = 400
#     session_sql = SessionSql()
#     array_return = []
#     # try:
#     morning_time_start_in = datetime.now().replace(hour=6, minute=0, second=0).strftime("%H:%M:%S")
#
#     morning_time_stop_in = datetime.now().replace(hour=7, minute=30, second=0).strftime("%H:%M:%S")
#
#     morning_time_start_out = datetime.now().replace(hour=10, minute=45, second=0).strftime("%H:%M:%S")
#
#     morning_time_stop_out = datetime.now().replace(hour=11, minute=30, second=0).strftime("%H:%M:%S")
#
#     afternoon_time_start_in = datetime.now().replace(hour=12, minute=30, second=0).strftime("%H:%M:%S")
#
#     afternoon_time_stop_in = datetime.now().replace(hour=14, minute=0, second=0).strftime("%H:%M:%S")
#
#     afternoon_time_start_out = datetime.now().replace(hour=16, minute=0, second=0).strftime("%H:%M:%S")
#
#     afternoon_time_stop_out = datetime.now().replace(hour=18, minute=0, second=0).strftime("%H:%M:%S")
#
#     time_now = datetime.now().strftime("%H:%M:%S")
#
#     stats_get = 0
#
#     if time_now >= morning_time_start_in and time_now <= morning_time_stop_in:
#         stats_get = 1
#         session_id = 1
#         session_name = 'Buổi Sáng'
#         session_name_en = "Morning Shift"
#         object_get = Person_Check_In
#         status_name = 'Đã diểm danh'
#         status_name_en = 'Attended'
#     elif time_now >= morning_time_start_out and time_now <= morning_time_stop_out:
#         stats_get = 2
#         session_id = 1
#         session_name = 'Buổi Sáng'
#         session_name_en = "Morning Shift"
#         object_get = Person_Check_Out
#         status_name = 'Đã ra về'
#         status_name_en = 'Left'
#     elif time_now >= afternoon_time_start_in and time_now <= afternoon_time_stop_in:
#         stats_get = 1
#         session_id = 2
#         session_name = 'Buổi Chiều'
#         session_name_en = "Afternoon Shift"
#         object_get = Person_Check_In
#         status_name = 'Đã diểm danh'
#         status_name_en = 'Attended'
#     elif time_now >= afternoon_time_start_out and time_now <= afternoon_time_stop_out:
#         stats_get = 2
#         session_id = 2
#         session_name = 'Buổi Chiều'
#         session_name_en = "Afternoon Shift"
#         object_get = Person_Check_Out
#         status_name = 'Đã ra về'
#         status_name_en = 'Left'
#     else:
#         session_id = 3
#         session_name = 'Buổi Tối'
#         session_name_en = "Evening Shift"
#         status_name = 'Đã ra về'
#         status_name_en = 'Left'
#         object_get = Person_Check_In
#     time_insert = datetime.now().strftime("%H:%M:%S")
#     date_insert = date.today().strftime('%Y-%m-%d')
#
#     # rs_check = session_sql.query(object_get).filter(
#     #     object_get.PERSON_ID == person_id,
#     #     object_get.DATE == date_insert,
#     #     object_get.SESSION_ID == session_id).all()
#     # if len(rs_check) == 0:
#     json_insert = {
#         "PERSON_ID": person_id,
#         "DATE": date_insert,
#         "TIME": time_insert,
#         "SESSION_ID": session_id,
#         "SESSION_NAME": session_name,
#         "SESSION_NAME_EN": session_name_en,
#         "SESSION_STATUS_NAME": status_name,
#         "SESSION_STATUS_NAME_EN": status_name_en,
#         "SESSION_IMAGE_BASE64": image_base64,
#         "USED_STATUS": 1,
#         "USED_STATUS_NAME": "In Use",
#     }
#     print('json_insert', json_insert)
#
#     if person_id is not None and int(person_id) > 0:
#         try:
#             session_sql.add(object_get(**json_insert))
#             session_sql.commit()
#             error_code = 200
#             if stats_get == 1:
#                 array_return = get_check_in(date_insert)
#             else:
#                 array_return = get_check_out(date_insert)
#         except:
#             error_code = 201
#         print('Kiem tra try ex', error_code, array_return)
#
#     # except Exception as e:
#     #     exc_type, exc_obj, exc_tb = sys.exc_info()
#     #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#     #     print(e, exc_type, fname, exc_tb.tb_lineno)
#     print('error_code', error_code)
#     session_sql.close()
#
#     return error_code, array_return


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

    start_date = datetime.strptime('26/' + month_1 + '/' + str(year_1), '%d/%m/%Y')
    end_date = datetime.strptime('26/' + month_2 + '/' + str(year_2), '%d/%m/%Y')

    rs_persons = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
    sample_data = {
        "month": month,  # filter month
        "year": year,  # filter year
        "current_year": datetime.now().year,  # current system year
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
    }
    if len(rs_persons) > 0:
        data = []
        for row_person in rs_persons:
            json1_person = {}
            json1_person['id_person'] = str(getattr(row_person, "PERSON_ID"))
            json1_person['msnv'] = getattr(row_person, "PERSON_ID_NUMBER")
            json1_person['name'] = get_full_name(
                getattr(row_person, 'PERSON_LAST_NAME'),
                getattr(row_person, 'PERSON_MIDDLE_NAME'),
                getattr(row_person, 'PERSON_FIRST_NAME')
            )
            person_date_data = []
            count_session = 0
            json_person = {}
            for _date in (start_date + timedelta(n) for n in range((end_date - start_date).days)):

                json_person = {}
                json_person["date"] = _date.strftime('%Y-%m-%d')

                for session_id in [1,2]:
                    rs_person_check_in = session_sql.query(Person_Check).filter(
                        Person_Check.PERSON_ID == row_person.PERSON_ID,
                        Person_Check.SESSION_ID == session_id,
                        Person_Check.SESSION_CHECK_ID == 1,

                        Person_Check.DATE == _date).first()

                    rs_person_check_out = session_sql.query(Person_Check).filter(
                        Person_Check.PERSON_ID == row_person.PERSON_ID,
                        Person_Check.SESSION_ID == session_id,
                        Person_Check.SESSION_CHECK_ID == 2,

                        Person_Check.DATE == _date).first()
                    # print(_date, session_id, rs_person_check_in, rs_person_check_out)
                    if session_id == 1:
                        if rs_person_check_in is not None:
                            json_person['sa_status'] = True
                            json_person['sa_checkin'] = rs_person_check_in.TIME.strftime('%H:%M:%S')
                        else:
                            json_person['sa_status'] = False
                            json_person['sa_checkin'] = '0:00:00'

                        if rs_person_check_out is not None:
                            json_person['sa_checkout'] = rs_person_check_out.TIME.strftime('%H:%M:%S')
                        else:
                            json_person['sa_status'] = False
                            json_person['sa_checkout'] = '0:00:00'

                        if json_person['sa_status'] == True:
                            count_session += 1
                    else:
                        if rs_person_check_in is not None:
                            json_person['ch_status'] = True
                            json_person['ch_checkin'] = rs_person_check_in.TIME.strftime('%H:%M:%S')
                        else:
                            json_person['ch_status'] = False
                            json_person['ch_checkin'] = '0:00:00'

                        if rs_person_check_out is not None:
                            json_person['ch_checkout'] = rs_person_check_out.TIME.strftime('%H:%M:%S')
                        else:
                            json_person['ch_status'] = False
                            json_person['ch_checkout'] = '0:00:00'

                        if json_person['ch_status'] == True:
                            count_session += 1

                person_date_data.append(json_person)


            json1_person['attendances'] = person_date_data
            json1_person['count_attendances'] = count_session

            data.append(json1_person)
        sample_data['data'] = data
    session_sql.close()
    return sample_data


def data_attendances_date_month_year_by_month(month, year):
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

    start_date = datetime.strptime('26/' + month_1 + '/' + str(year_1), '%d/%m/%Y')
    end_date = datetime.strptime('26/' + month_2 + '/' + str(year_2), '%d/%m/%Y')

    rs_persons = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()
    sample_data = {
        "month": month,  # filter month
        "year": year,  # filter year
        "current_year": datetime.now().year,  # current system year
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
    }
    if len(rs_persons) > 0:
        data = []
        for row_person in rs_persons:
            json1_person = {}
            json1_person['id_person'] = str(getattr(row_person, "PERSON_ID"))
            json1_person['msnv'] = getattr(row_person, "PERSON_ID_NUMBER")
            json1_person['name'] = get_full_name(
                getattr(row_person, 'PERSON_LAST_NAME'),
                getattr(row_person, 'PERSON_MIDDLE_NAME'),
                getattr(row_person, 'PERSON_FIRST_NAME')
            )
            person_date_data = []
            count_session = 0
            json_person = {}

            rs_person_check = session_sql.query(Person_Check).filter(
                Person_Check.PERSON_ID == str(getattr(row_person, "PERSON_ID")),
                Person_Check.MAIN_MONTH == month,
                Person_Check.MAIN_YEAR == year,
                Person_Check.USED_STATUS != 0
            ).all()
            array_person_check_all = []
            if len(rs_person_check) > 0:
                for row_rs_person_chek  in rs_person_check:
                    json_row_person_check = {}
                    for col in Person_Check_columns:
                        json_row_person_check[col] = getattr(row_rs_person_chek, col)
                        array_person_check_all.append(json_row_person_check)


            for row in array_person_check_all:
                print(row)
            break
            # json_person = {}
            # json_person["date"] = _date.strftime('%Y-%m-%d')
            #
            # for session_id in [1,2]:
            #     rs_person_check_in = session_sql.query(Person_Check).filter(
            #         Person_Check.PERSON_ID == row_person.PERSON_ID,
            #         Person_Check.SESSION_ID == session_id,
            #         Person_Check.SESSION_CHECK_ID == 1,
            #
            #         Person_Check.DATE == _date).first()
            #
            #     rs_person_check_out = session_sql.query(Person_Check).filter(
            #         Person_Check.PERSON_ID == row_person.PERSON_ID,
            #         Person_Check.SESSION_ID == session_id,
            #         Person_Check.SESSION_CHECK_ID == 2,
            #
            #         Person_Check.DATE == _date).first()
            #     # print(_date, session_id, rs_person_check_in, rs_person_check_out)
            #     if session_id == 1:
            #         if rs_person_check_in is not None:
            #             json_person['sa_status'] = True
            #             json_person['sa_checkin'] = rs_person_check_in.TIME.strftime('%H:%M:%S')
            #         else:
            #             json_person['sa_status'] = False
            #             json_person['sa_checkin'] = '0:00:00'
            #
            #         if rs_person_check_out is not None:
            #             json_person['sa_checkout'] = rs_person_check_out.TIME.strftime('%H:%M:%S')
            #         else:
            #             json_person['sa_status'] = False
            #             json_person['sa_checkout'] = '0:00:00'
            #
            #         if json_person['sa_status'] == True:
            #             count_session += 1
            #     else:
            #         if rs_person_check_in is not None:
            #             json_person['ch_status'] = True
            #             json_person['ch_checkin'] = rs_person_check_in.TIME.strftime('%H:%M:%S')
            #         else:
            #             json_person['ch_status'] = False
            #             json_person['ch_checkin'] = '0:00:00'
            #
            #         if rs_person_check_out is not None:
            #             json_person['ch_checkout'] = rs_person_check_out.TIME.strftime('%H:%M:%S')
            #         else:
            #             json_person['ch_status'] = False
            #             json_person['ch_checkout'] = '0:00:00'
            #
            #         if json_person['ch_status'] == True:
            #             count_session += 1
            #
            # person_date_data.append(json_person)
            #
            #
            # json1_person['attendances'] = person_date_data
            # json1_person['count_attendances'] = count_session

            data.append(json1_person)
        sample_data['data'] = data
    session_sql.close()
    return sample_data


def test_insert_check_in_check_out(month, year):
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

    start_date = datetime.strptime('26/' + month_1 + '/' + str(year_1), '%d/%m/%Y')
    end_date = datetime.strptime('26/' + month_2 + '/' + str(year_2), '%d/%m/%Y')

    rs_persons = session_sql.query(Person).filter(Person.USED_STATUS == 1).all()

    if len(rs_persons) > 0:
        for r_person in rs_persons:
            print(r_person)
            for _date in (start_date + timedelta(n) for n in range((end_date - start_date).days)):
                # json_check_in_morning = {}
                # json_check_out_morning = {}
                # json_check_in_evening = {}
                # json_check_out_evening = {}
                json_check = {}
                sess = []
                if int(_date.weekday()) == 5:
                    sess = [1]
                elif int(_date.weekday()) != 6 and int(_date.weekday()) != 5:
                    sess = [1, 2]


                for ses in sess:
                    for ses_c in [1, 2]:
                        if ses_c == 1 and ses == 1:
                            time = 6
                            ms = random.randrange(30, 59, 1)
                            sc = random.randrange(0, 59, 1)
                            json_check['SESSION_CHECK_ID'] = ses_c
                            json_check['SESSION_CHECK_NAME'] = 'Vào'
                            json_check['SESSION_CHECK_NAME_EN'] = 'CheckIn'
                            json_check['SESSION_STATUS_NAME'] = 'Đã điểm danh'
                            json_check['SESSION_STATUS_NAME_EN'] = 'Attended'
                            get_time = datetime.now().replace(hour=time, minute=ms, second=sc).strftime("%H:%M:%S")
                            json_check['TIME'] = get_time

                            json_check['SESSION_ID'] = ses
                            json_check['SESSION_NAME'] = 'Buổi Sáng'
                            json_check['SESSION_NAME_EN'] = 'Morning Shift'
                        elif ses_c == 2 and ses == 1:
                            time = 10
                            ms = random.randrange(50, 59, 1)
                            sc = random.randrange(0, 59, 1)
                            get_time = datetime.now().replace(hour=time, minute=ms, second=sc).strftime("%H:%M:%S")
                            json_check['TIME'] = get_time

                            json_check['SESSION_CHECK_ID'] = ses_c
                            json_check['SESSION_CHECK_NAME'] = 'Ra'
                            json_check['SESSION_CHECK_NAME_EN'] = 'CheckOut'
                            json_check['SESSION_STATUS_NAME'] = 'Đã ra về'
                            json_check['SESSION_STATUS_NAME_EN'] = 'Left'

                            json_check['SESSION_ID'] = ses
                            json_check['SESSION_NAME'] = 'Buổi Sáng'
                            json_check['SESSION_NAME_EN'] = 'Morning Shift'
                        elif ses_c == 1 and ses == 2:
                            time = 12
                            ms = random.randrange(30, 59, 1)
                            sc = random.randrange(0, 59, 1)
                            get_time = datetime.now().replace(hour=time, minute=ms, second=sc).strftime("%H:%M:%S")
                            json_check['TIME'] = get_time

                            json_check['SESSION_CHECK_ID'] = ses_c
                            json_check['SESSION_CHECK_NAME'] = 'Vào'
                            json_check['SESSION_CHECK_NAME_EN'] = 'CheckIn'
                            json_check['SESSION_STATUS_NAME'] = 'Đã điểm danh'
                            json_check['SESSION_STATUS_NAME_EN'] = 'Attended'

                            json_check['SESSION_ID'] = ses
                            json_check['SESSION_NAME'] = 'Buổi Chiều'
                            json_check['SESSION_NAME_EN'] = 'Evening Shift'
                        # elif ses_c == 2 and ses == 2:
                        else:
                            time = 16
                            ms = random.randrange(50, 59, 1)
                            sc = random.randrange(0, 59, 1)


                            json_check['SESSION_CHECK_ID'] = ses_c
                            json_check['SESSION_CHECK_NAME'] = 'Ra'
                            json_check['SESSION_CHECK_NAME_EN'] = 'CheckOut'
                            json_check['SESSION_STATUS_NAME'] = 'Đã ra về'
                            json_check['SESSION_STATUS_NAME_EN'] = 'Left'

                            json_check['SESSION_ID'] = ses
                            json_check['SESSION_NAME'] = 'Buổi Chiều'
                            json_check['SESSION_NAME_EN'] = 'Evenning Shift'
                        get_time = datetime.now().replace(hour=time, minute=ms, second=sc).strftime("%H:%M:%S")
                        json_check['TIME'] = get_time
                        json_check['DATETIME'] = datetime.now().replace(day=_date.day, month=_date.month, year=_date.year, hour=time, minute=ms, second=sc).strftime("%Y-%m-%d %H:%M:%S")
                        json_check['DATE'] = _date
                        json_check['PERSON_ID'] = getattr(r_person, "PERSON_ID")
                        json_check['SESSION_IMAGE_BASE64'] = getattr(r_person, "PERSON_IMAGE_BASE64")
                        json_check['USED_STATUS'] = 2
                        json_check['USED_STATUS_NAME'] = "TEST DATA"
                        json_check['MAIN_MONTH'] = int(month)
                        json_check['MAIN_YEAR'] = int(year)

                        try:
                            session_sql.add(Person_Check(**json_check))
                            session_sql.commit()
                        except Exception as e:
                            session_sql.rollback()
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(e, exc_type, fname, exc_tb.tb_lineno)



                # time = 10
                # ms = random.randrange(50, 59, 1)
                # sc = random.randrange(0, 59, 1)
                # get_time = datetime.now().replace(hour=time, minute=ms, second=sc).strftime("%H:%M:%S")
                # json_check_out_morning['TIME'] = get_time
                # json_check_out_morning['DATE'] = _date
                # json_check_out_morning['PERSON_ID'] = getattr(r_person, "PERSON_ID")
                # json_check_out_morning['SESSION_IMAGE_BASE64'] = getattr(r_person, "PERSON_IMAGE_BASE64")
                # json_check_out_morning['USED_STATUS'] = 2
                # json_check_out_morning['USED_STATUS_NAME'] = "TEST DATA"
                # json_check_out_morning['SESSION_ID'] = 1
                # json_check_out_morning['SESSION_NAME'] = 'Buổi Sáng'
                # json_check_out_morning['SESSION_NAME_EN'] = 'Morning Shift'
                # json_check_out_morning['SESSION_STATUS_NAME'] = 'Đã ra về'
                # json_check_out_morning['SESSION_STATUS_NAME_EN'] = 'Left'
                #
                # time = 12
                # ms = random.randrange(30, 59, 1)
                # sc = random.randrange(0, 59, 1)
                # get_time = datetime.now().replace(hour=time, minute=ms, second=sc).strftime("%H:%M:%S")
                # json_check_in_evening['TIME'] = get_time
                # json_check_in_evening['DATE'] = _date
                # json_check_in_evening['PERSON_ID'] = getattr(r_person, "PERSON_ID")
                # json_check_in_evening['SESSION_IMAGE_BASE64'] = getattr(r_person, "PERSON_IMAGE_BASE64")
                # json_check_in_evening['USED_STATUS'] = 2
                # json_check_in_evening['USED_STATUS_NAME'] = "TEST DATA"
                # json_check_in_evening['SESSION_ID'] = 2
                # json_check_in_evening['SESSION_NAME'] = 'Buổi Chiều'
                # json_check_in_evening['SESSION_NAME_EN'] = 'Afternoon Shift'
                # json_check_in_evening['SESSION_STATUS_NAME'] = 'Đã điểm danh'
                # json_check_in_evening['SESSION_STATUS_NAME_EN'] = 'Attended'
                #
                # time = 16
                # ms = random.randrange(50, 59, 1)
                # sc = random.randrange(0, 59, 1)
                # get_time = datetime.now().replace(hour=time, minute=ms, second=sc).strftime("%H:%M:%S")
                # json_check_out_evening['TIME'] = get_time
                # json_check_out_evening['DATE'] = _date
                # json_check_out_evening['PERSON_ID'] = getattr(r_person, "PERSON_ID")
                #
                # json_check_out_evening['SESSION_IMAGE_BASE64'] = getattr(r_person, "PERSON_IMAGE_BASE64")
                # json_check_out_evening['USED_STATUS'] = 2
                # json_check_out_evening['USED_STATUS_NAME'] = "TEST DATA"
                #
                # json_check_out_evening['SESSION_ID'] = 2
                # json_check_out_evening['SESSION_NAME'] = 'Buổi Chiều'
                # json_check_out_evening['SESSION_NAME_EN'] = 'Afternoon Shift'
                # json_check_out_evening['SESSION_STATUS_NAME'] = 'Đã ra về'
                # json_check_out_evening['SESSION_STATUS_NAME'] = 'Left'

                # print(_date,_date.weekday(), int(_date.weekday()))
                #
                # if int(_date.weekday()) == 5:
                #     try:
                #         session_sql.add(Person_Check_In(**json_check_in_morning))
                #         session_sql.commit()
                #     except Exception as e:
                #         exc_type, exc_obj, exc_tb = sys.exc_info()
                #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                #         print(e, exc_type, fname, exc_tb.tb_lineno)
                #
                #     try:
                #         session_sql.add(Person_Check_Out(**json_check_out_morning))
                #         session_sql.commit()
                #     except Exception as e:
                #         exc_type, exc_obj, exc_tb = sys.exc_info()
                #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                #         print(e, exc_type, fname, exc_tb.tb_lineno)
                #
                # elif int(_date.weekday()) != 6 and int(_date.weekday()) != 5:
                #
                #     try:
                #         session_sql.add(Person_Check_Out(**json_check_out_evening))
                #         session_sql.commit()
                #     except Exception as e:
                #         exc_type, exc_obj, exc_tb = sys.exc_info()
                #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                #         print(e, exc_type, fname, exc_tb.tb_lineno)
                #
                #     try:
                #         session_sql.add(Person_Check_Out(**json_check_out_morning))
                #         session_sql.commit()
                #     except Exception as e:
                #         exc_type, exc_obj, exc_tb = sys.exc_info()
                #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                #         print(e, exc_type, fname, exc_tb.tb_lineno)
                #
                #     try:
                #         session_sql.add(Person_Check_In(**json_check_in_morning))
                #         session_sql.commit()
                #     except Exception as e:
                #         exc_type, exc_obj, exc_tb = sys.exc_info()
                #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                #         print(e, exc_type, fname, exc_tb.tb_lineno)
                #
                #     try:
                #         session_sql.add(Person_Check_In(**json_check_in_evening))
                #         session_sql.commit()
                #     except Exception as e:
                #         exc_type, exc_obj, exc_tb = sys.exc_info()
                #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                #         print(e, exc_type, fname, exc_tb.tb_lineno)

    session_sql.close()

    return 1


def data_personal_profile(person_id, month, year):
    session_sql = SessionSql()

    if month is None and year is None:
        month = datetime.today().month
        year = datetime.today().year


    rs_personal = session_sql.query(Person).filter(Person.PERSON_ID == person_id,
                                                   Person.USED_STATUS == 1).first()
    json_profile = {}
    if rs_personal is not None:
        json_profile['full_name'] = get_full_name(
            getattr(rs_personal, 'PERSON_LAST_NAME'),
            getattr(rs_personal, 'PERSON_MIDDLE_NAME'),
            getattr(rs_personal, 'PERSON_FIRST_NAME')
        )
        json_profile['MONTH'] = month
        json_profile['YEAR'] = year
        json_profile['PERSON_ID'] = getattr(rs_personal, 'PERSON_ID')
        json_profile['PERSON_ID_NUMBER'] = getattr(rs_personal, 'PERSON_ID_NUMBER')
        json_profile['PERSON_DOB'] = getattr(rs_personal, 'PERSON_DOB')
        json_profile['PERSON_POB'] = getattr(rs_personal, 'PERSON_POB')
        json_profile['PERSON_IMAGE_BASE64'] = getattr(rs_personal, 'PERSON_IMAGE_BASE64').decode("utf-8")
        json_profile['PERSON_EMAIL'] = getattr(rs_personal, 'PERSON_EMAIL')
        json_profile['ID_NUMBER'] = getattr(rs_personal, 'ID_NUMBER')
        json_profile['USED_STATUS'] = getattr(rs_personal, 'USED_STATUS')
        json_profile['PERSON_ID'] = getattr(rs_personal, 'PERSON_POB')
        json_profile['USED_STATUS_NAME'] = getattr(rs_personal, 'USED_STATUS_NAME')

        json_profile['TOTALS'] = str(len(session_sql.query(Person_Check).filter(
            Person_Check.PERSON_ID == person_id,
            Person_Check.SESSION_CHECK_ID == 2,
            Person_Check.MAIN_YEAR == year,
            Person_Check.USED_STATUS != 0).all()))
        json_profile['TOTALS_MONTH'] = str(len(session_sql.query(Person_Check).filter(
            Person_Check.PERSON_ID == person_id,
            Person_Check.MAIN_MONTH == month,
            Person_Check.MAIN_YEAR == year,
            Person_Check.SESSION_CHECK_ID == 2,
            Person_Check.USED_STATUS != 0).all()))

        json_profile['USED_STATUS_NAME'] = getattr(rs_personal, 'USED_STATUS_NAME')
        json_profile['USED_STATUS_NAME'] = getattr(rs_personal, 'USED_STATUS_NAME')

        array_check = []

        rs_check = session_sql.query(Person_Check).filter(Person_Check.PERSON_ID == person_id,
                                                                Person_Check.USED_STATUS != 1,
                                                                Person_Check.MAIN_MONTH == month,
                                                          Person_Check.MAIN_YEAR == year,

                                                          ).order_by(Person_Check.DATETIME).all()

        if len(rs_check) > 0:
            for row in rs_check:
                json_check = {}
                json_check['DATETIME'] = getattr(row, 'DATETIME')
                json_check['SESSION_CHECK_ID'] = getattr(row, 'SESSION_CHECK_ID')
                json_check['SESSION_CHECK_NAME'] = getattr(row, 'SESSION_CHECK_NAME')
                json_check['SESSION_CHECK_NAME_EN'] = getattr(row, 'SESSION_CHECK_NAME_EN')
                json_check['DATE'] = getattr(row, 'DATE').strftime("%d/%m/%Y")
                json_check['TIME'] = getattr(row, 'TIME').strftime("%H:%M:%S")
                json_check['UNTIL_NOW'] = (getattr(row, 'DATETIME') - datetime.now()).days
                json_check['SESSION_ID'] = getattr(row, 'SESSION_ID')
                json_check['SESSION_NAME'] = getattr(row, 'SESSION_NAME')
                json_check['SESSION_NAME_EN'] = getattr(row, 'SESSION_NAME_EN')
                json_check['SESSION_STATUS_NAME'] = getattr(row, 'SESSION_STATUS_NAME')
                json_check['SESSION_STATUS_NAME_EN'] = getattr(row, 'SESSION_STATUS_NAME_EN')
                json_check['SESSION_IMAGE_BASE64'] = getattr(row, 'SESSION_IMAGE_BASE64').decode('utf-8')
                array_check.append(json_check)
                # json_check['DATETIME'] = getattr(row, 'DATETIME')
                # json_check['DATETIME'] = getattr(row, 'DATETIME')

        json_profile['timeline'] = array_check


    session_sql.close()
    return json_profile


def auto_create_account():
    session_sql = SessionSql()

    session_sql.close()

    return 1


# if __name__ == "__main__":
#     data_attendances_date_month_year_by_month("5", "2022")

    # for m in [1,2,3,4,5,6,7,8,9,10,11,12]:
    #     test_insert_check_in_check_out(m, 2021)
    # data = datetime.today()
    # end_date = data + timedelta(days=2)
    # print(end_date)
    # print(data.weekday())
    # print(end_date.weekday())


