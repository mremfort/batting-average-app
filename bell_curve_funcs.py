import pandas as pd
from database import fetch_scores


def process_uploaded_data(file):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file)

    # Make sure 'Final' column exists
    if 'Final' not in df.columns:
        raise ValueError("The uploaded file must contain a 'Final' column")

    if 'Fund' not in df.columns:
        raise ValueError("The uploaded file must contain a 'Fund' column")

    # Calculate the mean and standard deviation
    mean = df['Final'].mean()
    std_dev = df['Final'].std()

    return df, mean, std_dev


def process_database_data():
    scores = fetch_scores()

    # Create a DataFrame from the scores
    df = pd.DataFrame(scores, columns=["ID", "Fund", "Benchmark", "Ticker", "All Time Average", "Up Benchmark",
                                       "Down Benchmark"])

    # Calculate the Final column
    df["Final"] = (df["Up Benchmark"] + df["Down Benchmark"]) / 2

    # Drop unnecessary columns for bell curve calculation
    df = df.drop(columns=["ID", "Benchmark", "Ticker", "All Time Average", "Up Benchmark", "Down Benchmark"])

    # Calculate the mean and standard deviation
    mean = df['Final'].mean()
    std_dev = df['Final'].std()

    return df, mean, std_dev
