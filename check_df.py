import recommender

df = recommender.load_data()
print('columns:', df.columns.tolist()[:20])
print('title head:', df['title'].head())
