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

count = 0; score = 0

@csrf_exempt
def callback(request):
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body_decode = request.body.decode('utf-8')
        try:
            events = parser.parse(body_decode, signature)
            for event in events:
                timestamp = event.timestamp
                source = event.source
                reply_token  = event.reply_token
                if (event.type == "postback"):
                    print("event: ", event, ", postback data: ", event.postback.data)    
                    data = event.postback.data
                    response_file_name = os.path.join('json_file_v2', data+'.txt')
                    if(os.path.exists(response_file_name)):
                        reply_button(reply_token , response_file_name)
                    else:
                        if(data.startswith('assessment_s1o2_s2o2')):
                            print("startswith assessment_s1o2_s2o2")
                            startPhsyAssessment(reply_token, data)
                            return
                        line_bot_api.reply_message(reply_token,TextSendMessage(text='抱歉我還在學習中，請換個方式跟我說'))
                elif (event.type == "message"):
                    message = str(event.message.text)
                    if (message.startswith('貼圖')):
                        response_file_name = os.path.join('json_file_v2', 'sticker_json.txt')
                        reply_button(reply_token, response_file_name)
                    if (message.startswith('我想知道')):
                        response_file_name = os.path.join('json_file_v2', 'hypertension_articles.txt')
                        reply_button(reply_token , response_file_name)
            return HttpResponse()
        except InvalidSignatureError:
            print('InvalidSignatureError')
            return HttpResponseBadRequest()
    else:
        print('HttpResponseBadRequest!')
        return HttpResponseBadRequest()

def reply_button(replyToken, file_name):
    print("------------------- Start send reply button -------------------")
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
    print(body_payload)
    print("------------------- End send reply button -------------------")
    
def startPhsyAssessment(reply_token, data):
    global count
    global score
    sum_score(data)
    count += 1

    print("in startPhsyAssessment, score: ", str(score), ", count: " + str(count))

    if(count <= 5):
        response_file_name = os.path.join('json_file_v2', 'assessment_s1o2_s2o2_s3_' + str(count) + '.txt')
        reply_button(reply_token , response_file_name)
    else:
        if(score <= 3):
            response_file_name = os.path.join('json_file_v2', 'score_s1.txt')
        elif(3 < score <= 6):
            response_file_name = os.path.join('json_file_v2', 'score_s2.txt')
        elif(6 < score <= 9):
            response_file_name = os.path.join('json_file_v2', 'score_s3.txt')
        elif(9 < score <= 12):
            response_file_name = os.path.join('json_file_v2', 'score_s4.txt')
        elif(score > 12):
            response_file_name = os.path.join('json_file_v2', 'score_s5.txt')
        else:
            response_file_name = os.path.join('json_file_v2', 'score_s1.txt')

        count = 0
        score = 0

        # reply
        if(os.path.exists(response_file_name)):
            reply_button(reply_token , response_file_name)
        else:
            line_bot_api.reply_message(reply_token,TextSendMessage(text='抱歉我還在學習中，請換個方式跟我說'))

def sum_score(data):
    global score
    if(data == "assessment_s1o2_s2o2_s3o1"):
        score += 0
    elif (data == "assessment_s1o2_s2o2_s3o2"):
        score += 1
    elif data == "assessment_s1o2_s2o2_s3o3":
        score += 2
    elif data == "assessment_s1o2_s2o2_s3o4":
        score += 3
    