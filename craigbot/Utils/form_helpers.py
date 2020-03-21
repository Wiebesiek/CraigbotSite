from craigbot import forms as craigbot_forms
from django.contrib.auth.models import User
from urllib import request, error
from bs4 import BeautifulSoup
import requests


# checks if request is valid on the craigslist website, returns a pair
# of values. Where the first value is a boolean if it is a valid request.
# If the request is invalid the second item, will be a tuple of values
# representing the invalid values.
def new_craigbot_request_is_valid(form: craigbot_forms.newBotRequestForm,
                                  user: User):
    ret_val_boolean: bool = True
    invalid_arguments: tuple = ()

    city = form.cleaned_data.get('city')
    category = form.cleaned_data.get('category')
    price_min = form.cleaned_data.get('price_min')
    price_max = form.cleaned_data.get('price_max')

    # currently not processing search_query
    if not valid_craigslist_city(city):
        ret_val_boolean = False
        invalid_arguments += ('city',)
    if not bool(valid_craigslist_category(category)):
        ret_val_boolean = False
        invalid_arguments += ('category',)
    if price_max <= price_min:
        ret_val_boolean = False
        invalid_arguments += ('price')

    print(ret_val_boolean)
    print(form)
    return ret_val_boolean, invalid_arguments

def valid_craigslist_city(city: str) -> bool:
    url = "https://" + city + ".craigslist.org"
    # try/except for invalid cities
    try:
        req: request = request.urlopen(url)
        req_code = req.getcode()

    except error.URLError:
        req_code = -1

    if req_code == 200:
        return True
    else:
        return False

# returns BeautifulSoup object, if valid. otherwise None
def valid_craigslist_category(category: str) -> BeautifulSoup:
    # default to Portland craigslist to see if valid category
    tag = get_search_category_from_city("portland", category)
    return tag


# searches city page and finds BeautifulSoup of search category
def get_search_category_from_city(city: str, category: str) -> BeautifulSoup:
    url = "https://" + city + ".craigslist.com"
    try:
        page = requests.get(url)
    except error.URLError:
        return None
    soup = BeautifulSoup(page.content,'html.parser')
    center = soup.find("div", id="center")
    return center.find(string=category)


