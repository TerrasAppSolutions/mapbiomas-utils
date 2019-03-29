import insert_transition_postgres
import argparse
from functools import reduce


def send_to_postgres(path_json, idprefix = 0):
    data = insert_transition_postgres.get_data(path_json)
    data_formatted = insert_transition_postgres.format_data(data, idprefix)
    insert_transition_postgres.insert_postgres(data_formatted)

def biomas(path_folder, transition_years):
    for years_pair in transition_years:
        path_json = ""
        send_to_postgres(path_json)
