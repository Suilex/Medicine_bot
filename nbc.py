import os
import pickle

import nltk
import numpy as np
import pandas as pd
import pymorphy2
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from config import SEPARATE_SYMBOL
from process_data import ProcessData

nltk.download('stopwords')


class NaiveBayesClassifiers:
    def __init__(self):
        self.x = ''
        self.y = ''
        self.df = ''

    def predict(self, list_of_symptoms):
        list_of_symptoms = list(filter(None, list_of_symptoms))
        clean_predict_symptoms = list(set(self.clean_data(list_of_symptoms)))
        if not self.check_existing(clean_predict_symptoms):
            self.vectorize(clean_predict_symptoms)
            naive_bayes_model = self.naive_bayes_model()
        else:
            naive_bayes_model = self.get_naive_bayes_model()
        ids, length = self.get_list_of_ids_and_len_of_matrix(clean_predict_symptoms)
        prediction = self.get_prediction(naive_bayes_model, self.get_matrix_form(ids, length))
        return prediction[0]

    def check_existing(self, clean_predict_symptoms):
        list_of_tokens = self.get_tokens()
        for elem in clean_predict_symptoms:
            if elem not in list_of_tokens:
                return False
        else:
            return True

    def get_list_of_ids_and_len_of_matrix(self, clean_predict_symptoms):
        list_of_tokens = self.get_tokens()
        ids = []
        for elem in clean_predict_symptoms:
            ids.append(np.where(list_of_tokens == elem)[0][0])

        return ids, len(list_of_tokens)

    def get_all_correct_label_data(self, clean_predict_symptoms):
        data = ProcessData().get_all_correct_label_data()
        symptoms, disease = [], []
        for elem in data:
            list_of_symptoms = elem[1].split(SEPARATE_SYMBOL)
            clean_list_of_words = self.clean_data(list_of_symptoms)
            symptoms.append(' '.join(list(set(clean_list_of_words))))
            disease.append(elem[3])
        symptoms.append(' '.join(list(set(clean_predict_symptoms))))
        disease.append('None')
        self.df = pd.DataFrame(data={'symptoms': symptoms, 'disease': disease})

    def vectorize(self, clean_predict_symptoms):
        self.get_all_correct_label_data(clean_predict_symptoms)

        vectorizer = CountVectorizer()
        vectorizer_full_train_data = vectorizer.fit_transform(self.df['symptoms']).toarray()

        self.x = vectorizer_full_train_data[:-1]
        self.y = self.df['disease'][:-1]

        self.save_tokens(vectorizer.get_feature_names_out())

    def save_tokens(self, tokens):
        if not os.path.exists('nbc'):
            os.mkdir("nbc")
        with open('nbc/tokens.pkl', 'wb') as f:
            pickle.dump(tokens, f)

    def get_tokens(self):
        if os.path.exists('nbc/tokens.pkl'):
            with open('nbc/tokens.pkl', 'rb') as f:
                list_of_tokens = pickle.load(f)
            return list_of_tokens
        return []

    def naive_bayes_model(self):
        nb_classifier = MultinomialNB()
        nb_classifier.fit(self.x, self.y)
        self.save_naive_bayes_model(nb_classifier)

        return nb_classifier

    def save_naive_bayes_model(self, nb_classifier):
        if not os.path.exists('nbc'):
            os.mkdir("nbc")
        with open('nbc/naive_bayes_model.pkl', 'wb') as f:
            pickle.dump(nb_classifier, f)

    def get_prediction(self, nb_classifier, predict_matrix_of_symptoms):
        y_test_prediction = nb_classifier.predict([predict_matrix_of_symptoms])
        return y_test_prediction

    def get_naive_bayes_model(self):
        with open('nbc/naive_bayes_model.pkl', 'rb') as f:
            nb_classifier = pickle.load(f)
        return nb_classifier

    def clean_data(self, list_of_symptoms):
        morph = pymorphy2.MorphAnalyzer()
        clean_list_of_words = []
        for symptom in list_of_symptoms:
            if len(symptom.split(' ')) > 1:
                for word in symptom.split(' '):
                    if word not in stopwords.words('russian'):
                        phrase = morph.parse(word)[0]
                        clean_list_of_words.append(phrase.normal_form)
            else:
                if symptom not in stopwords.words('russian'):
                    phrase = morph.parse(symptom)[0]
                    clean_list_of_words.append(phrase.normal_form)
        return clean_list_of_words

    def get_matrix_form(self, ids, length):
        matrix = []
        for i in range(length):
            if i in ids:
                matrix.append(1)
            else:
                matrix.append(0)
        return matrix
