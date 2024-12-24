from src.db.config import db_ctrl_params, db_app_params
from src.db.connectionController import Connection



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
    def __init__(self, restart = False):
        self.ctrl_conn = Connection(db_ctrl_params, True)
        self.app_conn = Connection(db_app_params, True)

        if restart:
            self.dropSchema()
            self.init_db()



    def init_db(self):
        self.createSchema()
        self.createTables()
        self.initExampleData()

    def createSchema(self):
        with self.ctrl_conn.get_cursor() as cursor:
            cursor.execute("call init.create_schema()")

    def createTables(self):
        with self.ctrl_conn.get_cursor() as cursor:
            cursor.execute("call init.create_tables()")
            cursor.execute("call init.create_trigger()")



    def initExampleData(self):
        with self.ctrl_conn.get_cursor() as cursor:
            try:
                cursor.execute("call init.insert_russian_regions()")
                cursor.execute("call init.insert_russian_postcodes()")
                cursor.execute("call init.insert_santas()")
                cursor.execute("call init.add_child_letters()")
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
                cursor.execute("CALL func.add_letter(%s, %s, %s)", (child_id, topic, desc))
                return True
            except Exception as e:
                print(e.diag.message_primary)
                return False

    def getChildById(self, child_id):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.get_child_by_id_without_password", (child_id,))
                return child_from_raw(cursor.fetchone())
            except Exception as e:
                print(e.diag.message_primary)

    def getLettersByChildAndTopic(self, child_id, topic):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.get_letters_by_child_and_topic", (child_id,topic))
                return [letter_from_raw(data) for data in cursor.fetchall()]
            except Exception as e:
                print(e.diag.message_primary)
    def getLettersByChildAndYear(self, child_id, year):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.get_letters_by_child_and_year", (child_id, year))
                return [letter_from_raw(data) for data in cursor.fetchall()]
            except Exception as e:
                print(e.diag.message_primary)

    def deleteChild(self, child_id):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.execute("CALL func.delete_child(%s)", (child_id, ))
            except Exception as e:
                print(e.diag.message_primary)

    def deleteLetter(self, author_id, year):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.execute("CALL func.delete_letter(%s, %s)", (author_id, year))
            except Exception as e:
                print(e.diag.message_primary)

    def deleteLettersByChildAndTopic(self, author_id, topic):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.execute("CALL func.delete_letters_by_child_and_topic(%s, %s)", (author_id, topic))
            except Exception as e:
                print(e.diag.message_primary)

    def deleteLetterByChildAndYear(self, author_id, year):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.execute("CALL func.delete_letters_by_child_and_year(%s, %s)", (author_id, year))
            except Exception as e:
                print(e.diag.message_primary)

    def getLettersBySanta(self, santa_id):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.get_letters_by_santa", (santa_id,))
                return [letter_from_raw(data) for data in cursor.fetchall()]
            except Exception as e:
                print(e.diag.message_primary)

    def getLettersBySantaNickname(self, nickname):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.get_letters_by_santa_nickname", (nickname,))
                return [letter_from_raw(data) for data in cursor.fetchall()]
            except Exception as e:
                print(e.diag.message_primary)

    def getCurrentLettersBySantaNickname(self, nickname):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.get_current_letters_by_santa_nickname", (nickname,))
                return [letter_from_raw(data) for data in cursor.fetchall()]
            except Exception as e:
                print(e.diag.message_primary)

    def getRegionBySantaNickname(self, nickname):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.callproc("func.get_region_by_santa", (nickname,))
                return cursor.fetchone()[0]
            except Exception as e:
                print(e.diag.message_primary)

    def registerChild(self, birth_certificate, password, full_name, birth_date, postcode):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.execute("CALL func.register_child(%s, %s, %s, %s, %s)", (birth_certificate, password, full_name, birth_date, postcode))
                return True
            except Exception as e:
                print(e.diag.message_primary)
                return False

    def updateLetter(self, author_id, year, new_topic, new_desc):
        with self.app_conn.get_cursor() as cursor:
            try:
                cursor.execute("CALL func.update_letter(%s, %s, %s, %s)", (author_id, year, new_topic, new_desc))
            except Exception as e:
                print(e.diag.message_primary)

