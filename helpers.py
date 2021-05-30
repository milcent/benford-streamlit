from typing import List, Union
from pandas import DataFrame, read_csv


def get_color_mad(mad:float, mad_list=Union[List, None]):
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

def make_stats_df(benf_test):
    crit_chi  = benf_test.critical_values["chi2"]
    crit_ks = benf_test.critical_values["KS"]
    mad, mad_list = benf_test.MAD, benf_test.critical_values["MAD"]
    mad_color = get_color_mad(mad, mad_list)

    red_mask_chi = lambda x: f"color: {'red' if x > crit_chi else 'black'}"
    red_mask_ks = lambda x: f"color: {'red' if x > crit_ks else 'black'}"
    mask_mad = lambda x: f"color: {mad_color if isinstance(x, float) else 'black'}"
    if not benf_test.critical_values['Z']:
        red_mask_chi = lambda x: "color: black"
        red_mask_ks = lambda x: "color: black"

    stats = {
        "Chi-square": [benf_test.chi_square, crit_chi],
        "Kolmogorov-Smirnov": [benf_test.KS, crit_ks],
        "Mean Absolute Deviation": [mad, f"{mad_list} *"],
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


def make_z_scores_df(benf_test):
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
        #.background_gradient(cmap="OrRd", subset="Z score of Found Proportions")