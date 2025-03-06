import os


# Function to display backup files
def display_backup_files():
    if not os.path.exists('backups'):
        st.write("No backups found.")
        return

    backups = sorted([f for f in os.listdir('backups') if f.startswith('funds_scores_backup_')])
    if backups:
        st.write("Backup Files:")
        for backup in backups:
            st.write(backup)
    else:
        st.write("No backups found.")


# app
import streamlit as st
import pandas as pd
import time
from data_functions import uploaded_file_check, all_around_batting_average, up_benchmark_batting_average, \
    down_benchmark_batting_average, calculate_excess_return, calculate_annualized_return, calculate_annualized_std, \
    calculate_tracking_error, calculate_sharpe_ratio, calculate_information_ratio
from template_download_funcs import get_test_file_content, get_bell_file_content
from export import add_borders_to_tables, write_dataframes_to_excel
from database import create_table, insert_or_update_score, fetch_scores, remove_score, backup_database, restore_database

st.set_page_config(
    page_title="Up-Down App",
    page_icon=":chart:",
    layout="wide"
)
create_table()


def display_scores_table(scores):
    # Create a DataFrame from the scores
    df = pd.DataFrame(scores, columns=["ID", "Fund", "Benchmark", "Ticker", "All Time Average", "Up Benchmark",
                                       "Down Benchmark"])

    # Calculate the Final column
    df["Final"] = (df["Up Benchmark"] + df["Down Benchmark"]) / 2

    # Drop the ID column for display
    df = df.drop(columns=["ID"])

    # Display the DataFrame as a table
    st.dataframe(df)


def backup_database_with_progress():
    with st.spinner('Backing up database...'):
        backup_database()
        time.sleep(2)  # Simulate a delay for the backup process
        st.success('Database backup completed!')


with st.sidebar:
    page = st.selectbox("Choose a page", ["Test Fund", "Bell Curve", "Database"])

    if page == "Test Fund":
        if st.download_button(
                label="Download Batting Template",
                data=get_test_file_content(),
                file_name="batting_average_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            st.success("Download initiated!")
    elif page == "Bell Curve":
        if st.download_button(
                label="Download Bell Curve Template",
                data=get_bell_file_content(),
                file_name="bell_curve_import_template_.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            st.success("Download initiated!")

if page == "Test Fund":
    file = st.file_uploader("Upload your csv", type="xlsx")

    if file is not None:
        pass_status, original_file_df, fund_info_pd, fund_data_pd = uploaded_file_check(file)
        if pass_status is None:
            st.error("Something is wrong with your sheet. Make sure you are using the template", icon="🚨")
        else:
            if not fund_info_pd.empty:
                fund_info_col1, fund_info_col2 = st.columns(2)
                with fund_info_col1:
                    st.header("Fund Overview")
                    st.write(fund_info_pd.at[0, "Fund Name"])
                    st.write(fund_info_pd.at[0, "Benchmark Name"])
                    st.write(fund_info_pd.at[0, "Benchmark Ticker"])

                st.markdown("---")
                # Calculate excess return
                fund_data_pd = calculate_excess_return(fund_data_pd)

                # Calculate metrics
                annualized_return_fund = calculate_annualized_return(fund_data_pd['Fund Return'])
                annualized_return_benchmark = calculate_annualized_return(fund_data_pd['Benchmark Return'])
                annualized_std_fund = calculate_annualized_std(fund_data_pd['Fund Return'])
                annualized_std_benchmark = calculate_annualized_std(fund_data_pd['Benchmark Return'])
                excess_return = annualized_return_fund - annualized_return_benchmark
                tracking_error = calculate_tracking_error(fund_data_pd['Excess Return'])
                sharpe_ratio_fund = calculate_sharpe_ratio(annualized_return_fund, annualized_std_fund)
                sharpe_ratio_benchmark = calculate_sharpe_ratio(annualized_return_benchmark, annualized_std_benchmark)
                information_ratio = calculate_information_ratio(excess_return, tracking_error)
                information_ratio = calculate_information_ratio(excess_return, tracking_error)

                general_comparison_table, general_comparison_average = all_around_batting_average(fund_data_pd)
                up_benchmark_table, up_benchmark_average = up_benchmark_batting_average(general_comparison_table)
                down_benchmark_table, down_benchmark_average = down_benchmark_batting_average(general_comparison_table)

                general_comparison_cols1, general_comparison_cols2, general_comparison_cols3 = st.columns(3)
                with general_comparison_cols1:
                    st.header(f"All Time Performance")
                    st.subheader(f"Average: {round(general_comparison_average * 100)}%")
                    with st.expander("View General Performance Table"):
                        st.dataframe(general_comparison_table)

                with general_comparison_cols2:
                    st.header(f"Up Benchmark Performance")
                    st.subheader(f"Average: {round(up_benchmark_average * 100)}%")
                    with st.expander("View Up Benchmark Table"):
                        st.dataframe(up_benchmark_table)

                with general_comparison_cols3:
                    st.header(f"Down Benchmark Performance")
                    st.subheader(f"Average: {round(down_benchmark_average * 100)}%")
                    with st.expander("View Down Benchmark Table"):
                        st.dataframe(down_benchmark_table)

                with fund_info_col2:
                    st.header("Average")
                    full_average = round(((up_benchmark_average + down_benchmark_average) / 2) * 100)
                    st.subheader(f"{full_average}%")


                excess_cols1, excess_cols2, excess_cols3 = st.columns(3)
                # Display calculated metrics

                with excess_cols1:
                    st.markdown("---")
                    st.header("Fund Excess Return Data")
                    st.write(f"Annualized Return (Fund): {annualized_return_fund:.2%}")
                    st.write(f"Annualized STD (Fund): {annualized_std_fund:.2%}")
                    st.write(f"Excess Return (Fund): {excess_return:.2%}")
                    st.write(f"Tracking Error (Fund): {tracking_error:.2%}")
                    st.write(f"Sharpe Ratio (Fund): {sharpe_ratio_fund:.2f}")
                    st.write(f"Information Ratio (Fund): {information_ratio:.2f}")

                with excess_cols2:
                    # Display excess return data
                    st.markdown("---")
                    st.header("Bench Return Data")
                    st.write(f"Annualized Return (Benchmark): {annualized_return_benchmark:.2%}")
                    st.write(f"Annualized STD (Benchmark): {annualized_std_benchmark:.2%}")
                    st.write(f"Sharpe Ratio (Benchmark): {sharpe_ratio_benchmark:.2f}")
                with excess_cols3:
                    # Display excess return data
                    st.markdown("---")
                    st.header("Excess Return Table")
                    with st.expander("View Excess Return Table"):
                        st.dataframe(fund_data_pd[['Date', 'Fund Return', 'Benchmark Return', 'Excess Return']])

                # Insert or update scores in the database
                insert_or_update_score(
                    fund_info_pd.at[0, "Fund Name"],
                    fund_info_pd.at[0, "Benchmark Name"],
                    fund_info_pd.at[0, "Benchmark Ticker"],
                    general_comparison_average,
                    up_benchmark_average,
                    down_benchmark_average
                )

                if st.sidebar.button('Export Results'):
                    df1, df2, df3 = general_comparison_table, up_benchmark_table, down_benchmark_table
                    fund_name = fund_info_pd.at[0, "Fund Name"]
                    benchmark_name = fund_info_pd.at[0, "Benchmark Name"]
                    file_path = f'{fund_name}_vs_{benchmark_name}_results.xlsx'

                    # Create the excess return data DataFrame
                    excess_return_data = fund_data_pd[['Date', 'Fund Return', 'Benchmark Return', 'Excess Return']]

                    # Create the final scores DataFrame
                    final_scores = pd.DataFrame({
                        "Metric": ["Annualized Return (Fund)", "Annualized Return (Benchmark)",
                                   "Annualized STD (Fund)", "Annualized STD (Benchmark)",
                                   "Excess Return", "Tracking Error", "Sharpe Ratio (Fund)",
                                   "Sharpe Ratio (Benchmark)", "Information Ratio", "Up Batting Average","Down Batting Average", "All Time Batting Average","Final Batting Average"],
                        "Value": [annualized_return_fund, annualized_return_benchmark, annualized_std_fund,
                                  annualized_std_benchmark,
                                  excess_return, tracking_error, sharpe_ratio_fund, sharpe_ratio_benchmark,
                                  information_ratio,up_benchmark_average,down_benchmark_average,general_comparison_average,full_average]
                    })

                    # Write DataFrames and add borders
                    write_dataframes_to_excel(df1, df2, df3, general_comparison_average, up_benchmark_average,
                                              down_benchmark_average, fund_name, benchmark_name,file_path, excess_return_data,
                                              final_scores)
                    with st.sidebar:
                        st.success('Excel file created successfully!')
                        # Provide a link to download the file
                        with open(file_path, 'rb') as f:
                            st.download_button(
                                label='Download Excel File',
                                data=f,
                                file_name=file_path,
                                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                            )
            else:
                st.error("The file is empty. Please check the uploaded file.")

elif page == "Bell Curve":
    from bell_curve_funcs import process_uploaded_data, process_database_data
    from bell_curve_charts import create_bell_curve_chart

    data_source = st.radio("Select Data Source", ("Upload File", "Database"))

    if data_source == "Upload File":
        funds_file = st.file_uploader("Upload your csv", type="xlsx")
        if funds_file is not None:
            df, mean, std_dev = process_uploaded_data(funds_file)
            fig = create_bell_curve_chart(df, mean, std_dev)
            st.plotly_chart(fig)
    elif data_source == "Database":
        df, mean, std_dev = process_database_data()
        fig = create_bell_curve_chart(df, mean, std_dev)
        st.plotly_chart(fig)

elif page == "Database":
    search_term = st.text_input("Search for a Fund or Benchmark:")

    scores = fetch_scores()

    if search_term:
        scores = [score for score in scores if
                  search_term.lower() in score[1].lower() or search_term.lower() in score[2].lower()]

    display_scores_table(scores)

    selected_fund = st.selectbox("Select a Fund to Remove", [score[1] for score in scores])

    # Initialize session state for confirmation
    if 'confirm_remove' not in st.session_state:
        st.session_state.confirm_remove = False

    if selected_fund:
        if st.button("Remove Selected Fund"):
            st.session_state.confirm_remove = True

        if st.session_state.confirm_remove:
            st.error("Do you really, really, wanna do this?")
            if st.button("Yes I'm ready to rumble"):
                backup_database_with_progress()
                remove_score(selected_fund)
                st.success(f"{selected_fund} has been removed and the database has been backed up.")
                # Refresh the scores table
                scores = fetch_scores()
                display_scores_table(scores)
                # Reset confirmation state
                st.session_state.confirm_remove = False
        # Restore database section
        st.header("Restore Database from Backup")
        backups = sorted([f for f in os.listdir('backups') if f.startswith('funds_scores_backup_')])
        selected_backup = st.selectbox("Select a Backup to Restore", backups)

        if st.button("Restore Selected Backup"):
            restore_database(selected_backup)
            st.success(f"Database restored from {selected_backup}")
            # Refresh the scores table
            scores = fetch_scores()
            display_scores_table(scores)
    st.markdown("---")
    st.header("Database Backups")
    display_backup_files()
