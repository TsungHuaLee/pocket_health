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

Line_Access_Token = settings.LINE_ACCESS_TOKEN
channel_secret = settings.CHANNEL_SECRET

line_bot_api = LineBotApi(Line_Access_Token)
handler = WebhookHandler(channel_secret)
parser = WebhookParser(channel_secret)


@csrf_exempt
def callback(request):
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body_decode = request.body.decode('utf-8')
        try:
            events  = parser.parse(body_decode, signature)
            for event in events:
                print(event)
                print(event.postback)
                if (event.type == "postback"):
                    timestamp = event.timestamp
                    source = event.source
                    reply_token  = event.reply_token
                    data = event.postback.data
                    response_file_name = os.path.join('json_file', data+'.txt')
                    if(os.path.exists(response_file_name)):
                        reply_button(reply_token , response_file_name)
                    else:
                        line_bot_api.reply_message(reply_token,TextSendMessage(text='我不知道要回答什麼'))
                elif (event.type == "message"):
                    message = str(event.message.text)
                    line_bot_api.reply_message(reply_token,TextSendMessage(text=message))
            return HttpResponse()
        except InvalidSignatureError:
            print('InvalidSignatureError')
            return HttpResponseBadRequest()
    else:
        print('HttpResponseBadRequest!')
        return HttpResponseBadRequest()

def reply_button(replyToken, file_name):
    import requests
    import json
    with open(file_name, 'r', encoding="UTF-8") as f:
        template = json.loads(f.read())
    f.close()
    url = 'https://api.line.me/v2/bot/message/reply'
    header_payload = {
        'Content-Type': 'application/json',
        'Authorization' : 'Bearer ' + Line_Access_Token
    }
    body_payload ={
        "replyToken":replyToken,
        "messages":[template]
    }
    r = requests.post(url, data=json.dumps(body_payload), headers=header_payload)
    