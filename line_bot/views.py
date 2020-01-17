#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from django.shortcuts import render
import json,requests
import pandas as pd
from django.http import JsonResponse
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,HttpResponseServerError
from django.http import HttpRequest, HttpResponse
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage, TemplateSendMessage, ConfirmTemplate
from linebot.models import PostbackAction, MessageAction
from django.conf import settings
import os

import base64
import hashlib
import hmac

Line_Access_Token = settings.Line_Access_Token
channel_secret = settings.Channel_Secret

line_bot_api = LineBotApi(Line_Access_Token)
handler = WebhookHandler(channel_secret)
parser = WebhookParser(channel_secret)


@csrf_exempt
def callback(request):
    
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body_decode = request.body.decode('utf-8')
        # msg = json.loads(body_decode)
        body = json.loads(body_decode)
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            print('InvalidSignatureError')
            return HttpResponseBadRequest()
    else:
        print('HttpResponseBadRequest!')
        return HttpResponseBadRequest()

def reply_button(replyToken, file_name):
    import requests
    import json
    line_ace = access_token
    with open(file_name, 'r', encoding="UTF-8") as f:
        template = json.loads(f.read())
    f.close()
    url = 'https://api.line.me/v2/bot/message/reply'
    header_payload = {
        'Content-Type': 'application/json',
        'Authorization' : 'Bearer ' + line_ace
    }
    body_payload ={
        "replyToken":replyToken,
        "messages":[template]
    }
    r = requests.post(url, data=json.dumps(body_payload), headers=header_payload)
    