from tools.search import web_search_tool

results = web_search_tool.invoke({
    "query": "Careem company services and business operations",
    "max_results": 5
})

print(results)