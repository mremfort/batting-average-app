# app
import streamlit as st
from data_functions import uploaded_file_check, all_around_batting_average, up_benchmark_batting_average, down_benchmark_batting_average
from template_download_funcs import get_test_file_content, get_bell_file_content
from export import add_borders_to_tables, write_dataframes_to_excel
import openpyxl

st.set_page_config(
    page_title="Up-Down App",
    page_icon=":chart:",
    layout="wide"
)

with st.sidebar:
    page = st.selectbox("Choose a page", ["Test Fund", "Bell Curve"])

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
        pass_status, uploaded_file_pd, fund_info_pd, fund_data_pd = uploaded_file_check(file)
        if pass_status is None:
            st.error("Something is wong with your sheet. Make sure you are using the template",icon="🚨")

        else:
            fund_info_col1, fund_info_col2 = st.columns(2)
            with fund_info_col1:
                st.header("Fund Overview")
                st.write(fund_info_pd.at[0,"Fund Name"])
                st.write(fund_info_pd.at[0, "Benchmark Name"])
                st.write(fund_info_pd.at[0, "Benchmark Ticker"])


            st.markdown("---")

            general_comparison_table, general_comparison_average = all_around_batting_average(fund_data_pd)
            up_benchmark_table, up_benchmark_average = up_benchmark_batting_average(fund_data_pd)
            down_benchmark_table, down_benchmark_average = down_benchmark_batting_average(fund_data_pd)


            general_comparison_cols1, general_comparison_cols2, general_comparison_cols3 = st.columns(3)
            with general_comparison_cols1:
                st.header(f"All Time Performance")
                st.subheader(f"Average: {round(general_comparison_average *100)}%")
                with st.expander("View General Performance Table"):
                    st.dataframe(general_comparison_table)

            with general_comparison_cols2:
                st.header(f"Up Bechmark Performance")
                st.subheader(f"Average: {round(up_benchmark_average *100)}%")
                with st.expander("View Up Benchmark Table"):
                    st.dataframe(up_benchmark_table)

            with general_comparison_cols3:
                st.header(f"Down Bechmark Performance")
                st.subheader(f"Average: {round(down_benchmark_average *100)}%")
                with st.expander("View Down Benchmark Table"):
                 st.dataframe(down_benchmark_table)

            with fund_info_col2:
                st.header("Average")
                full_average = round(((up_benchmark_average+down_benchmark_average)/2)*100)
                st.subheader(f"{full_average}%")

            with st.sidebar:
                if st.button('Create Excel File'):
                    df1, df2, df3 = general_comparison_table, up_benchmark_table,down_benchmark_table
                    fund_name = fund_info_pd.at[0, "Fund Name"]
                    file_path = f'combined_data_horizontal_{fund_name}.xlsx'


                    # Write DataFrames and add borders
                    write_dataframes_to_excel(df1, df2, df3,general_comparison_average,up_benchmark_average,down_benchmark_average, fund_name,file_path)
                    add_borders_to_tables(file_path, fund_name,df1, df2, df3)

                    st.success('Excel file created successfully!')
                    # Provide a link to download the file
                    with open(file_path, 'rb') as f:
                        st.download_button(
                            label='Download Excel File',
                            data=f,
                            file_name=file_path,
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )

elif page == "Bell Curve":
    from bell_curve_funcs import process_uploaded_data
    from bell_curve_charts import create_bell_curve_chart

    funds_file = st.file_uploader("Upload your csv", type="xlsx")
    if funds_file is not None:
        df, mean, std_dev = process_uploaded_data(funds_file)
        fig = create_bell_curve_chart(df, mean, std_dev)
        st.plotly_chart(fig)

