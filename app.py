# app
import streamlit as st
import pandas as pd
from data_functions import uploaded_file_check, all_around_batting_average, up_benchmark_batting_average, \
    down_benchmark_batting_average
from template_download_funcs import get_test_file_content, get_bell_file_content
from export import add_borders_to_tables, write_dataframes_to_excel
from database import create_table, insert_or_update_score, fetch_scores

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


with st.sidebar:
    page = st.selectbox("Choose a page", ["Test Fund", "Bell Curve", "Database"])

    if page == "Test Fund":
        if st.download_button(
                label="Download Excel File",
                data=get_test_file_content(),
                file_name="batting_average_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            st.success("Download initiated!")
    elif page == "Bell Curve":
        if st.download_button(
                label="Download Excel File",
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

                # Insert or update scores in the database
                insert_or_update_score(
                    fund_info_pd.at[0, "Fund Name"],
                    fund_info_pd.at[0, "Benchmark Name"],
                    fund_info_pd.at[0, "Benchmark Ticker"],
                    general_comparison_average,
                    up_benchmark_average,
                    down_benchmark_average
                )

                if st.sidebar.button('Show All Scores'):
                    scores = fetch_scores()
                    display_scores_table(scores)

                if st.sidebar.button('Create Excel File'):
                    df1, df2, df3 = general_comparison_table, up_benchmark_table, down_benchmark_table
                    fund_name = fund_info_pd.at[0, "Fund Name"]
                    file_path = f'combined_data_horizontal_{fund_name}.xlsx'

                    # Write DataFrames and add borders
                    write_dataframes_to_excel(df1, df2, df3, general_comparison_average, up_benchmark_average,
                                              down_benchmark_average, fund_name, file_path)
                    add_borders_to_tables(file_path, fund_name, df1, df2, df3)

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
                st.error("The DataFrame is empty. Please check the uploaded file.")

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
