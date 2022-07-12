import base64
import datetime
import io
import os
import random
import sys

import numpy as np
import unidecode as unidecode
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

Person_Check = Base.classes.PERSON_CHECK
Person_Check_columns = Person_Check.__table__.columns.keys()

Person_Account = Base.classes.PERSON_ACCOUNT
Person_Account_columns = Person_Account.__table__.columns.keys()

from datetime import date, timedelta, datetime

def get_full_name(last, middle, first):
    if middle is not None or middle != '':
        full_name = last + ' ' + middle + ' ' + first
    else:
        full_name = last + ' ' + first

    return str(full_name)


def auto_create_account():
    session_sql = SessionSql()

    rs_person = session_sql.query(Person).filter(
        Person.USED_STATUS != 0
    ).all()

    if len(rs_person) > 0:
        for row_rs_person in rs_person:
            person_full_name = get_full_name(
                getattr(row_rs_person, 'PERSON_LAST_NAME'),
                getattr(row_rs_person, 'PERSON_MIDDLE_NAME'),
                getattr(row_rs_person, 'PERSON_FIRST_NAME'),
            )
            unaccented_string = unidecode.unidecode(person_full_name)
            person_full_name_lower = ''.join(unaccented_string.lower().strip().split(' '))
            json_insert = {
                'PERSON_ID': getattr(row_rs_person, 'PERSON_ID'),
                'PERSON_ACCOUNT_NAME': person_full_name_lower,
                'PERSON_PASSWORD': base64.b64encode(bytes(person_full_name_lower + '24a3posct', 'utf-8')),
                'ACCOUNT_TYPE_ID': 1,
                'ACCOUNT_TYPE_NAME': 'Chuyên Viên',
                'ACCOUNT_TYPE_NAME_EN': 'Officer',
                'ACCOUNT_TOKEN':  base64.b64encode(bytes('OFFICERPOSCT', 'utf-8')),
                'ACCOUNT_CREATE_DATE': datetime.now(),
                'USED_STATUS': 2,
                'USED_STATUS_NAME': 'CREATE BY DEVELOPER',

            }

            # session_sql.add(Person_Account(**json_insert))
            # session_sql.commit()
            # print(json_insert)

            # passw = json_insert['PERSON_PASSWORD'].decode('utf-8')
            # print(base64.b64decode(passw).decode('utf-8'))








    session_sql.close()

    return 1

def auto_create_function():
    session_sql = SessionSql()

    rs_person = session_sql.query(Person_Account).filter(
        Person.USED_STATUS != 0
    ).all()

    if len(rs_person) > 0:
        for row_rs_person in rs_person:
            person_full_name = get_full_name(
                getattr(row_rs_person, 'PERSON_LAST_NAME'),
                getattr(row_rs_person, 'PERSON_MIDDLE_NAME'),
                getattr(row_rs_person, 'PERSON_FIRST_NAME'),
            )
            unaccented_string = unidecode.unidecode(person_full_name)
            person_full_name_lower = ''.join(unaccented_string.lower().strip().split(' '))
            json_insert = {
                'PERSON_ID': getattr(row_rs_person, 'PERSON_ID'),
                'PERSON_ACCOUNT_NAME': person_full_name_lower,
                'PERSON_PASSWORD': base64.b64encode(bytes(person_full_name_lower + '24a3posct', 'utf-8')),
                'ACCOUNT_TYPE_ID': 1,
                'ACCOUNT_TYPE_NAME': 'Chuyên Viên',
                'ACCOUNT_TYPE_NAME_EN': 'Officer',
                'ACCOUNT_TOKEN':  base64.b64encode(bytes('OFFICERPOSCT', 'utf-8')),
                'ACCOUNT_CREATE_DATE': datetime.now(),
                'USED_STATUS': 2,
                'USED_STATUS_NAME': 'CREATE BY DEVELOPER',

            }

            # session_sql.add(Person_Account(**json_insert))
            # session_sql.commit()
            # print(json_insert)

            # passw = json_insert['PERSON_PASSWORD'].decode('utf-8')
            # print(base64.b64decode(passw).decode('utf-8'))








    session_sql.close()

    return 1


if __name__ == "__main__":
    auto_create_account()

