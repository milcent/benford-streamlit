import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import Tabs, Panel
from bokeh.layouts import Column

import benford as bf
from benfordviz.bokeh_plotting import BenfordBokehChart

csv_file = st.sidebar.file_uploader("", type="csv",
                key="csv_uploader")
try:
    df = pd.read_csv(csv_file)
    # st.dataframe(df)
except:
    pass

col = st.selectbox("==== Select column for analysis, whose dtype is 'int', "
                    "'float', or an easily convertible string. ====", df.columns)

# st.write(df.dtypes)
decimals = st.sidebar.number_input("Number of decimal places", min_value=0,
                        value=2, step=1)

sign = st.sidebar.selectbox("Choose which records' sign to analyse",
                    options=["all", "positive", "negative"])

try:
    bo = bf.Benford(df[col], decimals=decimals, sign=sign[:3])
    st.sidebar.markdown(f"#### Initial sample size: **{len(df)}**.")
    st.sidebar.markdown(f"#### Analysis performed on **{len(bo.base)}** " +
                        f"non-zero, {sign}-sign records.")
    st.sidebar.markdown("#### Number of discarded entries for each test " +
                        " (dependent on decimal places chosen): ")
    st.sidebar.markdown("- " +"\n - ".join(
                            [f"{bf.constants.TEST_NAMES[key]}: **{val}**" for key, 
                            val in bo._discarded.items()]))
except:
    st.markdown("#### Waiting for proper column selection.")

# st.bokeh_chart(tabs)
bbc = BenfordBokehChart(bo.F2D)
# st.write(type(bbc))
st.bokeh_chart(bbc.figure)