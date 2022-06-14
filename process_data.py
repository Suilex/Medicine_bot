import re

from config import SEPARATE_SYMBOL
from mariadb_connector import MariadbConnector


class ProcessData:
    def __init__(self):
        pass

    @staticmethod
    def put_symptoms_to_db(symptoms_text, user_id, disease):
        symptoms_list = symptoms_text.split(',')
        clean_list = []
        for elem in symptoms_list:
            clean_list.append(re.sub("[^А-Яа-я ]", "", elem.strip()).lower().strip())
        clean_disease = re.sub("[^А-Яа-я ]", "", disease.strip()).lower()
        MariadbConnector().insert_symptoms_to_db('{}'.format(SEPARATE_SYMBOL).join(clean_list), user_id, clean_disease)

    @staticmethod
    def put_predict_symptoms_to_db(symptoms_text, user_id, disease):
        symptoms_list = symptoms_text.split(',')
        clean_list = []
        for elem in symptoms_list:
            clean_list.append(re.sub("[^А-Яа-я ]", "", elem.strip()).lower())
        clean_disease = re.sub("[^А-Яа-я ]", "", disease.strip()).lower()
        MariadbConnector().insert_predict_symptoms_to_db('{}'.format(SEPARATE_SYMBOL).join(clean_list), user_id,
                                                         clean_disease)

    @staticmethod
    def get_clear_symptoms(user_id):
        symptoms_list = ProcessData.get_symptoms(user_id).split(',')
        clean_list = []
        for elem in symptoms_list:
            clean_list.append(re.sub("[^А-Яа-я ]", "", elem.strip()).lower().strip())
        return clean_list

    @staticmethod
    def get_data_with_predict_disease(user_id):
        return MariadbConnector().get_data_with_predict_disease(user_id)

    @staticmethod
    def update_disease(disease, number_of_row, number_of_block):
        list_of_ids = number_of_row.split(SEPARATE_SYMBOL)
        MariadbConnector().update_disease(re.sub("[^А-Яа-я ]", "", disease.strip()).lower(),
                                          list_of_ids[int(number_of_block) - 1])

    @staticmethod
    def update_assessment(block_number, number_of_row):
        ids = number_of_row.split(SEPARATE_SYMBOL)[:-1]
        MariadbConnector().update_assessment(ids[block_number - 1])

    @staticmethod
    def create_new_user(user_id, date_of_birth):
        MariadbConnector().insert_new_user(user_id, date_of_birth)

    @staticmethod
    def create_user_state(user_id):
        if not MariadbConnector().get_user_state(user_id):
            MariadbConnector().insert_state(user_id)

    @staticmethod
    def update_sex_user(user_id, sex):
        MariadbConnector().update_sex_user(user_id, sex)

    @staticmethod
    def update_city_user(user_id, city):
        MariadbConnector().update_city_user(user_id, city)

    @staticmethod
    def get_all_correct_label_data():
        return MariadbConnector().get_all_correct_label_data()

    @staticmethod
    def get_disease_and_sex_by_date(date_from, date_to):
        return MariadbConnector().get_disease_and_sex_by_date(date_from, date_to)

    @staticmethod
    def get_disease_and_city_by_date(date_from, date_to):
        return MariadbConnector().get_disease_and_city_by_date(date_from, date_to)

    @staticmethod
    def get_dob_by_disease(disease):
        return MariadbConnector().get_dob_by_disease(disease)

    @staticmethod
    def set_current_comm(user_id, current_comm):
        MariadbConnector().set_current_comm_db(user_id, current_comm)

    @staticmethod
    def set_current_state(user_id, current_state):
        MariadbConnector().set_current_state_db(user_id, current_state)

    @staticmethod
    def set_symptoms(user_id, symptoms):
        MariadbConnector().set_symptoms_db(user_id, symptoms)

    @staticmethod
    def set_disease(user_id, disease):
        MariadbConnector().set_disease_db(user_id, disease)

    @staticmethod
    def set_number_of_block(user_id, number_of_block):
        MariadbConnector().set_number_of_block_db(user_id, number_of_block)

    @staticmethod
    def set_amount_of_block(user_id, number_of_block):
        MariadbConnector().set_amount_of_block_db(user_id, number_of_block)

    @staticmethod
    def set_number_of_row(user_id, number_of_row):
        MariadbConnector().set_number_of_row_db(user_id, number_of_row)

    @staticmethod
    def get_current_comm(user_id):
        return MariadbConnector().get_current_comm_db(user_id)

    @staticmethod
    def get_current_state(user_id):
        return MariadbConnector().get_current_state_db(user_id)

    @staticmethod
    def get_symptoms(user_id):
        return MariadbConnector().get_symptoms_db(user_id)

    @staticmethod
    def get_disease(user_id):
        return MariadbConnector().get_disease_db(user_id)

    @staticmethod
    def get_number_of_block(user_id):
        return MariadbConnector().get_number_of_block_db(user_id)

    @staticmethod
    def get_amount_of_block(user_id):
        return MariadbConnector().get_amount_of_block_db(user_id)

    @staticmethod
    def get_number_of_row(user_id):
        return MariadbConnector().get_number_of_row_db(user_id)
