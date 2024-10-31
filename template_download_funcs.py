import pandas as pd
from io import BytesIO

# Path to the existing Excel file
test_fund_file_path = 'mremfort/batting-average-app/Batting Average Template.xlsx'
bell_file_path = 'Fund_import_template.xlsx'

# Function to read the Excel file and return its content
def get_test_file_content():
    with open(test_fund_file_path, 'rb') as file:
        file_content = file.read()
    return file_content

def get_bell_file_content():
    with open(bell_file_path, 'rb') as file:
        file_content = file.read()
    return file_content
