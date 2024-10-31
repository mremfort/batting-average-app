import pandas as pd

def process_uploaded_data(file):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file)

    # Make sure 'Values' column exists
    if 'Batting Average' not in df.columns:
        raise ValueError("The uploaded file must contain a 'Batting Average' column")

    if 'Funds' not in df.columns:
        raise ValueError("The uploaded file must contain a 'Funds' column")

    # Calculate the mean and standard deviation
    mean = df['Batting Average'].mean()
    std_dev = df['Batting Average'].std()

    return df, mean, std_dev