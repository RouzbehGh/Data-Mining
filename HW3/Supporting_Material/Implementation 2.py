import pandas as pd
from typing import List
import numpy as np


def csv_to_arff(csv_file_name: str, arff_file_name: str, title: str) -> None:
    """Writes the arff file from the csv entered"""
    data_frame = pd.read_csv(csv_file_name)
    arff_list = df_to_arff(data_frame, title)
    with open(arff_file_name, "w") as arrf_file:
        for line in arff_list:
            arrf_file.write(f"{line}\n")


def df_to_arff(data_frame: pd.DataFrame, title: str) -> List[str]:
    header = df_to_arff_header(data_frame, title)
    header.append("")
    data = df_to_arff_data(data_frame)
    for instance in data:
        header.append(instance)
    return header


def df_to_arff_data(df: pd.DataFrame) -> List[str]:
    """Returns the lists of lines corresponding to the data part of the
    arff file"""
    result = ["@data"]
    for row in range(df.shape[0]):
        instance = df.iloc[row]
        list_instance = instance.tolist()
        str_list_instance = list(map(str, list_instance))
        str_instance = ",".join(str_list_instance)
        result.append(str_instance)
    return result


def df_to_arff_header(df: pd.DataFrame, title: str) -> List[str]:
    """Returns the list of lines corresponding to the header part of the
    arff file"""
    result = [f"@relation {title}", ""]
    attributes = df.columns
    types = df.dtypes
    for att, type in zip(attributes, types):
        unique_values_att: any
        if np.issubdtype(type, np.number):
            unique_values_att = "NUMERICAL"
        elif "datetime64" == type:
            unique_values_att = "DATE-TIME"
        else:
            unique_values_att = set(df[att].tolist())
        result.append(f"@attribute {att} {unique_values_att.__str__()}")

    return result


if '__main__' == __name__:
    csv_file_name = "heart.csv"
    arrf_file_name = "heart.arff"
    title = "Heart"
    csv_to_arff(csv_file_name, arrf_file_name, title)