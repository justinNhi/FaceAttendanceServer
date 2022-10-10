import base64
import datetime
import io
import os
import random
import sys

import numpy as np
from PIL import Image
from sqlalchemy import create_engine, func, desc, distinct
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

Account_Function = Base.classes.ACCOUNT_FUNCTION
Account_Function_columns = Account_Function.__table__.columns.keys()

from datetime import date, timedelta, datetime


def get_full_name(last, middle, first):
    if middle is not None or middle != '':
        full_name = last + ' ' + middle + ' ' + first
    else:
        full_name = last + ' ' + first

    return str(full_name)


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


def get_person(person_id):
    session_sql = SessionSql()
    rs_person = session_sql.query(Person).filter(
        Person.USED_STATUS != 0,
        Person.PERSON_ID == person_id
    ).first()
    json_person = {}
    if rs_person is not None:
        json_person = {
            'PERSON_ID': str(getattr(rs_person, "PERSON_ID")),
            'PERSON_ID_NUMBER': getattr(rs_person, "PERSON_ID_NUMBER"),
            'PERSON_FULL_NAME': get_full_name(
                getattr(rs_person, "PERSON_LAST_NAME"),
                getattr(rs_person, "PERSON_MIDDLE_NAME"),
                getattr(rs_person, "PERSON_FIRST_NAME"),
            ),
            'PERSON_IMAGE_BASE64': getattr(rs_person, "PERSON_IMAGE_BASE64").decode("utf-8"),
        }
    session_sql.close()
    return json_person


def get_account_function(person_id):
    session_sql = SessionSql()
    rs_account_functions = session_sql.query(
        Account_Function.FUNCTION_ID
    ).filter(
        Account_Function.USED_STATUS != 0,
        Account_Function.PERSON_ID == person_id,
    ).all()

    # filter by user != 0 and by person id

    array_functions = []
    set_function_ids = []  # set of id

    if len(rs_account_functions) > 0:  # loop for set of id
        for row in rs_account_functions:
            set_function_ids.append(row.FUNCTION_ID)
    set_function_ids = set(set_function_ids)

    for function_id in set_function_ids:
        rs_account_functions = session_sql.query(Account_Function).filter(
            Account_Function.USED_STATUS != 0,
            Account_Function.PERSON_ID == person_id,
            Account_Function.FUNCTION_ID == function_id,
        )

        json_function = {
            "FUNCTION_ID": str(function_id),
            "FUNCTION_NAME": getattr(rs_account_functions.first(), 'FUNCTION_NAME'),
            "FUNCTION_URL": str(getattr(rs_account_functions.first(), 'FUNCTION_URL')),
            "FUNCTION_SEGMENT": getattr(rs_account_functions.first(), 'FUNCTION_SEGMENT'),
            "FUNCTION_ICON": str(getattr(rs_account_functions.first(), 'FUNCTION_ICON')),
            "FUNCTION_NOTE": getattr(rs_account_functions.first(), 'FUNCTION_NOTE'),
            "FUNCTION_INCLUDE_CHILDREN": str(getattr(rs_account_functions.first(), 'FUNCTION_INCLUDE_CHILDREN')),
        }
        # function of parent

        array_functions_children = []
        if int(getattr(rs_account_functions.first(), 'FUNCTION_INCLUDE_CHILDREN')) != 0:
            for row_rs_account_functions in rs_account_functions.all():
                json_function_child = {
                    "FUNCTION_CHILD_ID": str(getattr(row_rs_account_functions, 'FUNCTION_CHILD_ID')),
                    "FUNCTION_CHILD_NAME": getattr(row_rs_account_functions, 'FUNCTION_CHILD_NAME'),
                    "FUNCTION_CHILD_URL": str(getattr(row_rs_account_functions, 'FUNCTION_CHILD_URL')),
                    "FUNCTION_CHILD_ICON": str(getattr(row_rs_account_functions, 'FUNCTION_CHILD_ICON')),
                    "FUNCTION_CHILD_SEGMENT": getattr(row_rs_account_functions, 'FUNCTION_CHILD_SEGMENT'),
                    "FUNCTION_CHILD_NOTE": getattr(row_rs_account_functions, 'FUNCTION_CHILD_NOTE'),

                }
                array_functions_children.append(json_function_child)
            json_function['functions_children'] = array_functions_children
        array_functions.append(json_function)
        # children functions

        print(array_functions)
    session_sql.close()
    return array_functions


def check_account_log_in(account_name = None, account_password = None):
    session_sql = SessionSql()
    if account_name is not None and account_password is not None:
        account_password_base64 = base64.b64encode(bytes(account_password, 'utf-8'))
        rs_person_account = session_sql.query(Person_Account).filter(
            Person_Account.USED_STATUS != 0,
            Person_Account.PERSON_ACCOUNT_NAME == account_name,
            Person_Account.PERSON_PASSWORD == account_password_base64,
        ).first()
        json_person_account = {}
        if rs_person_account is not None:
            json_person_account = {
                'PERSON': get_person(getattr(rs_person_account, 'PERSON_ID')),
                'ACCOUNT_TYPE_ID': str(getattr(rs_person_account, 'ACCOUNT_TYPE_ID')),
                'ACCOUNT_TYPE_NAME': getattr(rs_person_account, 'ACCOUNT_TYPE_NAME'),
                'ACCOUNT_TYPE_NAME_EN': getattr(rs_person_account, 'ACCOUNT_TYPE_NAME_EN'),
                'ACCOUNT_TOKEN': getattr(rs_person_account, 'ACCOUNT_TOKEN').decode('utf-8'),
                'FUNCTION': get_account_function(getattr(rs_person_account, 'PERSON_ID')),
            }
    else:
        json_person_account = {
            'PERSON': None,
            'ACCOUNT_TYPE_ID': None,
            'ACCOUNT_TYPE_NAME': None,
            'ACCOUNT_TYPE_NAME_EN': None,
            'ACCOUNT_TOKEN': None,
            'FUNCTION': None
        }
    print('FUNCTION', json_person_account["FUNCTION"])
    session_sql.close()
    return json_person_account

# if __name__ == "__main__":
#     rs_test = check_log_in('lehoangnhi', 'lehoangnhi24a3posct')
#
#     print(rs_test)

# for m in [1,2,3,4,5,6,7,8,9,10,11,12]:
#     test_insert_check_in_check_out(m, 2021)
# data = datetime.today()
# end_date = data + timedelta(days=2)
# print(end_date)
# print(data.weekday())
# print(end_date.weekday())
