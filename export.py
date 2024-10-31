import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Border, Side

def add_batting_column(df, batting_value):
    """
    Add a 'batting' column with a single value to the DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame to modify.
        batting_value (any): Value to be placed in the 'batting' column.

    Returns:
        pd.DataFrame: Modified DataFrame with the 'batting' column added.
    """
    df['batting'] = ''
    if not df.empty:
        df.at[0, 'batting'] = batting_value
    return df

def write_dataframes_to_excel(df1, df2, df3, df1_batting, df2_batting, df3_batting, fund_name, file_path):
    """
    Write three DataFrames to a single Excel sheet horizontally.

    Parameters:
        df1, df2, df3 (pd.DataFrame): DataFrames to write.
        df1_batting, df2_batting, df3_batting (any): Values for the 'batting' column in each DataFrame.
        fund_name (str): Name of the sheet in the Excel file.
        file_path (str): Path to the output Excel file.
    """
    # Add 'batting' column with specified values
    df1 = add_batting_column(df1, df1_batting)
    df2 = add_batting_column(df2, df2_batting)
    df3 = add_batting_column(df3, df3_batting)

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        # Write each DataFrame to the Excel sheet, placing them horizontally
        df1.to_excel(writer, sheet_name=f'{fund_name}', startrow=0, startcol=0, index=False)
        df2.to_excel(writer, sheet_name=f'{fund_name}', startrow=0, startcol=len(df1.columns) + 3, index=False)
        df3.to_excel(writer, sheet_name=f'{fund_name}', startrow=0, startcol=len(df1.columns) + len(df2.columns) + 6, index=False)

    # Add borders after writing all DataFrames
    add_borders_to_tables(file_path, fund_name, df1, df2, df3)

def add_borders_to_tables(file_path, fund_name, df1, df2, df3):
    """
    Add borders around each table in the Excel sheet.

    Parameters:
        file_path (str): Path to the Excel file to modify.
        fund_name (str): Name of the sheet in the Excel file.
        df1, df2, df3 (pd.DataFrame): DataFrames to determine table dimensions for borders.
    """
    wb = load_workbook(file_path)
    ws = wb[f'{fund_name}']

    # Define a border style
    border = Border(left=Side(style='thin'),
                    right=Side(style='thin'),
                    top=Side(style='thin'),
                    bottom=Side(style='thin'))

    # Add borders to each DataFrame's table
    start_col = 0
    for df in [df1, df2, df3]:
        num_rows, num_cols = df.shape
        for row in ws.iter_rows(min_row=1, max_row=num_rows, min_col=start_col + 1, max_col=start_col + num_cols):
            for cell in row:
                cell.border = border
        start_col += num_cols + 3  # Move to the next column, with some spacing

    wb.save(file_path)
