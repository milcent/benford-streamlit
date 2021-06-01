"""
Marcel Milcent, Copyright 2021

This file is part of benford-streamlit app.

    benford-streamlit app is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    benford-streamlit app is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with benford-streamlit app.  If not, see <https://www.gnu.org/licenses/>
"""

import streamlit as st

import benford as bf
from benford.constants import CONFS
from benfordviz.bokeh_plotting import BenfordBokehChart

from helpers import (TESTS, load_df, make_stats_df, make_z_scores_df,
                     filter_df_by_digits)

st.markdown("# Interactive Benford Analysis")

csv_file = st.sidebar.file_uploader("", type="csv", key="csv_uploader")
                
try:
    df = load_df(csv_file)

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
        st.markdown(
            """<h4 style='color:red'>Waiting for proper column selection</h4>""",
            unsafe_allow_html=True)

    test_show = getattr(bo, TESTS[benf_test])

    col1, col2 = st.beta_columns(2)
    with col1:
        st.markdown("## Digits Found and Expected Proportions")
    with col2:
        st.markdown(f"Initial sample size: **{len(df)}**. Analysis performed"
                    f" on **{len(bo.base)}** non-zero, {sign}-sign records.\n"
                    "Number of discarded registries for this test (dependent "
                    f"on decimal places): **{bo._discarded[TESTS[benf_test]]}**.")

    bbc = BenfordBokehChart(test_show)
    st.bokeh_chart(bbc.figure)
    
    st.markdown("## Scalar statistics")
    independ_stat_df = make_stats_df(test_show)
    st.dataframe(independ_stat_df)
    st.markdown("\* Independent of sample size or confidence; "
                "** Better close to 0: 0-ref_1: green; ref_1-ref_2: orange; "
                "ref_2-ref_3: red; and > ref_3: dark red")

    col5, col6 = st.beta_columns(2)
    with col5:
        st.markdown("## Z scores table")
    with col6:
        st.markdown("")
        st.markdown("")
        st.markdown(f"Critical Z score for {confidence}% confidence: "
                    f"{CONFS[confidence]} (red for failing).")
    st.dataframe(make_z_scores_df(test_show))

    st.markdown("## Select failing Z score digit to filter base data")
    fail_z_digits = test_show.sort_values("Z_score", ascending=False)\
                        .loc[test_show.Z_score > test_show.critical_values["Z"]]\
                        .index.to_list()
    # st.write(fail_z_digits)
    dig_to_filter = st.selectbox("", options=fail_z_digits)
    filtered_df = filter_df_by_digits(bo, df, TESTS[benf_test], dig_to_filter,
                                     col)
    st.write(filtered_df)

    st.markdown("""***Disclaimer***: this interactive dashboard was built to 
                facilitate your analysis. It asssumes you already know 
                your dataset and how to apply the tests, with all possible
                configurations, and how to interpret the results that may 
                arise from them. The author assumes no responsability for 
                how you use any of the information inserted herein, nor 
                any result from its analysis.""")
except:
    pass