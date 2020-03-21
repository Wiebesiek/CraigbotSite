from django.http import HttpRequest, HttpResponse
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from craigbot.models import craigBot
import json


def delete_bot(request: HttpRequest):
    if request.method == 'POST':
        bot_to_delete_id = request.POST.get('bot_id')
        bot_to_delete = craigBot.objects.get(bot_id=bot_to_delete_id)
        if bot_to_delete.owner == request.user:
            # craigBot.objects.filter(bot_id=bot_to_delete_id).delete()
            if bot_to_delete.delete():
                messages.success(request, 'Bot Deleted')
            print("delete_bot method.. deleting bot " + bot_to_delete_id)
            data = {
                'msg': render_to_string('craigbot/messages.html', {}, request, ),
            }
            messages.success(request, 'Bot Deleted')
            # return render_to_json(request, data)
            return JsonResponse(data)
        else:
            raise Http404
    else:
        raise Http404


# `data` is a python dictionary
def render_to_json(request, data):
    return HttpResponse(
        json.dumps(data, ensure_ascii=False),
        mimetype=request.is_ajax() and "application/json" or "text/html"
    )
