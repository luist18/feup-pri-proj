#%%
import requests

SELECT_URL = 'http://localhost:5002/solr/movies/select'

def abc():    
    params = {
        'q': 'text:constituicao'
    }

    result = requests.get(SELECT_URL, params=params)
    return result.json()

#%%
results = abc()
print(results)