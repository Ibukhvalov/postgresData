from traceback import print_exception

from config import db_ctrl_params, db_app_params
from connectionController import Connection


def child_from_raw(rawData):
    if len(rawData) != 6:
      print(f"ALARM AT {rawData}")
    return {
        "birth_certificate": rawData[0],
        "full_name": rawData[1],
        "birth_date": rawData[2],
        "postcode": rawData[3],
        "number_of_good_deeds": rawData[4],
        "number_of_misdeeds": rawData[5],
    }

def letter_from_raw(rawData):
    if len(rawData) != 4:
      print(f"ALARM AT {rawData}")
    return {
        "author_id": rawData[0],
        "year": rawData[1],
        "topic": rawData[2],
        "description": rawData[3]
    }

class DBController:
    def __init__(self):
        self.ctrl_conn = Connection(db_ctrl_params, True)
        self.app_conn = Connection(db_app_params, True)
        #self.drop_schema()
        self.init_db()
        #self.test()
        print(self.isChildLoggedIn('121212', 'huy')[0])

    def init_db(self):
        self.createSchema()
        self.createTables()
        self.initRussianData()

    def createSchema(self):
        with self.ctrl_conn.get_cursor() as cursor:
            cursor.execute("call init.create_schema()")

    def createTables(self):
        with self.ctrl_conn.get_cursor() as cursor:
            cursor.execute("call init.create_tables()")
            cursor.execute("call init.create_trigger()")

    def initRussianData(self):
        with self.ctrl_conn.get_cursor() as cursor:
            try:
                cursor.execute("call init.insert_russian_regions()")
                cursor.execute("call init.insert_russian_postcodes()")
                cursor.execute("call init.insert_santas()")
            except Exception as e:
                print("Error at initialization tables:", e.diag.message_primary)

    def dropSchema(self):
        with self.ctrl_conn.get_cursor() as cursor:
            cursor.execute("call init.drop_schema()")

    def isChildLoggedIn(self, login: str, password: str):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.child_login", (login, password))
                return cursor.fetchone()[0]
            except Exception as e:
                print(f"Error at log in child ({login}):", e.diag.message_primary)


    def isSantaLoggedIn(self, login: str, password: str):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.santa_login", (login, password))
                return cursor.fetchone()[0]
            except Exception as e:
                print(f"Error at adding santa ({login}):", e.diag.message_primary)

    def getCurrentLettersBySanta(self, santa_id):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.get_current_letters_by_santa", (santa_id,))
                return [letter_from_raw(data) for data in cursor.fetchall()]
            except Exception as e:
                print(f"Error at getting letters by santa ({santa_id}):", e.diag.message_primary)

    def getLettersByChild(self, child_id):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.get_letters_by_child", (child_id,))
                return [letter_from_raw(data) for data in cursor.fetchall()]
            except Exception as e:
                print(f"Error at getting letters by santa ({child_id}):", e.diag.message_primary)

    def addLetter(self, child_id, topic, desc):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.add_letter", (child_id, topic, desc))
            except Exception as e:
                print(e.diag.message_primary)

    def getChildById(self, child_id):
        with self.app_conn.get_cursor as cursor:
            try:
                cursor.callproc("func.get_child_by_id_without_password", (child_id,))
                return child_from_raw(cursor.fetchone())
            except Exception as e:
                print(e.diag.message_primary)

    def getLettersByChildAndTopic(self, child_id, topic):
        with self.app_conn.get_cursor as cursor:
            try:
                cursor.callproc("func.get_letters_by_child_and_topic", (child_id,topic))
                return [letter_from_raw(data) for data in cursor.fetchall()]
            except Exception as e:
                print(e.diag.message_primary)
    def getLettersByChildAndYear(self, child_id, year):
        with self.app_conn.get_cursor as cursor:
            try:
                cursor.callproc("func.get_letters_by_child_and_year", (child_id, year))
                return [letter_from_raw(data) for data in cursor.fetchall()]
            except Exception as e:
                print(e.diag.message_primary)

    def deleteChild(self, child_id):
        with self.app_conn.get_cursor as cursor:
            try:
                cursor.callproc("func.delete_child", (child_id,))
            except Exception as e:
                print(e.diag.message_primary)

    def deleteLetter(self, author_id, year):
        with self.app_conn.get_cursor as cursor:
            try:
                cursor.callproc("func.delete_letter", (author_id, year))
            except Exception as e:
                print(e.diag.message_primary)

    def deleteLettersByChildAndTopic(self, author_id, topic):
        with self.app_conn.get_cursor as cursor:
            try:
                cursor.callproc("func.delete_letter_by_child_and_topic", (author_id, topic))
            except Exception as e:
                print(e.diag.message_primary)

    def deleteLettersByChildAndYear(self, author_id, year):
        with self.app_conn.get_cursor as cursor:
            try:
                cursor.callproc("func.delete_letter_by_child_and_year", (author_id, year))
            except Exception as e:
                print(e.diag.message_primary)

    def getLettersBySanta(self, santa_id):
        with self.app_conn.get_cursor as cursor:
            try:
                cursor.callproc("func.get_letters_by_santa", (santa_id,))
                return [letter_from_raw(data) for data in cursor.fetchall()]
            except Exception as e:
                print(e.diag.message_primary)

    def registerChild(self, birth_certificate, password, full_name, birth_date, postcode):
        with self.app_conn.get_cursor as cursor:
            try:
                cursor.callproc("func.register_child", (birth_certificate, password, full_name, birth_date, postcode))
            except Exception as e:
                print(e.diag.message_primary)

    def updateLetter(self, author_id, year, new_topic, new_desc):
        with self.app_conn.get_cursor as cursor:
            try:
                cursor.callproc("func.update_letter", (author_id, year, new_topic, new_desc))
            except Exception as e:
                print(e.diag.message_primary)