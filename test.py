from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights

res = search_flights("Plane a 10 days palne from Delhi to japan")

print(res)

# res=tavily_search("Best hotel in hyderabad for bitiyani")
# print(res)