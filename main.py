import requests

api_key = 'Enter Your API Key'
search_engine_id = 'ENter your Search ENGINE_ID'
query = 'memory leaks'

def google_search(query, api_key, search_engine_id):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={search_engine_id}"
    response = requests.get(url)
    return response.json()

results = google_search(query, api_key, search_engine_id)

for item in results.get('items', []):
    print(f"Title: {item['title']}")
    print(f"Link: {item['link']}")
    print(f"Snippet: {item['snippet']}\n")

with open('search_results.txt', 'w') as file:
    for item in results.get('items', []):
        file.write(f"Title: {item['title']}\n")
        file.write(f"Link: {item['link']}\n")
        file.write(f"Snippet: {item['snippet']}\n\n")
