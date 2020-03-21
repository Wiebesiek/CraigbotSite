# Create your tasks here
from __future__ import absolute_import, unicode_literals
from craigbot.models import newBotRequest, craigBot
from craigbot.Utils.utils import create_search_url, create_query_string_data
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core.mail import send_mail
from celery.utils.log import get_task_logger
from CraigBotWebsite.celery import app
import requests

logger = get_task_logger(__name__)


@app.task
def create_bot(botreqid):
    """Creates bot in database and kickstarts initial webscrape"""
    try:
        bot_req: newBotRequest = newBotRequest.objects.get(req_id=botreqid)
    except newBotRequest.DoesNotExist:
        logger.info("Invalid botreqid supplied to create_bot")
        return
    # check if bot already exists. Only one bot_req per craigbot
    cb_result_set = craigBot.objects.filter(newBotReq=bot_req)
    if cb_result_set:
        logger.info("Bot already exitsts")
        return
    search_link = create_search_url(bot_req.city, bot_req.category)
    # if not a valid search_link we will punt for now and just return
    if not search_link:
        logger.info("Search link returned none")
        return
    # perform GET with prices and search query to query string
    data_qs = create_query_string_data(int(bot_req.price_min),
                                       bot_req.price_max,
                                       bot_req.search_query)
    page = requests.get(search_link, params=data_qs)
    new_cb = craigBot(newBotReq=bot_req,
                      item_found=False,
                      email_sent=False,
                      search_url=search_link,
                      price_min=bot_req.price_min,
                      price_max=bot_req.price_max,
                      search_query=bot_req.search_query,
                      hyperlink_for_result_found="",
                      owner=bot_req.owner, )

    # if page is not valid, we give up for now and let it try again later
    if page.status_code != 200:
        new_cb.save()
        bot_req.craig_bot = new_cb
        bot_req.save()
        return
    else:
        # now we search the page to see if there are valid results
        # we do this by simply searching for "no results"
        soup = BeautifulSoup(page.text, 'html.parser')
        no_results: str = soup.find(string="no results")
        if no_results:
            new_cb.save()
            bot_req.craig_bot = new_cb
            bot_req.save()
        else:
            new_cb.item_found = True
            if not new_cb.email_sent:
                if send_email(bot_req.owner, page.url):
                    new_cb.email_sent = True
                    new_cb.hyperlink_for_result_found = page.url
                    logger.info("Email Successfully Sent")
            new_cb.save()
            bot_req.craig_bot = new_cb
            bot_req.save()


# https://www.codementor.io/ankurrathore/asynchronous-task-with-rabbitmq-celery-and-django-8904ceway
@app.task
def send_email(user: User, url: str):
    logger.info("Sent email function ran.")
    return send_mail('Craigslist item found!',
                     url,
                     'AutoBot@craigbot.cc',
                     [user.email, ],
                     fail_silently=False)


@app.task
def scan_craigslist_with_bot():
    # get bots that need to be searched
    bot_list = craigBot.objects.filter(item_found=False)
    # TODO:RECENT CHANGE if no bots, lets log that there was nothing to search
    if len(bot_list) == 0:
        logger.info("No valid bots for scheduled scan.")
    # search craigslist for each bot and update bot.
    for bot in bot_list:
        search_link = bot.search_url
        data_qs = create_query_string_data(int(bot.price_min),
                                           bot.price_max,
                                           bot.search_query)
        page = requests.get(search_link, params=data_qs)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            no_results: str = soup.find(string="no results")
            if no_results:
                pass
            else:
                bot.item_found = True
                if not bot.email_sent:
                    if send_email(bot.owner, page.url):
                        bot.email_sent = True
                        bot.hyperlink_for_result_found = page.url
                        logger.info("Email Successfully Sent")
            bot.save()
