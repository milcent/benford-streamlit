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

from typing import List, Union
from pandas import DataFrame, read_csv
from benford import Test, Benford

TESTS = {
    "First Digit Test": "F1D", "Second Digit Test": "SD",
    "First Two Digits Test": "F2D", "First Three Digits Test": "F3D",
    "Last Two Digits Test": "L2D"
}

STATS_DF_LEGEND = """<span style='color:black'>* Independent of sample size 
    or confidence; ** Better close to 0: </span><span style='color:green'>
    0-ref_1: green</span><span style='color:black'>; </span><span style='color:
    orange'>ref_1-ref_2: orange</span><span style='color:black'>; </span><span
     style='color:red'>ref_2-ref_3: red</span><span style='color:black'>; and 
     </span> <span style='color:darkred'>> ref_3: dark red</span><span style=
     'color:black'>. Black when not applicable</span>"""

DISCLAIMER = """***Disclaimer***: this interactive app was built to 
                facilitate your analysis. It asssumes you already know 
                your dataset and how to apply the tests, with all possible
                configurations, and how to interpret the results that may 
                arise from them. The author assumes no responsability for 
                how you use any of the information inserted herein, nor 
                any result from its analysis."""

def _get_color_mad_(mad:float, mad_list=Union[List, None]):
    if not mad_list:
        return "black"
    if mad > mad_list[2]:
        return "darkred"
    elif mad > mad_list[1]:
        return "red"
    elif mad > mad_list[0]:
        return "orange"
    return "green"


load_df = read_csv


def make_stats_df(benf_test:Test):
    crit_chi  = benf_test.critical_values["chi2"]
    crit_ks = benf_test.critical_values["KS"]
    mad, mad_list = benf_test.MAD, benf_test.critical_values["MAD"]
    mad_color = _get_color_mad_(mad, mad_list)

    red_mask_chi = lambda x: f"color: {'red' if x > crit_chi else 'black'}"
    red_mask_ks = lambda x: f"color: {'red' if x > crit_ks else 'black'}"
    mask_mad = lambda x: f"color: {mad_color if isinstance(x, float) else 'black'}"
    if not benf_test.critical_values['Z']:
        red_mask_chi = lambda x: "color: black"
        red_mask_ks = lambda x: "color: black"

    stats = {
        "Chi-square": [benf_test.chi_square, crit_chi],
        "Kolmogorov-Smirnov": [benf_test.KS, crit_ks],
        "Mean Absolute Deviation": [mad, f"{mad_list} * **"],
        "Bhattacharyya Coefficient": [
            benf_test.bhattacharyya_coefficient, "Better close to 1 *"
        ],
        "Kullback-Leibler Divergence": [
            benf_test.kullback_leibler_divergence, "Better close to 0 *"
        ]
    }
    return DataFrame(stats, index=["statistic", "reference"])\
            .style.set_properties(
                **{"text-align": "center", "font-weight": "bold"})\
            .applymap(red_mask_chi, subset="Chi-square")\
            .applymap(red_mask_ks, subset="Kolmogorov-Smirnov")\
            .applymap(mask_mad, subset="Mean Absolute Deviation")


def make_z_scores_df(benf_test:Test):
    red_mask = lambda x: f"color: {'red' if x > benf_test.critical_values['Z'] else 'black'}"
    if not benf_test.critical_values['Z']:
        red_mask = lambda x: "color: black"
    return benf_test[["Counts", "Found", "Expected", "Z_score"]]\
        .rename(columns={
            "Counts": "Digits Counts", "Found": "Found Proportions",
            "Expected": "Expected Proportions",
            "Z_score": "Z score of Found Proportions"
        }).reset_index().style.set_properties(**{"text-align": "center", "font-weight": "bold"})\
        .applymap(red_mask,
                    subset="Z score of Found Proportions")\
        .hide_index()


def filter_df_by_digits(benf_instance:Benford, base_data:DataFrame,
                        benf_test_name:str, digits:int, selected_col:str):

    filter_df = benf_instance.base.loc[
                    benf_instance.base[benf_test_name] == digits, "seq"
                ]
    return base_data.join(filter_df, how="inner").drop(columns=["seq"])\
                .style.set_properties(**{
                        "background_color":"orange","font-weight": "bold"},
                    subset=selected_col)
            
