from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users import forms as user_forms
from craigbot import forms as craigbot_forms
from craigbot.Utils import form_helpers
from craigbot.models import newBotRequest, craigBot
from craigbot.tasks import create_bot


def edit(request, pk):
    bot: craigBot = get_object_or_404(craigBot, bot_id=pk)
    if request.method == 'POST':
        form = craigbot_forms.newBotRequestForm(data=request.POST)
        if form.is_valid():
            form_helper_tuple = form_helpers.new_craigbot_request_is_valid(form, request.user)
            if form_helpers.new_craigbot_request_is_valid(form, request.user)[0]:
                new_bot_req = newBotRequest(owner=request.user,
                                            city=form.cleaned_data.get('city'),
                                            category=form.cleaned_data.get('category'),
                                            search_query=form.cleaned_data.get('search_query'),
                                            price_min=form.cleaned_data.get('price_min'),
                                            price_max=form.cleaned_data.get('price_max'),
                                            )
                new_bot_req.save()
                create_bot.delay(new_bot_req.req_id)
                bot.delete()
                messages.success(request, 'Beep, Boop. Bot being forged!')
                return redirect('index')
            else:
                for bad_form_entry in form_helper_tuple[1]:
                    messages.warning(request, "Invalid entry for " + bad_form_entry)
                return redirect('index')
        else:
            messages.warning(request, 'Invalid Info')
            return redirect('index')

    else:
        form = craigbot_forms.newBotRequestForm(initial={'city': bot.newBotReq.city,
                                                         'category': bot.newBotReq.category,
                                                         'search_query': bot.newBotReq.search_query,
                                                         'price_min': bot.newBotReq.price_min,
                                                         'price_max': bot.newBotReq.price_max})
        return render(request, 'craigbot/edit_bot.html', {'form': form})


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'craigbot/index.html')
    else:
        return render(request, 'craigbot/u.html')


def login_view(request: HttpRequest):
    if request.method == 'POST':
        form = user_forms.CustomSigninForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}')
                return redirect('index')
            else:
                messages.warning(request, 'Invalid Login Info')
                return redirect(request, 'login')
        else:
            print(form.errors.as_data)
            for key in form.errors:
                messages.warning(request, form.errors[key])
            return redirect('login')

    else:
        form = user_forms.CustomSigninForm()
        return render(request, 'craigbot/login.html', {'form':form})


def logout_view(request: HttpRequest):
    logout(request)
    messages.info(request, 'Logout Successful')
    return redirect('index')


def about(request):
    return render(request, 'craigbot/about.html')


def create_new_bot(request: HttpRequest):
    if request.method == 'POST':
        form = craigbot_forms.newBotRequestForm(data=request.POST)
        if form.is_valid():
            form_helper_tuple = form_helpers.new_craigbot_request_is_valid(form, request.user)
            if form_helpers.new_craigbot_request_is_valid(form, request.user)[0]:
                new_bot_req = newBotRequest(owner=request.user,
                                            city=form.cleaned_data.get('city'),
                                            category=form.cleaned_data.get('category'),
                                            search_query=form.cleaned_data.get('search_query'),
                                            price_min=form.cleaned_data.get('price_min'),
                                            price_max=form.cleaned_data.get('price_max'),
                                            )
                new_bot_req.save()
                create_bot.delay(new_bot_req.req_id)
                messages.success(request, 'Beep, Boop. Bot being forged!')

                return redirect('index')
            else:
                for bad_form_entry in form_helper_tuple[1]:
                    messages.warning(request, "Invalid entry for " + bad_form_entry)
                return redirect('index')
        else:
            messages.warning(request, 'Invalid Info')
            return redirect('index')
    else:
        form = craigbot_forms.newBotRequestForm()
        return render(request, 'craigbot/createnewbot.html', {'form': form})


def view_bots(request: HttpRequest):
    bots_to_show = craigBot.objects.filter(owner=request.user)
    return render(request, 'craigbot/view_bots.html', {'bots': bots_to_show})
