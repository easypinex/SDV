import pandas as pd

from sdv.constraints import create_custom_constraint_class


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

    salary = column_names[0]
    loan_amount = column_names[1]

    return data[loan_amount] <= 1.5 * data[salary]

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

    salary = column_names[0]
    loan_amount = column_names[1]

    reversed_data = transformed_data
    reversed_data[loan_amount] \
        = reversed_data.apply(lambda x: x[loan_amount] 
                              if x[salary] * 1.5 >= x[loan_amount] 
                              else x[salary] * 1.5, axis=1)

    return reversed_data


LoanMaximumConstraints = create_custom_constraint_class(
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