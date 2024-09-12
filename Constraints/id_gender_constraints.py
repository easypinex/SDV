import pandas as pd

from sdv.constraints import create_custom_constraint_class

import re

def replace_id(text, text2):
    return re.sub(r'\d', text2, text, count=1)


def is_valid(column_names, data):
    """
    Checks for the validity of the data for the given column names.
    
    Args:
        column_names(list[str]):
            A list of the column names involved in the constraint
        data(pandas.DataFrame):
            A dataaset

    Returns:
        pandas Series:
            A Series of True/False values describing whether the each row
            of the data is valid. There is exactly 1 True/False value for
            every row in the data.
    """

    id = column_names[0]
    gender = column_names[1]

    male = (data[gender] == '男') & (data[id].str.extract(r'(\d)', expand=False) == '1')
    female = (data[gender] == '女') & (data[id].str.extract(r'(\d)', expand=False) == '2')

    return male | female

def transform(column_names, data):
    """
    Transforms the data for the given column names. The transformed
    data will be given to the synthetic data model and will ensure that
    the constraint is learned.

    Args:
        column_names(list[str]):
            A list of column names involved in the constraint
        data(pandas.DataFrame):
            A dataset with the original data

    Returns:
        pandas DataFrame
            The full data after it has been transformed
    """

    transformed_data = data
    return transformed_data

def reverse_transform(column_names, transformed_data):
    """
    Reverses the transformation for the column names to recover
    data in the original state. The reverse transform will be applied
    to the synthetic data data the model creates.


    Args:
        column_names(list[str]):
            A list of column names involved in the constraint
        transformed_data(pandas.DataFrame):
            A dataset with the transformed data

    Returns:
        pandas DataFrame
            The full data after it has been reverse transformed
    """

    id = column_names[0]
    gender = column_names[1]

    reversed_data = transformed_data
    reversed_data[id] = reversed_data.apply(
        lambda x: replace_id(x[id], '1') if x[gender] == '男' 
        else replace_id(x[id], '2'), axis=1)

    return reversed_data


IdGenderConstraints = create_custom_constraint_class(
    is_valid_fn=is_valid,
    transform_fn=transform,
    reverse_transform_fn=reverse_transform # optional
)

### USE THE CONSTRAINT IN A SEPARATE FILE

# Step 1. Load the constraint
# synthesizer.load_custom_constraint_class(
#     filepath='custom_constraint_template.py'
#     class_names='MyCustomConstraintClass'
# )
   
# Step 2. Apply it
# my_constraint = {
#     'constraint_class': 'MyCustomConstraintClass',
#     'constraint_parameters': {
#         'column_names': [],
#         'extra_parameter': None
#     }
# }
# synthsizer.add_constraints([my_constraint])