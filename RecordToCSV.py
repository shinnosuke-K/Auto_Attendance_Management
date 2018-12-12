# -*- coding: utf-8 -*-

import csv


def read_csv(filename):
    f = open(filename, 'r')
    csv_data = csv.reader(f)
    data_list = [e for e in csv_data]
    f.close()
    return data_list


if __name__ == '__main__':
    data = read_csv('Computer_configuration_theory.csv')
    print(data)