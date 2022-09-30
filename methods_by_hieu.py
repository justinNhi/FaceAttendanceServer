"""
Cac phuong thuc co trong file nay:
******
    get_personal_profile_data(): lay du lieu ho so ca nhan
******
    data_history(*args): lay du lieu lich su check-in, check-out
        1 tham so se tu check date hoac main_year
        2 tham so theo thu tu main_year -> main_month
*****
"""

import datetime
import os
import sys

from new_data_models import Person, Person_Check, SessionSql, get_full_name


def get_personal_profile_data():
    session_sql = SessionSql()
    rs_personal = session_sql.query(Person).filter(
        Person.USED_STATUS != 0).all()
    data = {}
    if len(rs_personal) > 0:
        for row in rs_personal:
            json_profile = {}
            json_profile['full_name'] = get_full_name(
                getattr(row, 'PERSON_LAST_NAME'),
                getattr(row, 'PERSON_MIDDLE_NAME'),
                getattr(row, 'PERSON_FIRST_NAME')
            )
            json_profile['PERSON_ID'] = getattr(row, 'PERSON_ID')
            json_profile['PERSON_ID_NUMBER'] = getattr(
                row, 'PERSON_ID_NUMBER')
            json_profile['PERSON_ID_STAFF'] = getattr(
                row, 'PERSON_ID_STAFF')
            json_profile['PERSON_TYPE_ID'] = getattr(
                row, 'PERSON_TYPE_ID')
            json_profile['PERSON_TYPE_NAME'] = getattr(
                row, 'PERSON_TYPE_NAME')
            json_profile['PERSON_ADDRESS'] = getattr(
                row, 'PERSON_ADDRESS')
            json_profile['PERSON_GENDER'] = getattr(
                row, 'PERSON_GENDER')
            json_profile['PERSON_EMAIL'] = getattr(
                row, 'PERSON_EMAIL')
            json_profile['PERSON_PHONENUMBER_1'] = getattr(
                row, 'PERSON_PHONENUMBER_1')
            json_profile['PERSON_PHONENUMBER_2'] = getattr(
                row, 'PERSON_PHONENUMBER_2')
            json_profile['PERSON_DOB'] = getattr(row, 'PERSON_DOB')
            json_profile['PERSON_POB'] = getattr(row, 'PERSON_POB')
            json_profile['PERSON_IMAGE_BASE64'] = getattr(
                row, 'PERSON_IMAGE_BASE64').decode("utf-8")
            json_profile['PERSON_EMAIL'] = getattr(row, 'PERSON_EMAIL')
            json_profile['ID_NUMBER'] = getattr(row, 'ID_NUMBER')
            json_profile['USED_STATUS'] = getattr(row, 'USED_STATUS')
            json_profile['USED_STATUS_NAME'] = getattr(
                row, 'USED_STATUS_NAME')
            json_profile['USED_STATUS_NAME'] = getattr(
                row, 'USED_STATUS_NAME')
            json_profile['USED_STATUS_NAME'] = getattr(
                row, 'USED_STATUS_NAME')

            data.update({json_profile['PERSON_ID']: json_profile})
    session_sql.close()
    return data


def get_data_history(*args):
    data_personal_profile = get_personal_profile_data()
    """
    1 tham so se tu check date hoac main_year
    2 tham so theo thu tu main_year -> main_month
    """
    session_sql = SessionSql()
    data_json = []
    if len(args) == 1:
        check_input_date = args[0]
        print('check_input_date', check_input_date)
        if type(check_input_date) != datetime.datetime:
            try:
                date = datetime.datetime.strptime(check_input_date, "%Y-%m-%d")
                # month = date.month
                # year = date.year
                rs_check = session_sql.query(Person_Check).filter(
                    Person_Check.DATE == date,
                    Person_Check.USED_STATUS != 0).all()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(e, exc_type, fname, exc_tb.tb_lineno)
                year = check_input_date # convert to datetime fail will enter to year
                rs_check = session_sql.query(Person_Check).filter(
                    Person_Check.MAIN_YEAR == year,
                    Person_Check.USED_STATUS != 0).all()
        else:
            # year = check.year
            # month = check.month
            date = check_input_date # is datetime format
            rs_check = session_sql.query(Person_Check).filter(
                Person_Check.DATE == date,
                Person_Check.USED_STATUS != 0).all()
    else:
        year = args[1]
        month = args[0]
        rs_check = session_sql.query(Person_Check).filter(
            Person_Check.MAIN_MONTH == month,
            Person_Check.MAIN_YEAR == year,
            Person_Check.USED_STATUS != 0).all()
    if len(rs_check) > 0:
        for row in rs_check:
            json_check = {}
            json_check['DATETIME'] = getattr(row, 'DATETIME')
            json_check['SESSION_CHECK_ID'] = getattr(
                row, 'SESSION_CHECK_ID')
            json_check['SESSION_CHECK_NAME'] = getattr(
                row, 'SESSION_CHECK_NAME')
            json_check['SESSION_CHECK_NAME_EN'] = getattr(
                row, 'SESSION_CHECK_NAME_EN')
            json_check['DATE'] = getattr(row, 'DATE').strftime("%d/%m/%Y")
            json_check['TIME'] = getattr(row, 'TIME').strftime("%H:%M:%S")
            json_check['UNTIL_NOW'] = (
                getattr(row, 'DATETIME') - datetime.datetime.now()).days
            json_check['SESSION_ID'] = getattr(row, 'SESSION_ID')
            json_check['SESSION_NAME'] = getattr(row, 'SESSION_NAME')
            json_check['SESSION_NAME_EN'] = getattr(row, 'SESSION_NAME_EN')
            json_check['SESSION_STATUS_NAME'] = getattr(
                row, 'SESSION_STATUS_NAME')
            json_check['SESSION_STATUS_NAME_EN'] = getattr(
                row, 'SESSION_STATUS_NAME_EN')
            json_check['SESSION_IMAGE_BASE64'] = getattr(
                row, 'SESSION_IMAGE_BASE64').decode('utf-8')
            person_id = getattr(row, 'PERSON_ID')
            json_profile = data_personal_profile[person_id]
            json_check['profile'] = json_profile
            data_json.append(json_check)

    session_sql.close()
    return data_json


# if __name__ == "__main__":
#     data_personal_profile = get_personal_profile_data()
#     data_history = data_history("2022", "6")
