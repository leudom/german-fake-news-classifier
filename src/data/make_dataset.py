# -*- coding: utf-8 -*-
# %%
import os
import logging
from dotenv import find_dotenv, load_dotenv
import pandas as pd

# Functions


def prepare_news_csv(filepath):
    """ 
    1.) Drop columns -> Kategorie, Quelle, Art
    2.) Check on duplicate Titel and Body and drop the first entry of duplicates
    3.) Rename Columns in order to match it with the other dataset (GermanFakeNC)
    4.) Add column source_name with news_csv to identifiy the source of a row after merging
    """

    # Read news.csv from disk
    _df = pd.read_csv(filepath)
    logger.debug(_df.info())
    # Drop cols
    logger.info('Null values in news.csv: \n%s' % _df.isnull().sum())
    cols_to_drop = ['Kategorie', 'Quelle', 'Art']
    _df.drop(cols_to_drop, axis=1, inplace=True)
    logger.info('Cols %s dropped' % cols_to_drop)


    # Drop duplicates
    logger.info('Percent duplicated Titel and Body: \n%s' % str(
        _df.duplicated(subset=['Titel', 'Body']).value_counts(normalize=True)))
    _df.drop_duplicates(subset=['Titel', 'Body'], inplace=True)
    logger.info('Duplicates in Titel and Body dropped')

    # Rename Cols
    new_cols = {'id': 'src_id',
                'Titel': 'title',
                'Body': 'text',
                'Datum': 'date',
                'Fake': 'fake'}
    _df.rename(columns=new_cols, inplace=True)
    logger.info('Cols renamed')

    # Add col source_name
    _df['src_name'] = 'news_csv'

    return _df


def prepare_germanfake(filepath):
    """ 
    1.) Drop columns -> [False_Statement_1_Location,
                         False_Statement_1_Index,
                         False_Statement_2_Location,
                         False_Statement_2_Index,
                         False_Statement_3_Location,
                         False_Statement_3_Index,
                         Ratio_of_Fake_Statements,
                         Overall_Rating]
        We treat all entries as fakenews, eventhough there are some instances
        that have a very low fake overall ratings!!
    2.) Make index source_id
    3.) Check on duplicate titel and text and drop the first entry of duplicates
    4.) Drop rows where titel or text is null 
    5.) Fill Dates for missing values -> From the URL we can see that the Date could
        be 2017/12 
    6.) Rename Columns in order to match it with the other dataset (news.csv)
    7.) Add label col 'fake' = 1 -> all 1; col 'src_name' = 'GermanFakeNC'
    """

    # Read news.csv from disk
    _df = pd.read_csv(filepath)
    logger.debug(_df.info())
    # Drop cols
    logger.info('Null values in GermanFakeNC_interim.csv: \n%s' % _df.isnull().sum())
    cols_to_drop = ['False_Statement_1_Location',
                    'False_Statement_1_Index',
                    'False_Statement_2_Location',
                    'False_Statement_2_Index',
                    'False_Statement_3_Location',
                    'False_Statement_3_Index',
                    'Ratio_of_Fake_Statements',
                    'Overall_Rating']
    _df.drop(cols_to_drop, axis=1, inplace=True)
    logger.info('Cols %s dropped' % cols_to_drop)

    # Set source_id
    _df.reset_index(inplace=True)
    logger.info('Index reset')
    
    # Drop duplicates
    logger.info('Percent duplicated titel and text: \n%s' % str(
        _df.duplicated(subset=['titel', 'text']).value_counts(normalize=True)))
    _df.drop_duplicates(subset=['titel', 'text'], inplace=True)
    logger.info('Duplicates in titel and text dropped')

    # Drop rows where titel or text is null
    _df.dropna(subset=['titel', 'text'], inplace=True)
    logger.info('Null rows for titel and text dropped')

    # Fill the missing dates
    _df['Date'].fillna(pd.to_datetime('01/12/2017'), inplace=True)

    # Rename Cols
    new_cols = {'index': 'src_id',
                'titel': 'title',
                'Date': 'date',
                'URL': 'url'}
    _df.rename(columns=new_cols, inplace=True)
    logger.info('Cols renamed')

    # Add col source_name
    _df['fake'] = 1
    _df['src_name'] = 'GermanFakeNC'

    return _df


def merge_datasets(df_1, df_2):
    logger.info('Shape: %s\n Columns: %s' % (df_1.shape, df_1.columns))
    logger.info('Shape: %s\n Columns: %s' % (df_2.shape, df_2.columns))
    # Check col names
    sym_diff = set(df_1).symmetric_difference(set(df_2))
    assert len(sym_diff) == 0 , 'Differences in colnames of the two datasets'
    return pd.concat([df_1, df_2], axis=0, ignore_index=True)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s : %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger()

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    NEWS_CSV = os.path.join(os.getenv('PROJECT_DIR'), 'data', 'raw', 'news.csv')
    GERMAN_FAKE_NC = os.path.join(os.getenv('PROJECT_DIR'), 'data', 'interim', 'GermanFakeNC_interim.csv')
    OUTPUT = os.path.join(os.getenv('PROJECT_DIR'), 'data', 'processed', 'fake_news_processed.csv')

    df_news = prepare_news_csv(NEWS_CSV)
    df_gfn = prepare_germanfake(GERMAN_FAKE_NC)
    df_merged = merge_datasets(df_news, df_gfn)

    try:
        df_merged.to_csv(OUTPUT, sep=';', index=False)
        logger.info('Final dataset prepared and saved to %s' % OUTPUT)
    except Exception:
        logger.exception('File could not be daved to disk\n', exc_info=True )
    
