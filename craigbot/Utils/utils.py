from craigbot.Utils.form_helpers import get_search_category_from_city
from bs4 import BeautifulSoup


# returns a url to POST search query to
def create_search_url(city: str,
                      category: str) -> str:
    soup: BeautifulSoup = get_search_category_from_city(city, category)
    # soup will more than likely be a navigableString
    # to get href, we have to traverse up
    par = soup.find_parent('a', href=True)
    if par:
        href = par['href']
        base_url = "https://" + city + ".craigslist.org"
        return base_url + href
    else:
        return None


# creates a dictionary for query string data to be supplied
# to the "create_search_url"
def create_query_string_data(price_min: int, price_max: int, search_query: str):
    # Need to replace " " with "+"  ---don't know if this is necessary---
    search_query_value = search_query.replace(" ", "+")
    # search_query_value = search_query
    if (not price_min) and (not price_max):
        return {"query": search_query_value}
    if not price_min:
        return {"max_price": price_max, "query": search_query_value}
    return {"min_price": price_min, "max_price": price_max, "query": search_query_value}
