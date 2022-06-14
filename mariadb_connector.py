import mariadb

from config import DB_NAME, SYMPTOMS_TABLE, USERS_TABLE, USER_STATES_TABLE, USER, PASSWORD, HOST, PORT


class MariadbConnector:
    def __init__(self):
        pass

    @staticmethod
    def to_connect():
        return mariadb.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT)

    def get_conn_and_cursor(self):
        conn = self.to_connect()
        cur = conn.cursor()
        cur.execute("use {}".format(DB_NAME))
        return conn, cur

    def insert_symptoms_to_db(self, symptoms, user_id, disease):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("insert into {} (symptoms, user_id, is_correct, disease) values ('{}', {}, true, '{}')".format(
            SYMPTOMS_TABLE, symptoms, user_id, disease))
        conn.commit()
        conn.close()

    def insert_predict_symptoms_to_db(self, symptoms, user_id, disease):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("insert into {} (symptoms, user_id, is_correct, disease) values ('{}', {}, false, '{}')".format(
            SYMPTOMS_TABLE, symptoms, user_id, disease))
        conn.commit()
        conn.close()

    def insert_new_user(self, date_of_birth, user_id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("insert into {} (date_of_birth, user_id) values ('{}', {})".format(
            USERS_TABLE, date_of_birth, user_id))
        conn.commit()
        conn.close()

    def insert_state(self, user_id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("insert into {} (user_id) values ({})".format(
            USER_STATES_TABLE, user_id))
        conn.commit()
        conn.close()

    def get_user_state(self, user_id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("select id from {} where user_id = {}".format(USER_STATES_TABLE, user_id))
        result = cur.fetchall()
        conn.close()
        return result

    def update_sex_user(self, user_id, sex):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("update {} set sex = '{}' where user_id = {}".format(
            USERS_TABLE, sex, user_id))
        conn.commit()
        conn.close()

    def update_city_user(self, user_id, city):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("update {} set city = '{}' where user_id = {}".format(
            USERS_TABLE, city, user_id))
        conn.commit()
        conn.close()

    def update_disease(self, disease, id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("update {} set disease = '{}', is_correct = true where id = {}".format(
            SYMPTOMS_TABLE, disease, id))
        conn.commit()
        conn.close()

    def update_assessment(self, id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("update {} set is_correct = true where id = {}".format(
            SYMPTOMS_TABLE, id))
        conn.commit()
        conn.close()

    def get_data_with_predict_disease(self, user_id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("select * from {} where user_id = {} and is_correct = false".format(SYMPTOMS_TABLE, user_id))
        result = cur.fetchall()
        conn.close()
        return result

    def get_all_correct_label_data(self):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("select * from {} where is_correct = true".format(SYMPTOMS_TABLE))
        result = cur.fetchall()
        conn.close()
        return result

    def get_all_data(self):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("select * from {}".format(SYMPTOMS_TABLE))
        result = cur.fetchall()
        conn.close()
        return result

    def set_current_comm_db(self, user_id, current_comm):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("update {} set current_comm = '{}' where user_id = {}".format(
            USER_STATES_TABLE, current_comm, user_id))
        conn.commit()
        conn.close()

    def set_current_state_db(self, user_id, current_state):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("update {} set current_state = {} where user_id = {}".format(
            USER_STATES_TABLE, current_state, user_id))
        conn.commit()
        conn.close()

    def set_symptoms_db(self, user_id, symptoms):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("update {} set symptoms = '{}' where user_id = {}".format(
            USER_STATES_TABLE, symptoms, user_id))
        conn.commit()
        conn.close()

    def set_disease_db(self, user_id, disease):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("update {} set disease = '{}' where user_id = {}".format(
            USER_STATES_TABLE, disease, user_id))
        conn.commit()
        conn.close()

    def set_number_of_block_db(self, user_id, number_of_block):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("update {} set number_of_block = {} where user_id = {}".format(
            USER_STATES_TABLE, number_of_block, user_id))
        conn.commit()
        conn.close()

    def set_number_of_row_db(self, user_id, number_of_row):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("update {} set number_of_row = '{}' where user_id = {}".format(
            USER_STATES_TABLE, number_of_row, user_id))
        conn.commit()
        conn.close()

    def set_amount_of_block_db(self, user_id, amount_of_block):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("update {} set amount_of_block = {} where user_id = {}".format(
            USER_STATES_TABLE, amount_of_block, user_id))
        conn.commit()
        conn.close()

    def get_current_comm_db(self, user_id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("select current_comm from {} where user_id = {}".format(USER_STATES_TABLE, user_id))
        result = cur.fetchall()
        conn.close()
        return result[0][0]

    def get_current_state_db(self, user_id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("select current_state from {} where user_id = {}".format(USER_STATES_TABLE, user_id))
        result = cur.fetchall()
        conn.close()
        return result[0][0]

    def get_symptoms_db(self, user_id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("select symptoms from {} where user_id = {}".format(USER_STATES_TABLE, user_id))
        result = cur.fetchall()
        conn.close()
        return result[0][0]

    def get_disease_db(self, user_id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("select disease from {} where user_id = {}".format(USER_STATES_TABLE, user_id))
        result = cur.fetchall()
        conn.close()
        return result[0][0]

    def get_number_of_block_db(self, user_id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("select number_of_block from {} where user_id = {}".format(USER_STATES_TABLE, user_id))
        result = cur.fetchall()
        conn.close()
        return result[0][0]

    def get_number_of_row_db(self, user_id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("select number_of_row from {} where user_id = {}".format(USER_STATES_TABLE, user_id))
        result = cur.fetchall()
        conn.close()
        return result[0][0]

    def get_amount_of_block_db(self, user_id):
        conn, cur = self.get_conn_and_cursor()
        cur.execute("select amount_of_block from {} where user_id = {}".format(USER_STATES_TABLE, user_id))
        result = cur.fetchall()
        conn.close()
        return result[0][0]

    def get_disease_and_sex_by_date(self, date_from, date_to):
        conn, cur = self.get_conn_and_cursor()
        cur.execute(
            "select a.sex, b.disease, count(b.disease) from {} as b join {} as a "
            "where a.user_id = b.user_id and b.created_at between '{}' and '{}' group by a.sex, b.disease".format(
                SYMPTOMS_TABLE, USERS_TABLE, date_from, date_to))
        result = cur.fetchall()
        conn.close()
        return result

    def get_disease_and_city_by_date(self, date_from, date_to):
        conn, cur = self.get_conn_and_cursor()
        cur.execute(
            "select a.city, b.disease, count(b.disease) from {} as b join {} as a "
            "where a.user_id = b.user_id and b.created_at between '{}' and '{}' group by a.city, b.disease".format(
                SYMPTOMS_TABLE, USERS_TABLE, date_from, date_to))
        result = cur.fetchall()
        conn.close()
        return result

    def get_dob_by_disease(self, disease):
        conn, cur = self.get_conn_and_cursor()
        cur.execute(
            "select a.date_of_birth, b.disease, count(b.disease) from {} as b join {} as a "
            "where a.user_id = b.user_id and b.disease = '{}' group by b.disease, a.date_of_birth".format(
                SYMPTOMS_TABLE, USERS_TABLE, disease))
        result = cur.fetchall()
        conn.close()
        return result
