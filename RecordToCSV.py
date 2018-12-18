# -*- coding: utf-8 -*-

import pandas as pd


def read_csv():
    df = pd.read_csv('Computer_configuration_theory.csv', encoding='utf_8', index_col=0)
    return df

def input_csv(student_num, date_num, attendance):
