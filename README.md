german_fake_news_classifier
==============================

## Overview
> **This repo was fully migrated to https://dagshub.com/leudom/german-fake-news-classifier. Further development will take place there!**

This repo is about classifying german news/fake-news. The objective is to train a binary classifier that is capable of classifying news articles into fake and non-fake. This repo provides a stack for
* Experiments and Collaboration (Dagshub - https://dagshub.com/leudom/german-fake-news-classifier)
* Model and Data Versioning (dvc)
* ML Pipelines (dvc)
* Deployment of Endpoints in Azure (Azure ML)

All those functionalities are provided in a template-wise manner for you in order to to kick-off your own project or - even better - contribute to this repo ;-)

A few words regarding the data we used her to train our model(s):

For training a model we currently use 2 Datasources. One datasource stem from Kaggle (https://www.kaggle.com/kerneler/starter-fake-news-dataset-german-9cc110a2-9/data). This dataset is a collection of news (non-fake) and fake-news, whereas fake news are derived from satire online editors like "Die Tagespresse" or "Der Postillion". This way, sarcastic news articles are treated as fake news in this dataset. (see EDA on that dataset --> notebooks/01-eda-german-fake-news.ipynb)

The second source for fake news is a dataset from Inna Vogel and Peter Jiang (2019)*. Thereby, Every fake statement in the text was verified claim-by-claim by authoritative sources (e.g. from local police authorities, scientific studies, the police press office, etc.). The time interval for most of the news is established from December 2015 to March 2018.


*Fake News Detection with the New German Dataset "GermanFakeNC". In Digital Libraries for Open Knowledge - 23rd International Conference on Theory and Practice of Digital Libraries, TPDL 2019, Oslo, Norway, September 9-12, 2019, Proceedings (pp. 288–295).

## Reproducing the Project and Contributing

1. Fork the repo on GitHub
2. Clone the project to your own machine
3. Experiment and commit changes to your own branch
4. Push your work back up to your fork
5. Submit a Pull request so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

For reproduction consider the following:
1. Check out all the *.example files in order to get your env and credentials set up
2. Become familiar with the dvc workflow (in combination with git)


## Project Organization
    .
    ├── LICENSE
    ├── .azureml                <- Store Azure specific configurations
    ├── README.md               <- The top-level README for developers using this project.
    ├── anaconda-project.yml
    ├── bin
    │   └── models              <- Trained and serialized models (model.pkl)
    ├── data
    │   ├── external            <- Data from third party sources.
    │   ├── interim             <- Intermediate data that has been transformed.
    │   ├── processed           <- The final, canonical data sets for modeling.
    │   └── raw                 <- The original, immutable data dump.
    ├── dvc.lock
    ├── dvc.yaml
    ├── envs
    │   ├── fake_news_env
    │   └── inference_env
    │── .env                    <- Env file to store env specific and/or private variables
    ├── metrics.csv
    ├── notebooks               <- Jupyter notebooks. Naming convention is a number
    ├── params.yml
    ├── references
    ├── reports                 <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures             <- Generated graphics and figures to be used reporting
    └── src                     <- Source code for use in this project.
        ├── __init__.py         <- Makes src a Python module
        ├── data                <- Scripts to download or generate data
        ├── features            <- Scripts to turn raw data into features for modeling
        ├── models              <- Scripts to train, evaluate, test and deploy models
        └── visualization       <- Scripts to create exploratory and results oriented viz


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
