FROM python:3.8.10-slim

LABEL maintainer="Marcel Milcent"
LABEL version="0.1.0"
LABEL maintainer-email="marcelmilcent@gmail.com"

COPY . /benford-streamlit

WORKDIR /benford-streamlit

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["benford_analysis.py"]

