from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

Base = automap_base()


engine = create_engine("mssql+pyodbc://sa:nhi874755@192.168.1.179/TEST_API_T_AID_ROBOT_AUTO_TAKE_IMAGES?driver=SQL+Server")

# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
# STUDENT_IMAGE_FOR_FR= Base.classes.WR_STUDENT
# STUDENT_IMAGE_FOR_FR_columns = STUDENT_IMAGE_FOR_FR.__table__.columns.keys()

STUDENT_IMAGES_AUTO_TAKE = Base.classes.STUDENT_IMAGES_AUTO_TAKE
STUDENT_IMAGES_AUTO_TAKE_columns = STUDENT_IMAGES_AUTO_TAKE.__table__.columns.keys()

WR_STUDENT = getattr(Base.classes,'WR_STUDENT')
WR_STUDENT_columns = ['STUDENT_ID_NUMBER', 'CURRENT_LAST_NAME', 'CURRENT_MIDDLE_NAME', 'CURRENT_FIRST_NAME']



def get_student_list():
