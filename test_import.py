import recommender
print('imported ok')

try:
    df = recommender.load_data()
    print('loaded', len(df), 'rows')
except Exception as e:
    print('error during load:', e)
