from bell_curve_funcs import prepare_data
from bell_curve_charts import create_bell_curve_chart


df, mean, std_dev = prepare_data()
fig = create_bell_curve_chart(df, mean, std_dev)
st.plotly_chart(fig)