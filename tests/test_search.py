from tools.search import search_web


results = search_web(
    query="Careem company services and business operations",
    max_results=5
)

for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print("Title:", result.get("title"))
    print("URL:", result.get("url"))
    print("Content:", result.get("content"))