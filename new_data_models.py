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

# engine = create_engine("mssql+pyodbc://sa:123456@192.168.1.179:49999/face_attendance_8_11_2021?driver=SQL+Server")
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

Person_Attendance = Base.classes.PERSON_ATTENDANCE
Person_Attendance_columns = Person_Attendance.__table__.columns.keys()

Person_Session_1 = Base.classes.PERSON_SESSION_1
Person_Session_1_columns = Person_Session_1.__table__.columns.keys()

Person_Session_2 = Base.classes.PERSON_SESSION_2
Person_Session_2_columns = Person_Session_2.__table__.columns.keys()

Person_Session_3 = Base.classes.PERSON_SESSION_3
Person_Session_3_columns = Person_Session_3.__table__.columns.keys()

Person_Check_In = Base.classes.PERSON_CHECK_IN
Person_Check_In_columns = Person_Check_In.__table__.columns.keys()

Person_Check_Out = Base.classes.PERSON_CHECK_OUT
Person_Check_Out_columns = Person_Check_Out.__table__.columns.keys()


def insert_check_in(person_id, image_base64):
    error_code = 400
    session_sql = SessionSql()
    try:
        morning_time = datetime.datetime.now().replace(hour=6, minute=0, second=0).strftime("%H:%M:%S")
        afternoon_time = datetime.datetime.now().replace(hour=11, minute=0, second=0).strftime("%H:%M:%S")
        evening_time = datetime.datetime.now().replace(hour=17, minute=0, second=0).strftime("%H:%M:%S")
        time_now = datetime.datetime.now().strftime("%H:%M:%S")
        if time_now >= morning_time and time_now <= afternoon_time:
            session_id = 1
            session_name = 'Buổi Sáng'
            session_name_en = "Morning Shift"
        elif time_now > afternoon_time and time_now <= evening_time:
            session_id = 2
            session_name = 'Buổi Chiều'
            session_name_en = "Afternoon Shift"
        # elif time_now > evening_time:
        else:
            session_id = 3
            session_name = 'Buổi Tối'
            session_name_en = "Evening Shift"
        date_insert = datetime.date.today().strftime('%d/%m/%Y')

        rs_check = session_sql.query(Person_Check_In).filter(
            Person_Check_In.PERSON_ID == person_id,
            Person_Check_In.DATE == date_insert,
            Person_Check_In.SESSION_ID == session_id).all()
        if len(rs_check) == 0:
            if person_id is not None and int(person_id) > 0:
                json_insert = {
                    "PERSON_ID": person_id,
                    "DATE": date_insert,
                    "TIME": datetime.datetime.now().strftime("%H:%M:%S"),
                    "SESSION_ID": session_id,
                    "SESSION_NAME": session_name,
                    "SESSION_NAME_EN": session_name_en,
                    "SESSION_STATUS_NAME": 'Đã điểm danh',
                    "SESSION_STATUS_NAME_EN": 'Attend',
                    "SESSION_IMAGE_BASE64": image_base64,
                    "USED_STATUS": 1,
                    "USED_STATUS_NAME": "In Use",
                }
                session_sql.add(Person_Check_In(**json_insert))
                error_code = 200
                session_sql.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)

    session_sql.close()
    return error_code


def insert_check_out(person_id, image_base64):
    error_code = 400
    session_sql = SessionSql()
    try:
        morning_time = datetime.datetime.now().replace(hour=7, minute=0, second=0).strftime("%H:%M:%S")
        afternoon_time = datetime.datetime.now().replace(hour=13, minute=0, second=0).strftime("%H:%M:%S")
        evening_time = datetime.datetime.now().replace(hour=18, minute=0, second=0).strftime("%H:%M:%S")
        time_now = datetime.datetime.now().strftime("%H:%M:%S")

        date_insert = datetime.date.today().strftime('%d/%m/%Y')



        if time_now >= morning_time and time_now <= afternoon_time:
            session_id = 1
            session_name = 'Buổi Sáng'
            session_name_en = "Morning Shift"
        elif time_now > afternoon_time and time_now <= evening_time:
            session_id = 2
            session_name = 'Buổi Chiều'
            session_name_en = "Afternoon Shift"
        # elif time_now > evening_time:
        else:
            session_id = 3
            session_name = 'Buổi Tối'
            session_name_en = "Evening Shift"

        rs_check = session_sql.query(Person_Check_Out).filter(
            Person_Check_In.PERSON_ID == person_id,
            Person_Check_In.DATE == date_insert,
            Person_Check_In.SESSION_ID == session_id).all()
        if len(rs_check) == 0:
            if person_id is not None and int(person_id) > 0:
                json_insert = {
                    "PERSON_ID": person_id,
                    "DATE": date_insert,
                    "TIME": datetime.datetime.now().strftime("%H:%M:%S"),
                    "SESSION_ID": session_id,
                    "SESSION_NAME": session_name,
                    "SESSION_NAME_EN": session_name_en,
                    "SESSION_STATUS_NAME": 'Đã hoàn thành buổi làm',
                    "SESSION_STATUS_NAME_EN": 'Done a Shift',
                    "SESSION_IMAGE_BASE64": image_base64,
                    "USED_STATUS": 1,
                    "USED_STATUS_NAME": "In Use",
                }
                session_sql.add(Person_Check_Out(**json_insert))
                error_code = 200
                session_sql.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)

    session_sql.close()
    return error_code


def get_json_person_check_in(person_id, date, session_process=1):
    # 1 check in morning
    # 2 check in afternoon
    # 3 check in evening
    session_sql = SessionSql()
    json_return = {}
    try:
        if person_id is not None and date is not None:
            date = datetime.datetime.strptime(date, '%d/%m/%Y')
            if int(session_process) == 1:
                results_of_check = session_sql.query(Person_Check_In).filter(
                    Person_Check_In.PERSON_ID == person_id,
                    Person_Check_In.DATE == date,
                    Person_Check_In.USED_STATUS == 1
                ).all()
                if results_of_check is not None and len(results_of_check) > 0:
                    json_return['SESSION_NAME'] = getattr(results_of_check, 'SESSION_NAME')
                    json_return['SESSION_NAME_EN'] = getattr(results_of_check, 'SESSION_NAME_EN')
                    json_return['SESSION_STATUS_NAME'] = getattr(results_of_check, 'SESSION_STATUS_NAME')
                    json_return['SESSION_STATUS_NAME_EN'] = getattr(results_of_check, 'SESSION_STATUS_NAME_EN')
                    json_return['SESSION_IMAGE_BASE64'] = getattr(results_of_check, 'SESSION_IMAGE_BASE64')
                    json_return['USED_STATUS_NAME'] = getattr(results_of_check, 'USED_STATUS_NAME')
                else:
                    pass
        else:
            pass
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
    session_sql.close()
    return json_return


def get_json_person_check_out(person_id, date, session_process=1):
    # 1 check in morning
    # 2 check in afternoon
    # 3 check in evening
    session_sql = SessionSql()
    json_return = {}
    try:
        if person_id is not None and date is not None:
            date = datetime.datetime.strptime(date, '%d/%m/%Y')
            if int(session_process) == 1:
                results_of_check = session_sql.query(Person_Check_Out).filter(
                    Person_Check_Out.PERSON_ID == person_id,
                    Person_Check_Out.DATE == date,
                    Person_Check_Out.USED_STATUS == 1
                ).all()
                if results_of_check is not None and len(results_of_check) > 0:
                    json_return['SESSION_NAME'] = getattr(results_of_check, 'SESSION_NAME')
                    json_return['SESSION_NAME_EN'] = getattr(results_of_check, 'SESSION_NAME_EN')
                    json_return['SESSION_STATUS_NAME'] = getattr(results_of_check, 'SESSION_STATUS_NAME')
                    json_return['SESSION_STATUS_NAME_EN'] = getattr(results_of_check, 'SESSION_STATUS_NAME_EN')
                    json_return['SESSION_IMAGE_BASE64'] = getattr(results_of_check, 'SESSION_IMAGE_BASE64')
                    json_return['USED_STATUS_NAME'] = getattr(results_of_check, 'USED_STATUS_NAME')
                else:
                    pass
        else:
            pass
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
    session_sql.close()
    return json_return

def get_json_all_check_in():
    # 1 check in morning
    # 2 check in afternoon
    # 3 check in evening
    session_sql = SessionSql()
    array_return = []
    try:
        date = datetime.datetime.today().strftime('%Y-%d-%m')
        results_of_check = session_sql.query(Person_Check_In).filter(
            # Person_Check_In.PERSON_ID == person_id,
            Person_Check_In.DATE == date,
            Person_Check_In.USED_STATUS == 1
        ).all()
        if results_of_check is not None and len(results_of_check) > 0:
            for row in results_of_check:
                json_return = {}

                rs_person = session_sql.query(Person).filter(Person.PERSON_ID == getattr(row, 'PERSON_ID')).first()
                json_return['PERSON_ID'] = int(getattr(rs_person, 'PERSON_ID'))
                json_return['PERSON_ID_NUMBER'] = getattr(rs_person, 'PERSON_ID_NUMBER')
                json_return['PERSON_FULL_NAME'] = get_full_name(
                    getattr(rs_person, 'PERSON_LAST_NAME'),
                    getattr(rs_person, 'PERSON_MIDLE_NAME'),
                    getattr(rs_person, 'PERSON_FIRST_NAME')
                )
                json_return['TIME'] = getattr(row, 'TIME').strftime("%H:%M:%S")
                json_return['SESSION_NAME'] = getattr(row, 'SESSION_NAME')
                json_return['SESSION_NAME_EN'] = getattr(row, 'SESSION_NAME_EN')
                json_return['SESSION_STATUS_NAME'] = getattr(row, 'SESSION_STATUS_NAME')
                json_return['SESSION_STATUS_NAME_EN'] = getattr(row, 'SESSION_STATUS_NAME_EN')
                json_return['SESSION_IMAGE_BASE64'] = getattr(row, 'SESSION_IMAGE_BASE64').decode("utf-8")
                json_return['USED_STATUS_NAME'] = getattr(row, 'USED_STATUS_NAME')
                array_return.append(json_return)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
    session_sql.close()
    return array_return

def get_json_all_check_out():
    # 1 check in morning
    # 2 check in afternoon
    # 3 check in evening
    session_sql = SessionSql()
    array_return = []
    try:
        date = datetime.datetime.today().strftime('%Y-%d-%m')
        results_of_check = session_sql.query(Person_Check_Out).filter(
            # Person_Check_In.PERSON_ID == person_id,
            Person_Check_In.DATE == date,
            Person_Check_In.USED_STATUS == 1
        ).all()
        if results_of_check is not None and len(results_of_check) > 0:
            for row in results_of_check:
                json_return = {}

                rs_person = session_sql.query(Person).filter(Person.PERSON_ID == getattr(row, 'PERSON_ID')).first()
                json_return['PERSON_ID'] = int(getattr(rs_person, 'PERSON_ID'))
                json_return['PERSON_ID_NUMBER'] = getattr(rs_person, 'PERSON_ID_NUMBER')
                json_return['PERSON_FULL_NAME'] = get_full_name(
                    getattr(rs_person, 'PERSON_LAST_NAME'),
                    getattr(rs_person, 'PERSON_MIDLE_NAME'),
                    getattr(rs_person, 'PERSON_FIRST_NAME')
                )
                json_return['TIME'] = getattr(row, 'TIME').strftime("%H:%M:%S")
                json_return['SESSION_NAME'] = getattr(row, 'SESSION_NAME')
                json_return['SESSION_NAME_EN'] = getattr(row, 'SESSION_NAME_EN')
                json_return['SESSION_STATUS_NAME'] = getattr(row, 'SESSION_STATUS_NAME')
                json_return['SESSION_STATUS_NAME_EN'] = getattr(row, 'SESSION_STATUS_NAME_EN')
                json_return['SESSION_IMAGE_BASE64'] = getattr(row, 'SESSION_IMAGE_BASE64').decode("utf-8")
                json_return['USED_STATUS_NAME'] = getattr(row, 'USED_STATUS_NAME')
                array_return.append(json_return)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
    session_sql.close()
    return array_return


def get_full_name(last, middle, first):
    if middle is not None or middle != '':
        full_name = last + ' ' + middle + ' ' + first
    else:
        full_name = last + ' ' + first

    return str(full_name)


def data_person_label_embedding():
    session_sql = SessionSql()
    all_persons = session_sql.query(Person, Person_EMB).filter(Person.USED_STATUS == 1,
                                                               Person.PERSON_ID == Person_EMB.PERSON_ID).all()
    array_return = []
    for row in all_persons:
        row_person = row[0]
        row_person_emb = row[1]
        json_return = {
            'PERSON_ID': getattr(row_person, 'PERSON_ID'),
            'PERSON_ID_NUMBER': getattr(row_person, 'PERSON_ID_NUMBER'),
            'FULL_NAME': get_full_name(
                getattr(row_person, 'PERSON_LAST_NAME'),
                getattr(row_person, 'PERSON_MIDLE_NAME'),
                getattr(row_person, 'PERSON_FIRST_NAME')
            ),
            'PERSON_EMB': np.frombuffer(getattr(row_person_emb, 'PERSON_EMB_BASE64'), dtype="float32")
        }
        array_return.append(json_return)
    session_sql.close()
    return array_return

def get_list_of_usets():
    session_sql = SessionSql()
    result_users = session_sql.query(Person, Person_EMB).filter(
        Person.PERSON_ID == Person_EMB.PERSON_ID,
        Person.USED_STATUS == 1,
        Person_EMB.USED_STATUS == 1
    ).all()
    array_return = []
    if len(result_users) > 0:
        for person, person_emb in result_users:
            json_return = {}
            json_return['PERSON_ID_NUMBER'] = getattr(person, "PERSON_ID_NUMBER")
            json_return['PERSON_FULL_NAME'] = get_full_name(
                getattr(person, "PERSON_LAST_NAME"),
                getattr(person, "PERSON_MIDDLE_NAME"),
                getattr(person, "PERSON_FIRST_NAME")
            )
            json_return['PERSON_IMAGE_BASE64'] = getattr(person_emb, "PERSON_IMAGE_BASE64")

            array_return.append(json_return)
    session_sql.closr()
    return array_return


# data_attendances_date_auto_for_day()
#
# print(return_date_today_attendance(date_today))
