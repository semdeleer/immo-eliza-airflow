# immo-eliza-ml
[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
![pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![vsCode](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-007A88?style=for-the-badge&logo=Apache+Airflow&logoColor=white)




## 📖 Description
This project combines several individual real estate (immo) projects into a cohesive automation framework utilizing Apache Airflow. 
The component projects are:
- [immo-eliza-scraping-immozila](https://github.com/NathNacht/immo-eliza-scraping-immozila.git)
- [immo-eliza-scraping-immozila-Cleaning-EDA](https://github.com/NathNacht/immo-eliza-scraping-immozila-Cleaning-EDA.git)
- [immo-eliza-ml](https://github.com/semdeleer/immo-eliza-ml.git)
- [immo-eliza-deployment](https://github.com/semdeleer/immo-eliza-deployment.git)

The objective of this unified project is to automate the process of scraping, cleaning, and modeling data from the immoweb website to enable price prediction.



## 🛠 Installation

* clone the repo
```bash
git git@github.com:semdeleer/immo-eliza-airflow.git
```

* Install all the libraries in requirements.txt
```bash
pip install -r requirements.txt
```

* Run the docker file
```bash
$ docker compose --build
```
* Now everything shoulc be automated in a docker enviroment

## 🤖 Project File structure
```
C:.
│   .dockerignore
│   .env
│   .gitignore
│   docker-compose.yaml
│   dockerfile
│   README.md
│   requirements.txt
│
├───config
├───dags
│   │   cleaning.py
│   │   welcome_dag.py
│   │
│   ├───immoweb
│   │   │   test.txt
│   │   │   __init__.py
│   │   │
│   │   ├───data
│   │   │   ├───clean
│   │   │   │       clean_app.csv
│   │   │   │       clean_app2.csv
│   │   │   │       clean_house.csv
│   │   │   │       clean_house2.csv
│   │   │   │
│   │   │   └───raw
│   │   │           georef-belgium-postal-codes.csv
│   │   │           raw_apartement_te_koop.csv
│   │   │           raw_huis_te_koop.csv
│   │   │           zipcodes_alpha_nl_new.csv
│   │   │
│   │   ├───model
│   │   │   │   model_pickle_b2
│   │   │   │   trainb.py
│   │   │   │
│   │   │   └───__pycache__
│   │   │           trainb.cpython-312.pyc
│   │   │           trainb.cpython-37.pyc
│   │   │
│   │   ├───pipeline
│   │   │   │   clean.py
│   │   │   │   __init__.py
│   │   │
│   │   ├───scraper
│   │   │       immospider.py
│   │   │       scraper.py
│   │   │       weblinks.py
│
├───logs
│   └───scheduler
│       
└───plugins
```


## 🔍 Contributors
- [Sem Deleersnijder](https://github.com/semdeleer)

## 📜 Timeline

This project was created in 5 days.