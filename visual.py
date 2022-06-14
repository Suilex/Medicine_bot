from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px

from process_data import ProcessData


class Visual:
    def __init__(self):
        pass

    def plot_disease_and_sex_by_date(self, date_from=datetime.now(), date_to=datetime.now()):
        list_of_disease_by_sex = ProcessData().get_disease_and_sex_by_date(date_from=date_from, date_to=date_to)
        list_of_sex, list_of_diseases, list_of_count = [], [], []

        for sex, disease, count in list_of_disease_by_sex:
            list_of_sex.append(sex)
            list_of_diseases.append(disease)
            list_of_count.append(count)

        df = pd.DataFrame({'sex': list_of_sex, 'disease': list_of_diseases, 'count': list_of_count})

        fig = px.bar(df, x="disease", y="count", color="sex",
                     labels={
                         "disease": "Заболевание",
                         "count": "Количество",
                         "sex": "Пол"
                     },
                     barmode='group', title="Распределение болезней по полу")
        fig.show()

    def plot_disease_and_city_by_date(self, date_from=datetime.now(), date_to=datetime.now()):
        list_of_disease_by_city = ProcessData().get_disease_and_city_by_date(date_from=date_from, date_to=date_to)
        list_of_cities, list_of_diseases, list_of_count = [], [], []

        for city, disease, count in list_of_disease_by_city:
            list_of_cities.append(city)
            list_of_diseases.append(disease)
            list_of_count.append(count)

        df = pd.DataFrame({'city': list_of_cities, 'disease': list_of_diseases, 'count': list_of_count})

        fig = px.bar(df, x="disease", y="count", color="city",
                     labels={
                         "disease": "Заболевание",
                         "count": "Количество",
                         "city": "Город"
                     },
                     barmode='group', title="Распределение болезней по городам")
        fig.show()

    def plot_dob_by_disease(self, disease):
        list_of_dob_by_disease = ProcessData().get_dob_by_disease(disease)
        list_of_dob, list_of_diseases, list_of_count = [], [], []

        for dob, disease, count in list_of_dob_by_disease:
            list_of_dob.append(datetime.strftime(dob, '%Y'))
            list_of_diseases.append(disease)
            list_of_count.append(count)

        df = pd.DataFrame({'dob': list_of_dob, 'disease': list_of_diseases, 'count': list_of_count})

        fig = px.bar(df, x="disease", y="count", color="dob",
                     labels={
                         "disease": "Заболевание",
                         "count": "Количество",
                         "dob": "Год рождения"
                     },
                     barmode='group', title="Распределение болезней по году рождения")
        fig.show()


Visual().plot_disease_and_sex_by_date(date_from=datetime.now() - timedelta(4),
                                      date_to=datetime.today())
Visual().plot_disease_and_city_by_date(date_from=datetime.now() - timedelta(4),
                                       date_to=datetime.today())
Visual().plot_dob_by_disease('орви')
