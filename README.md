# benford-streamlit

## Interactive Benford Analysis App

This project brings [`benford_py`](https://github.com/milcent/benford_py),  [`benfordviz`](https://github.com/milcent/benfordviz), and [`streamlit`](https://streamlit.io/) together in an interactive Benford Analysis.

### Citing

If you find *`benford-streamlit`* useful in your research, please consider adding the following citation:

```bibtex
@misc{benford-streamlit,
      author = {Marcel, Milcent},
      title = {{benford-streamlit: an Interactive Benford Analysis App}},
      year = {2021},
      publisher = {GitHub},
      journal = {GitHub repository},
      howpublished = {\url{https://github.com/milcent/benford-streamlit}},
}
```

## Version 0.1.0

### Python versions and dependencies

This implementation has been tested in python versions `3.7.9` and `3.8.10`, and with `streamlit` versions `0.68` and `0.82`. The most important configuration is letting `bokeh` in version `2.2.2` (not the most recent), as the charts for some reason do not show with 2.3.2. Setting up the environment with the`requirements.txt` file should work fine.

## Installation

Clone the repo and go into the recently created `benford-streamlit` folder:

```bash
git clone https://github.com/milcent/benford-streamlit.git
cd benford-streamlit
```

### `venv` and `pip`

Create a virtual environment for the repo:

```bash
python -m venv venv
```

Acivate the environment

- On windows:

```powershell
./venv/Scripts/activate
```

- On Linux / Mac:

```bash
source venv/bin/activate
```

Update pip and install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### `conda`

If you use conda, setting up an environment with it has also worked:

```bash
conda env create -n benford-streamlit
conda activate benford-streamlit
conda install pandas bokeh=2.2.2
```

But `streamlit`, `benford_py`, and `benfordviz` must be installed with `pip` anyway, so you will have to use it in this last part:

```bash
pip install streamlit benford_py benfordviz
```

### Launching the interactive analysis through `streamlit` after setup

```bash
streamlit run benford-analysis.py
```

A message lik the one bellow will appear:

```bash
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://255.168.1.2:8501
```

If your browser does not open automatically, open it and go to [http://localhost:8501](http://localhost:8501).

### `Docker`

I have also created a `Docker` container with the interactive app in it ready to go:

###########COLOCAR-DOCKER

## Analysis

The first option is the file selector, with which you choose the file to upload. As of now, it supports only `.csv` files, and make sure yours really uses commas (`,`) as separators.

![File_uploader](figures/00_file_upload.png)

Next up, select the column you want to analyse. You can change it at any time. Just remember to choose a numeric column. `benford_py`, and `pandas` for that matter, will try to convert numeric columns loaded as strings, but it is not guaranteed.

![Column_selector](figures/01_column_selector.png)

While you do not choose a column with the right `dtype`, the message below will be on.

![Proper_Column_Warning](figures/02_waiting_column.png)

Then, you must choose the sign of the records you want to analyse. Under the hood, `benford_py` will turn all number to their absolute values, but you may want to run your analyses only on the positive or negative records (defaults to all).

![Sign_selector](figures/03_choose_sign.png)

A message similar to the one beloow will show on the top right side if your data has negative numbers and you choose only the positive ones.

![Positive_selection](figures/05_positive_sign_selection.png)

The next selector is the decimal places one. `benford_py` lets you tune this paramenter based on the type of data tou have. The default is `2`, for currencies, but you may need to decrease it down to `0`, when dealing with integers, or increase it, when analysing really small numbers, with lots of decimal places, such as log-returns of a stock.

![Decimal_selector](figures/04_choose_decimals.png)

If you know your data, though, this parameter should be properly set and forgotten. Having sad that, dependent on the Benford Test you choose to apply to the dataset, you will be informed how many, if any, records were discarded from the analysed sample due to your decimal places choice.

![Decimal_discarded](figures/06_decimal_selection.png)

Getting closer now! You will choose the Benford Test to apply in the next dropdown.

![Test_selector](figures/07_test_selector.png)

The analysis covers the:

- First Digit Test;
- Second Digit Test;
- First Two Digits Test;
- First Three Digits Test; and
- Last Two Digits Test.

The final selector in the sidebar is the `confidence` one. Some of the statistics computed in the tests (Chi-square, Kolmogorov-Smirnov, Z scores) need a confidence level set, so there can be critical values to compared the findings with.

![Confidece_selector](figures/08_confidence_selector.png)