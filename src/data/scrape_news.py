# -*- coding: utf-8 -*-
import logging
import os
from dotenv import find_dotenv, load_dotenv
import pandas as pd
from newspaper import Article

# Functions


def extract_title(url):
    article = Article(url)
    try:
        article.download()
        logger.info('Article title downloaded from %s' % url)
        article.parse()
    except:
        article.title = 'No title'

    return article.title


def extract_text(url):
    article = Article(url)
    try:
        article.download()
        logger.info('Article text downloaded from %s' % url)
        article.parse()
    except:
        article.text = 'No text'

    return article.text


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger()

    # Load .env file
    load_dotenv(find_dotenv())

    INPUTFILE = os.path.join(os.getenv('PROJECT_DIR'),
                             'data',
                             'raw',
                             'GermanFakeNC.json')

    INTERIMFILE = os.path.join(os.getenv('PROJECT_DIR'),
                               'data',
                               'interim',
                               'GermanFakeNC_interim.csv')

    df = pd.read_json(INPUTFILE)
    logger.info('Head of dataframe: \n%s' % df.head())

    # %% We only take News with an overall rating of at least 0.5
    #overall_rating_mask = df['Overall_Rating'] >= 0.5
    ##ratio_mask = df['Ratio_of_Fake_Statements'].isin([3, 4])
    #df_fake = df[overall_rating_mask & ratio_mask].reset_index()

    df['titel'] = df['URL'].apply(extract_title)
    df['text'] = df['URL'].apply(extract_text)

    logger.info('Head of dataframe after parsing: \n%s' % df.head())

    # Create mask to filter rows with no information (titel or text)
    no_info_mask = (df['titel'] != 'No title') | (df['text'] != 'No text')
    df_final = df[no_info_mask]

    logger.info('Shape of final dataframe: %s' % str(df_final.shape))
    logger.info('dtypes: \n%s' % str(df_final.dtypes))
    logger.info('Rows with null values: \n%s' % df_final.isnull().sum())

    # Save as csv
    try:
        df_final.to_csv(INTERIMFILE, index=False)
        logger.info("CSV was saved to disk")
    except Exception:
        logger.exception("Couldn't save CSV to disc \n", exc_info=True)
