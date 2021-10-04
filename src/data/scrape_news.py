#%%
import pandas as pd
from newspaper import Article

#%%
df = pd.read_json('./GermanFakeNC/GermanFakeNC.json')
# %%
df.head()
# %%
df.describe()
# %%
overall_rating_mask = df['Overall_Rating'] >= 0.6
# %%
ratio_mask = df['Ratio_of_Fake_Statements'].isin([3, 4])
# %%
df_fake = df[overall_rating_mask & ratio_mask].reset_index()
print(df_fake.shape)
# %%
df_fake.loc[0, 'URL']
#%%
def extract_title(url):
    article = Article(url)
    try:
        article.download()
        print('Article title downloaded from %s' % url)
        article.parse()
    except:
        article.title = 'No title'

    return article.title

#%%
def extract_text(url):
    article = Article(url)
    try:
        article.download()
        print('Article text downloaded from %s' % url)
        article.parse()
    except:
        article.text = 'No text'

    return article.text

# %%
df_fake['titel'] = df_fake['URL'].apply(extract_title)
df_fake['text'] = df_fake['URL'].apply(extract_text)

# %%
df_fake.head(20)
# %%
df_fake_final = df_fake[df_fake['titel'] != 'No title']
# %%
df_fake_final.shape
# %%
df_fake_final.head()
#%%
df_fake_final.isnull().sum()
#%%
df_fake_final.dtypes
#%%
#%%
df_fake_final['Date'].fillna(pd.to_datetime('1/1/2016'), inplace=True)
#%%
df_fake_final.isnull().sum()
# %%
df_fake_final.to_csv('GermanFakeNC_prep.csv', index=False)
# %%
