import pandas as pd
import numpy as np

def uploaded_file_check(file):

    original_file_df = pd.ExcelFile(file)

    imported_file_sheet_names = original_file_df.sheet_names

    if 'Fund Info' not in imported_file_sheet_names:
        return None

    elif 'Data' not in imported_file_sheet_names:
        return  None

    else:
        fund_info = pd.read_excel(file,"Fund Info")

        fund_info_cols = fund_info.columns.tolist()

        if "Fund Name" not in fund_info_cols:
            return None

        elif "Benchmark Name" not in fund_info_cols:
            return None

        elif "Benchmark Ticker" not in fund_info_cols:
            return None

        fund_data = pd.read_excel(file,"Data")
        fund_data_cols = fund_data.columns.tolist()

        if "Date" not in fund_data_cols:
            return None

        elif "Fund Return" not in fund_data_cols:
            return None

        elif "Benchmark Return" not in fund_data_cols:
            return None

    return "pass",original_file_df, fund_info, fund_data


def all_around_batting_average(fund_data_df):
    fund_data_df['check'] = np.where(fund_data_df["Fund Return"] > fund_data_df["Benchmark Return"],1,0)
    general_comparison_table = fund_data_df.copy()
    count_check = general_comparison_table['check'].sum()
    total_rows = len(general_comparison_table)
    general_average = count_check/total_rows

    return general_comparison_table, general_average

def up_benchmark_batting_average(general_comparison_table):
    # Add the 'check' column based on the condition
    general_comparison_table['check'] = np.where(
        (general_comparison_table["Fund Return"] > general_comparison_table["Benchmark Return"]),
        1,
        0
    )

    # Filter the DataFrame to include only rows where 'Benchmark Return' > 0
    up_benchmark_table = general_comparison_table[general_comparison_table["Benchmark Return"] > 0].copy()

    # Calculate the count of 'check' and total rows after filtering
    count_check = up_benchmark_table['check'].sum()
    total_rows = len(up_benchmark_table)

    # Calculate the up benchmark average
    up_benchmark_average = count_check / total_rows if total_rows > 0 else 0

    return up_benchmark_table, up_benchmark_average


def down_benchmark_batting_average(general_comparison_table):
    # Add the 'check' column based on the condition
    general_comparison_table['check'] = np.where(
        (general_comparison_table["Fund Return"] > general_comparison_table["Benchmark Return"]),
        1,
        0
    )

    # Filter the DataFrame to include only rows where 'Benchmark Return' < 0
    down_benchmark_table = general_comparison_table[general_comparison_table["Benchmark Return"] < 0].copy()

    # Calculate the count of 'check' and total rows after filtering
    count_check = down_benchmark_table['check'].sum()
    total_rows = len(down_benchmark_table)

    # Calculate the down benchmark average
    down_benchmark_average = count_check / total_rows if total_rows > 0 else 0

    return down_benchmark_table, down_benchmark_average