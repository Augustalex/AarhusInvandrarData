import csv
import json
import numpy as np


def make_integer_value_node(label, value):
    return {'name': label, 'size': int(value)}


def make_parent_node(label, children):
    return {'name': label, 'children': children}


def country_node(country_name, age_rows, age_labels):
    """The age_rows is a 2d matrix containing data for
    each age in one row for each sex. That is, two rows
    and a column for each age group.
    The age_labels denotes the label for each age group (i.e.
    each column). """

    male_children = []
    female_children = []
    for i in range(len(age_labels)):
        male_children.append(make_integer_value_node(age_labels[i], age_rows[0][i]))
        female_children.append(make_integer_value_node(age_labels[i], age_rows[1][i]))

    male_node = make_parent_node('Male', male_children)
    female_node = make_parent_node('Female', female_children)
    return make_parent_node(country_name, [male_node, female_node])


def immigrant_csv_to_json(csv_file_path):
    file = open(csv_file_path, 'r')
    row_reader = csv.reader(file, delimiter=';')
    data = np.array([row for row in row_reader])

    age_group_labels = data[0, 2:]
    headerless_data = data[1:]

    _gender_groups_presplit = headerless_data[::, 2:]
    gender_groups = np.vsplit(_gender_groups_presplit, round(len(_gender_groups_presplit) / 2))
    countries = headerless_data[::2, 0]

    return [country_node(countries[i], gender_groups[i], age_group_labels) for i in range(len(countries))]


def dump_to_json(dictionary_data, file_name="data.json"):
    file_pointer = open(file_name, 'w')
    json.dump(immigrant_csv_to_json("data.csv"), file_pointer, ensure_ascii=False)


dump_to_json(immigrant_csv_to_json("data.csv"))



