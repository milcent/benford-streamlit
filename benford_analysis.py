import streamlit as st
# from bokeh.plotting import figure
# from bokeh.models import Tabs, Panel
# from bokeh.layouts import Column

import benford as bf
from benford.constants import CONFS
from benfordviz.bokeh_plotting import BenfordBokehChart

from helpers import (load_df, make_stats_df,
                     make_z_scores_df)

TESTS = {
    "First Digit Test": "F1D", "Second Digit Test": "SD",
    "First Two Digits Test": "F2D", "First Three Digits Test": "F3D",
    "Last Two Digits Test": "L2D"
}

st.markdown("# Interactive Benford Analysis")

csv_file = st.sidebar.file_uploader("", type="csv", key="csv_uploader")
                
try:
    df = load_df(csv_file)
    # st.dataframe(df)    

    col = st.sidebar.selectbox("Select column for analysis, whose dtype is 'int', "
                        "'float', or an easily convertible string.", df.columns)

    # st.write(df.dtypes)
    sign = st.sidebar.selectbox("Choose which records' sign to analyse",
                                options=["all", "positive", "negative"])

    decimals = st.sidebar.number_input("Chooose number of decimal places", min_value=0,
                            value=2, step=1)


    try:
        bo = bf.Benford(
            df[col], decimals=decimals, sign=sign[:3])
        benf_test = st.sidebar.selectbox("Choose test", options=list(TESTS.keys()))
        confidence = st.sidebar.select_slider(
            "Choose confidence level (%)", options=list(CONFS.keys()),
            value=95)
        if not (isinstance(confidence, int) | isinstance(confidence, float)):
            confidence=None
        bo.update_confidence(confidence)

    except:
        st.markdown("""<h4 style='color:red'>Waiting for proper column selecyion</h4>""",
                unsafe_allow_html=True)

    test_show = getattr(bo, TESTS[benf_test])

    col1, col2 = st.beta_columns(2)
    with col1:
        st.markdown("## Digits Found and Expected Proportions")
    with col2:
        st.markdown(f" Initial sample size: **{len(df)}**."
                    f" Analysis performed on **{len(bo.base)}** "
                    f"non-zero, {sign}-sign records.\nNumber of discarded registries for this test (dependent "
                    f"on decimal places): **{bo._discarded[TESTS[benf_test]]}**.")

    bbc = BenfordBokehChart(test_show)
    st.bokeh_chart(bbc.figure)
    
    st.markdown("## Scalar statistics")
    independ_stat_df = make_stats_df(test_show)
    st.dataframe(independ_stat_df)
    st.markdown("\* Independent of sample size or confidence")

    col5, col6 = st.beta_columns(2)
    with col5:
        st.markdown("## Z scores table")
    with col6:
        st.markdown("")
        st.markdown("")
        st.markdown(f"Critical Z score for {confidence}% confidence: "
                    f"{CONFS[confidence]} (red for failing).")
    st.dataframe(make_z_scores_df(test_show))
except:
    pass