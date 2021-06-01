# benford-streamlit

## Interactive Benford Dashboard

This project brings [`benford_py`](https://github.com/milcent/benford_py),  [`benfordviz`](https://github.com/milcent/benfordviz), and [`streamlit`](https://streamlit.io/) together in an interactive Benford Analysis.

### Citing

If you find *`benford-streamlit`* useful in your research, please consider adding the following citation:

```bibtex
@misc{benford-streamlit,
      author = {Marcel, Milcent},
      title = {{benford-streamlit: an Interactive Benford Dashboard}},
      year = {2021},
      publisher = {GitHub},
      journal = {GitHub repository},
      howpublished = {\url{https://github.com/milcent/benford-streamlit}},
}
```

## Version 0.1.0

### Python versions and dependencies

This implementation has been tested in python versions `3.7.9` and `3.8.10`, and with `streamlit` versions `0.68` and `0.82`. The most important configuration is letting `bokeh` in version `2.2.2` (not the most recent), as the charts for some reason do not show with 2.3.2. Setting up the environment with `requirements.txt` file should work fine.

## Installation

Clone the repo and go into the recently created `benford-streamlit` folder:

```bash
git clone https://github.com/milcent/benford-streamlit.git
cd benford-streamlit
```

### `venv` and `pip`

Create an virtual environment for the repo:

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

But `streamlit`, `benford-py`, and `benfordviz` must be installed with `pip` anyway, so you will have to use it in this last part:

```bash
pip install streamlit benford-py benfordviz
```

### Launching the interactive analysis through `streamlit` after setup

```bash
streamlit run benford-analysis.py
```

If your browser does not open automatically, open it and go to [http://localhost:8501](http://localhost:8501).

### `Docker`

I have also created a `Docker` container with the interactive app in it ready to go:

###########COLOCAR-DOCKER

## Analysis

