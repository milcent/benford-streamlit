import streamlit as st
import pandas as pd
import benford as bf

csv_file = st.sidebar.file_uploader("", type="csv",
                key="csv_uploader")
try:
    df = pd.read_csv(csv_file)
    st.dataframe(df)
except:
    pass

col = st.selectbox("Select column for analysis", df.columns)

# st.write(df.dtypes)
decimals = st.sidebar.number_input("Number of decimal places", min_value=0,
                        value=2, step=1)

sign = st.sidebar.selectbox("Choose which records' sign to analyse",
                    options=["all", "positive", "negative"])

try:
    bo = bf.Benford(df[col], decimals=decimals, sign=sign[:3])
    st.sidebar.markdown(f"#### Initial sample size: **{len(df)}**.")
    st.sidebar.markdown(f"#### Analysis performed on **{len(bo.base)}** records.")
    st.sidebar.markdown("#### Number of discard entries for each test: ")
    st.sidebar.markdown("- " +"\n - ".join([f"{key}: **{val}**" for key, val in 
                            bo._discarded.items()]))
except:
    st.markdown("## Something went wrong with your selection. " +\
        "Benford_py tries to convert data in string to *int* o *float* " +\
        "but did not succed. Check you data types.")

