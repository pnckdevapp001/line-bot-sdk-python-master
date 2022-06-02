# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.


import datetime
import errno
import json
import os
import sys
import tempfile
import re
import requests
import random
from googletrans import Translator
import http.client
from bs4 import BeautifulSoup
from pornhub_api import PornhubApi
api = PornhubApi()
api.stars.all()
#from pyngrok import ngrok

#ngrok.set_auth_token("29v8FNXJGbnKw3ujusg71Zu2ciX_4K4YJYzSDSJxFWxc37oos")

#ngrok.connect(5000)

from argparse import ArgumentParser

from flask import Flask, request, abort, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage,VideoSendMessage)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

# get channel_secret and channel_access_token from your environment variable
channel_secret = "62e9015c564529ac5c3dafe828ccfef5"
channel_access_token = "mIOW7SSdWZHTbrFq9ZZBQdytyb5JO9KaCYT9A6uzw/FHdu8nuusFh2YnNLIf/qt+TdWEPDo0DpDKZzCn8yZknNsOWBrG3gmgNt01s2lkfs4T6UBzhXTmI9Al7ERMPr0o+0obosBIgZdVVEt9vx6TGgdB04t89/1O/w1cDnyilFU="
if channel_secret is None or channel_access_token is None:
    print('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

def trans(texttr):
    translator = Translator()
    translations = translator.translate(texttr,src='auto',dest='th')
    #print(translations.text)
    return translations.text

def url_match(urlX):
    try:
        videopath = urlX.split("$")[1]
        print(videopath)
        return videopath
    except:
        return urlX

# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text

    if text == 'profile':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Display name: ' + profile.display_name),
                    TextSendMessage(text='Status message: ' + str(profile.status_message))
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
    elif text == 'emojis':
        emojis = [
            {
                "index": 0,
                "productId": "5ac1bfd5040ab15980c9b435",
                "emojiId": "001"
            },
            {
                "index": 13,
                "productId": "5ac1bfd5040ab15980c9b435",
                "emojiId": "002"
            }
        ]
        text_message = TextSendMessage(text='$ LINE emoji $', emojis=emojis)
        line_bot_api.reply_message(
            event.reply_token, [
                text_message
            ]
        )
    elif re.search(r'avfreex24\.com', text.lower()):
        #label = "JAV"
        APIAV = ["https://mgzyz1.com/api.php/provide/vod/?ac=detail&pg="+str(random.randint(1,100)),"https://apilj.com/api.php/provide/vod/at/json/?ac=detail&pg="+str(random.randint(1,100))]
        url = requests.get(random.choice(APIAV))
        text = url.text
        data = json.loads(text)
        avdata = data['list'][random.randint(1,19)]
        # x_vod_id = str(avdata['vod_id'])
        x_vod_pic = avdata['vod_pic']
        if x_vod_pic.startswith("http://"):
            x_vod_pic = x_vod_pic.replace("http://", "https://")
        x_vod_name_Th = trans(avdata['vod_name'])
        x_vod_name = avdata['vod_name']
        #x_vod_time = avdata['vod_time']
        x_type_name_Th = trans(avdata['type_name'])
        # x_vod_score = str(avdata['vod_score'])
        vpath = url_match(avdata['vod_play_url'])
        #flexJav={"type": "bubble", "size": "kilo", "body":{"type": "box", "layout": "vertical", "contents": [{"type": "video", "url": vpath, "previewUrl": vpath, "altContent":{"type": "image", "size": "full", "aspectRatio": "1:1", "aspectMode": "cover", "url": x_vod_pic}},{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "AVFREEX24.COM", "size": "xxs", "color": "#ff0000"}], "position": "absolute", "borderWidth": "1px", "borderColor": "#ff0000", "paddingStart": "5px", "paddingEnd": "5px", "paddingTop": "1px", "paddingBottom": "1px", "cornerRadius": "5px", "offsetTop": "5px", "offsetStart": "5px", "backgroundColor": "#00000011"},{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": x_vod_name_Th , "weight": "bold", "wrap": True, "color": "#ffffffcc"},{"type": "text", "text": x_type_name_Th, "wrap": True, "size": "xxs", "margin": "sm", "color": "#ffffffcc"}], "paddingTop": "5px", "paddingEnd": "10px", "paddingStart": "10px"}], "paddingAll": "0px", "paddingBottom": "13px", "backgroundColor": "#000000"}}
        #print(flexJav)
        #client.sendFlexVideo(msg.to,vpath)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='AVFREEX24นำเสนอ: \n' + x_vod_name +"\n"+x_vod_name_Th+"\nประเภท: "+x_type_name_Th),
                #TextSendMessage(text='value: ' + str(quota.value)),
                VideoSendMessage(
                    original_content_url=vpath,
                    preview_image_url=x_vod_pic
                )
            ]
        )

    elif re.search(r'clipthai', text.lower()):
        #label = "JAV"
        url = requests.get(f"https://ru-4569f-default-rtdb.asia-southeast1.firebasedatabase.app/GO"+str(random.randint(1,7))+"/"+str(random.randint(1,120))+".json")
        #APIAV = ["https://mgzyz1.com/api.php/provide/vod/?ac=detail&pg="+str(random.randint(1,100)),"https://apilj.com/api.php/provide/vod/at/json/?ac=detail&pg="+str(random.randint(1,100))]
        #url = requests.get(random.choice(APIAV))
        text = url.text
        data = json.loads(text)
        #avdata = data['list'][random.randint(1,19)]
        x_vod_pic = data['splash']
        x_vod_name = data['splashtext'].replace(".mp4", "")
        x_vod_src = data['src']
        #flexJav={"type": "bubble", "size": "kilo", "body":{"type": "box", "layout": "vertical", "contents": [{"type": "video", "url": vpath, "previewUrl": vpath, "altContent":{"type": "image", "size": "full", "aspectRatio": "1:1", "aspectMode": "cover", "url": x_vod_pic}},{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "AVFREEX24.COM", "size": "xxs", "color": "#ff0000"}], "position": "absolute", "borderWidth": "1px", "borderColor": "#ff0000", "paddingStart": "5px", "paddingEnd": "5px", "paddingTop": "1px", "paddingBottom": "1px", "cornerRadius": "5px", "offsetTop": "5px", "offsetStart": "5px", "backgroundColor": "#00000011"},{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": x_vod_name_Th , "weight": "bold", "wrap": True, "color": "#ffffffcc"},{"type": "text", "text": x_type_name_Th, "wrap": True, "size": "xxs", "margin": "sm", "color": "#ffffffcc"}], "paddingTop": "5px", "paddingEnd": "10px", "paddingStart": "10px"}], "paddingAll": "0px", "paddingBottom": "13px", "backgroundColor": "#000000"}}
        #print(flexJav)
        #client.sendFlexVideo(msg.to,vpath)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='CLIP.AVFREEX24 นำเสนอ: \n' + x_vod_name),
                #TextSendMessage(text='value: ' + str(quota.value)),
                VideoSendMessage(
                    original_content_url=x_vod_src,
                    preview_image_url=x_vod_pic
                )
            ]
        )

    elif text.lower().startswith('lox='):
        msgTU = text.lower().split('lox=')[1]
        if msgTU == "":
            return line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ไม่พบ ID VIDEO TIKTOK'),
                #TextSendMessage(text='value: ' + str(quota.value)),
            ]
        )
        DOWNLOAD_HEADERS = {'user-agent': 'TelegramBot (like TwitterBot)'}
        conn = http.client.HTTPSConnection("api.tiktokv.com")
        payload = ''
        headers = {}
        conn.request("GET", "/aweme/v1/multi/aweme/detail/?aweme_ids=%5B" + msgTU + "%5D", payload, headers)
        res = conn.getresponse()
        data = res.read()
        obj = json.loads(data.decode("utf-8"))
        download_url =  obj["aweme_details"][0]["video"]["play_addr"]["url_list"][0];
        #client.sendFlexVideoLTK(msg.to,download_url)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='DownLoad Video TikTok ไม่มีลายน้ำ เรียบร้อย: \n'),
                #TextSendMessage(text='value: ' + str(quota.value)),
                VideoSendMessage(
                    original_content_url=download_url,
                    preview_image_url="https://clip.avfreex24.com/wp-content/uploads/2022/06/logoChang.png"
                )
            ]
        )

    elif re.search(r'กำลังไปเอาหนังมาให้ดูใจเย็นๆ', text.lower()) or re.search(r'movieav\.net', text.lower()):
        #label = "JAV"
        data = api.search.search("model+media", period="weekly")
        pornlist = []
        for vid in data.videos:
            pornlist.append(vid.video_id)
        url = requests.get("https://playx.cleverapps.io/api/?site_id=pornhub&video_id="+random.choice(pornlist))
        text = url.text
        datapX = json.loads(text)
        thumb = datapX['thumb']
        try:
            fullHD = datapX['mp4']['1080p']
        except:
            fullHD = datapX['mp4']['720p']
        phone = datapX['mp4']['480p']
        if fullHD != "":
            print(fullHD,thumb)
            line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='JAV สวย ไม่เซ็นเซอร์ HD\nต้องการค้นหา พิมพ์\nph=ข้อความ\nตัวอย่าง ph=เสียงไทย'),
                #TextSendMessage(text='value: ' + str(quota.value)),
                VideoSendMessage(
                    original_content_url=fullHD,
                    preview_image_url=thumb
                )
            ]
        )
        elif phone != "":
            print(phone,thumb)
            line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='JAV สวย ไม่เซ็นเซอร์\nต้องการค้นหา พิมพ์\nph=ข้อความ\nตัวอย่าง ph=เสียงไทย'),
                #TextSendMessage(text='value: ' + str(quota.value)),
                VideoSendMessage(
                    original_content_url=phone,
                    preview_image_url=thumb
                )
            ]
        )
        else:
            print("NOVID")
            line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ชัวร์เลย pronhub block ลองใหม่อีกสักพัก'),
                #TextSendMessage(text='value: ' + str(quota.value)),
            ]
        )

    elif text.lower().startswith('sp='):
        msgTU = text.lower().split('sp=')[1]
        if msgTU == "":
            return line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ไม่พบ ข้อความที่จะค้นหาหนัง'),
                #TextSendMessage(text='value: ' + str(quota.value)),
            ]
        )
        
        limit = int(10)
        #https://spankbang.com/s/model+media/?p=m
        r = requests.get(f"https://spankbang.com/s/{msgTU}?p=m").text
        soup = BeautifulSoup(r, 'lxml')
        seedata = []
        for item in soup.find_all('div', class_='video-item')[0:limit]:
            try:
                full_video = item.find("a", class_='thumb')['href']
            except:
                print(f'No videos found for: {msgTU}')
            if "/category/" in full_video:
                continue
            title = full_video.split('/')[3].replace('+', ' ')
            vvid = full_video.split("/")[1]
            prev = item.picture.img
            try:
                prev_vid = prev['data-preview']
                image = prev['data-src']
            except:
                prev_vid = "Not Found"
                image = "Not Found"
            seedata.append({
                "SPTitle": title,
                "PreviewVideo": prev_vid,
                "Thumbnail": image,
                "urlPP": "https://pnck-ytdl.herokuapp.com/api/info?url=https://spankbang.com/"+vvid+"/embed/"
            })
            
        SExsa = random.choice(seedata)
        urlsp = requests.get(SExsa['urlPP'])
        text = urlsp.text
        datapX = json.loads(text)
        playMP4 = []
        for mp4play in datapX['info']['formats']:
            if mp4play['url'].startswith("https://vdownload"):
                playMP4.append(mp4play['url'])
                
        #print(playMP4[-1],SExsa['SPTitle'],SExsa['PreviewVideo'],SExsa['Thumbnail'])
        if playMP4[-1] != "":
            line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ผลการค้นหาจากSpankbang\nวีดีโอMP4 Title:\n'+SExsa['SPTitle']),
                #TextSendMessage(text='value: ' + str(quota.value)),
                VideoSendMessage(
                    original_content_url=playMP4[-1],
                    preview_image_url=SExsa['Thumbnail']
                )
            ]
        )
        else:
            print("NOVID")
            line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ไม่พบ หนังเย็ดกันครับ'),
                #TextSendMessage(text='value: ' + str(quota.value)),
            ]
        )

    elif text.lower().startswith('ph='):
        msgTU = text.lower().split('ph=')[1]
        if msgTU == "":
            return line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ไม่พบ ข้อความที่จะค้นหาหนัง'),
                #TextSendMessage(text='value: ' + str(quota.value)),
            ]
        )
        data = api.search.search(msgTU, period="weekly")
        pornlist = []
        for vid in data.videos:
            pornlist.append(vid.video_id)
        url = requests.get("https://playx.cleverapps.io/api/?site_id=pornhub&video_id="+random.choice(pornlist))
        text = url.text
        datapX = json.loads(text)
        thumb = datapX['thumb']
        try:
            fullHD = datapX['mp4']['1080p']
        except:
            fullHD = datapX['mp4']['720p']
        phone = datapX['mp4']['480p']
        if fullHD != "":
            print(fullHD,thumb)
            line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='JAV สวย ไม่เซ็นเซอร์ HD\nดาวน์โหลดวีดีโอ TIKTOK ไม่มีลายน้ำ พิมพ์\nlox=IDวีดีโอ\nตัวอย่าง lox=7080324825415159082'),
                #TextSendMessage(text='value: ' + str(quota.value)),
                VideoSendMessage(
                    original_content_url=fullHD,
                    preview_image_url=thumb
                )
            ]
        )
        elif phone != "":
            print(phone,thumb)
            line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='JAV สวย ไม่เซ็นเซอร์\nดาวน์โหลดวีดีโอ TIKTOK ไม่มีลายน้ำ พิมพ์\nlox=IDวีดีโอ\nตัวอย่าง lox=7080324825415159082'),
                #TextSendMessage(text='value: ' + str(quota.value)),
                VideoSendMessage(
                    original_content_url=phone,
                    preview_image_url=thumb
                )
            ]
        )
        else:
            print("NOVID")
            line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ไม่พบ หนังเย็ดกันครับ'),
                #TextSendMessage(text='value: ' + str(quota.value)),
            ]
        )

    elif text == 'Xmsquota':
        quota = line_bot_api.get_message_quota()
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='type: ' + quota.type),
                TextSendMessage(text='value: ' + str(quota.value))
            ]
        )
    elif text == 'quota_consumptionXms':
        quota_consumption = line_bot_api.get_message_quota_consumption()
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='total usage: ' + str(quota_consumption.total_usage)),
            ]
        )
    elif text == 'Xmspush':
        line_bot_api.push_message(
            event.source.user_id, [
                TextSendMessage(text='PUSH!'),
            ]
        )
    elif text == 'multicasXmst':
        line_bot_api.multicast(
            [event.source.user_id], [
                TextSendMessage(text='THIS IS A MULTICAST MESSAGE'),
            ]
        )
    elif text == 'Xmsbroadcast':
        line_bot_api.broadcast(
            [
                TextSendMessage(text='THIS IS A BROADCAST MESSAGE'),
            ]
        )
    elif text.startswith('Xmsbroadcast '):  # broadcast 20190505
        date = text.split(' ')[1]
        print("Getting broadcast result: " + date)
        result = line_bot_api.get_message_delivery_broadcast(date)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='Number of sent broadcast messages: ' + date),
                TextSendMessage(text='status: ' + str(result.status)),
                TextSendMessage(text='success: ' + str(result.success)),
            ]
        )
    elif text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))
    elif text == 'ximagex':
        url = request.url_root + '/static/logo.png'
        app.logger.info("url=" + url)
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(url, url)
        )
    elif text == 'xconfirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageAction(label='Yes', text='Yes!'),
            MessageAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'xbuttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping'),
                PostbackAction(label='ping with text', data='ping', text='ping'),
                MessageAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'xcarousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackAction(label='ping with text', data='ping', text='ping'),
                MessageAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    
    elif re.search(r'agm', text.lower()):
        urlX = requests.get("https://yed.moviefreex24.com/models")
        text = urlX.text
        datapX = json.loads(text)
        countX = datapX['totalModels']
        models = datapX['models']
        # for thumb in datapX['images']:
        #     picTitle = thumb['title']
        #     picSrc = thumb['src']
        #     picLink = thumb['link']
        #     print("")
        numx1 = random.randint(1,countX)
        numx2 = random.randint(1,countX)
        numx3 = random.randint(1,countX)
        numx4 = random.randint(1,countX)
        numx5 = random.randint(1,countX)
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url=models[numx1]['src'],
                                action=PostbackAction(label = models[numx1]['rank']+" "+models[numx1]['name'][0:7] ,data = "username="+models[numx1]['username'])),
            ImageCarouselColumn(image_url=models[numx2]['src'],
                                action=PostbackAction(label = models[numx2]['rank']+" "+models[numx2]['name'][0:7] ,data = "username="+models[numx2]['username'])),
            ImageCarouselColumn(image_url=models[numx3]['src'],
                                action=PostbackAction(label = models[numx3]['rank']+" "+models[numx3]['name'][0:7] ,data = "username="+models[numx3]['username'])),
            ImageCarouselColumn(image_url=models[numx4]['src'],
                                action=PostbackAction(label = models[numx4]['rank']+" "+models[numx4]['name'][0:7] ,data = "username="+models[numx4]['username'])),
            ImageCarouselColumn(image_url=models[numx5]['src'],
                                action=PostbackAction(label = models[numx5]['rank']+" "+models[numx5]['name'][0:7] ,data = "username="+models[numx5]['username']))
        ])
        template_message = TemplateSendMessage(
            alt_text='ดูAV LINEOA ฟรีไม่มีโฆษณา', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'ximage_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='datetime',
                                                            data='datetime_postback',
                                                            mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='date',
                                                            data='date_postback',
                                                            mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    
    elif text == 'ximagemap':
        pass
    elif text == 'xflex':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://example.com/cafe.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Brown Cafe', weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            TextComponent(text='4.0', size='sm', color='#999999', margin='md',
                                          flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Shinjuku, Tokyo',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:000000'),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='WEBSITE', uri="https://example.com")
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif text == 'xflex_update_1':
        bubble_string = """
        {
          "type": "bubble",
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip3.jpg",
                "position": "relative",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "1:1",
                "gravity": "center"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "Brown Hotel",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#ffffff"
                      },
                      {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                          {
                            "type": "icon",
                            "size": "sm",
                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                          },
                          {
                            "type": "icon",
                            "size": "sm",
                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                          },
                          {
                            "type": "icon",
                            "size": "sm",
                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                          },
                          {
                            "type": "icon",
                            "size": "sm",
                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                          },
                          {
                            "type": "icon",
                            "size": "sm",
                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                          },
                          {
                            "type": "text",
                            "text": "4.0",
                            "size": "sm",
                            "color": "#d6d6d6",
                            "margin": "md",
                            "flex": 0
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "¥62,000",
                        "color": "#a9a9a9",
                        "decoration": "line-through",
                        "align": "end"
                      },
                      {
                        "type": "text",
                        "text": "¥42,000",
                        "color": "#ebebeb",
                        "size": "xl",
                        "align": "end"
                      }
                    ]
                  }
                ],
                "position": "absolute",
                "offsetBottom": "0px",
                "offsetStart": "0px",
                "offsetEnd": "0px",
                "backgroundColor": "#00000099",
                "paddingAll": "20px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "SALE",
                    "color": "#ffffff"
                  }
                ],
                "position": "absolute",
                "backgroundColor": "#ff2600",
                "cornerRadius": "20px",
                "paddingAll": "5px",
                "offsetTop": "10px",
                "offsetEnd": "10px",
                "paddingStart": "10px",
                "paddingEnd": "10px"
              }
            ],
            "paddingAll": "0px"
          }
        }
        """
        message = FlexSendMessage(alt_text="hello", contents=json.loads(bubble_string))
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif text == 'xquick_reply':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='Quick reply',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(label="label1", data="data1")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="label2", text="text2")
                        ),
                        QuickReplyButton(
                            action=DatetimePickerAction(label="label3",
                                                        data="data3",
                                                        mode="date")
                        ),
                        QuickReplyButton(
                            action=CameraAction(label="label4")
                        ),
                        QuickReplyButton(
                            action=CameraRollAction(label="label5")
                        ),
                        QuickReplyButton(
                            action=LocationAction(label="label6")
                        ),
                    ])))
    elif text == 'xlink_token' and isinstance(event.source, SourceUser):
        link_token_response = line_bot_api.issue_link_token(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='link_token: ' + link_token_response.link_token)
            ]
        )
    elif text == 'xinsight_message_delivery':
        today = datetime.date.today().strftime("%Y%m%d")
        response = line_bot_api.get_insight_message_delivery(today)
        if response.status == 'ready':
            messages = [
                TextSendMessage(text='broadcast: ' + str(response.broadcast)),
                TextSendMessage(text='targeting: ' + str(response.targeting)),
            ]
        else:
            messages = [TextSendMessage(text='status: ' + response.status)]
        line_bot_api.reply_message(event.reply_token, messages)
    elif text == 'xinsight_followers':
        today = datetime.date.today().strftime("%Y%m%d")
        response = line_bot_api.get_insight_followers(today)
        if response.status == 'ready':
            messages = [
                TextSendMessage(text='followers: ' + str(response.followers)),
                TextSendMessage(text='targetedReaches: ' + str(response.targeted_reaches)),
                TextSendMessage(text='blocks: ' + str(response.blocks)),
            ]
        else:
            messages = [TextSendMessage(text='status: ' + response.status)]
        line_bot_api.reply_message(event.reply_token, messages)
    elif text == 'xinsight_demographic':
        response = line_bot_api.get_insight_demographic()
        if response.available:
            messages = ["{gender}: {percentage}".format(gender=it.gender, percentage=it.percentage)
                        for it in response.genders]
        else:
            messages = [TextSendMessage(text='available: false')]
        line_bot_api.reply_message(event.reply_token, messages)

    elif re.search(r'help', text.lower()):
        link_token_response = line_bot_api.issue_link_token(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='''🌟 บอทLINEOA AVFREEX24.COM
    - ใช้งานฟรี ไม่มีโฆษณา แอบแฟง
    - สามารถ ดึงบอทไปใช้ในกลุ่มได้
    - บอทเป็นบอทLINEOAไม่มีเตะยกห้อง
    -------------------------------
    🌟🌟 คำสั่งที่ใช้ได้ 🌟🌟
    - ดูหนังAV มีเซ็นเซอร์
      พิมพ์ avfreex24.com
    - คลิปหลุดไทย
      พิมพ์ clipthai
    - หนังAVไม่เซ็นเซอร์
      พิมพ์ movieav.net
    - เรียกดูตารางบอลและดูบอลสด
      พิมพ์ dob 
      *กดAllowครั้งแรกที่เปิด*
    ------------------------------- 
    ** ค้นหาจาก pornhub
    พิมพ์ ph=ตามด้วยข้อความ
    ตัวอย่าง ph=เสียงไทย
    -------------------------------
    ** ค้นหาจาก spankbang
    พิมพ์ sp=ตามด้วยข้อความ
    ตัวอย่าง sp=modelmedia
    -------------------------------
    ** ดาวน์โหลดวีดีโอจาก TikTok ไมมีลายน้ำ ด้วยID
    พิมพ์ lox=IDวีดีโอ
    ตัวอย่าง lox=7078856042293103914
    -------------------------------
    ดูรูปจาก elitebabes วัยรุ่นเมกา
    งานดี พิมพ์ agm
    -------------------------------
    ในส่วนอื่นๆกำลัง อัพเดทให้ครับ''')
            ]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="คำสั่งไม่ถูกต้อง\nดูหนังAV พิมพ์ avfreex24.com \nหรือดูคลิปหลุด\nพิมพ์ clipthai \n ดูคำสั่งที่ใช้ได้ พิมพ์ help \n แนะนำให้จิ้มผ่าน เมนูสะดวกกว่า\nดูฟรี ไม่มีโฆษณา"))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title='Location', address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )


# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save content.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '-' + event.message.file_name
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save file.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(FollowEvent)
def handle_follow(event):
    app.logger.info("Got Follow event:" + event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    app.logger.info("Got Unfollow event:" + event.source.user_id)


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))
    elif event.postback.data == 'datetime_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
    elif event.postback.data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))
    elif event.postback.data.startswith('username'):
        modelUser = event.postback.data
        urlXM = requests.get("https://yed.moviefreex24.com/model?"+modelUser)
        text = urlXM.text
        datapX = json.loads(text)
        name_m = datapX['name']
        desc1_m = trans(datapX['desc1'])
        poster_m = datapX['poster']
        totalImages_m = datapX['totalImages']
        # for imgx in datapX['images']:
        #     src_m = imgx['src']
        #     title_m = imgx['title']
        #print(str(totalImages_m))
        
        bubble = BubbleContainer(
            size = "giga",
            direction='ltr',
            hero=ImageComponent(
                url = poster_m,
                size='full',
                aspect_ratio='1:1',
                aspect_mode='fit',
                #action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text = " "+name_m , weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            # IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            # IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            # IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            # IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            # IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            TextComponent(text='🌟🌟🌟🌟🌟 5.0', size='sm', color='#999999', margin='md', flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text = "รูปภาพทั้งหมด:",
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=" "+str(totalImages_m) + " รูป",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Description:',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=" "+desc1_m,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=PostbackAction(label='ดู 5 รูป', data='modelget=5&'+modelUser),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        #action=PostbackAction(label='ดูรูปทั้งหมด', data='modelget=ALL&'+modelUser)
                        action= MessageAction(label='ดูรูปทั้งหมด', text='ยังบ่พร้อม')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="PNCKDEVAPP", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        #print(name_m,desc1_m,totalImages_m)

        #line_bot_api.reply_message(
            #event.reply_token, TextSendMessage(text=event.postback.params['date'])
        #    )
    # elif event.postback.data.startswith('modelget'):
    #     valueImg = event.postback.data.split('modelget=')[1]
    #     userModel = valueImg.split('&')[1]
    #     urlXM = requests.get("https://yed.moviefreex24.com/model?"+userModel)
    #     text = urlXM.text
    #     datapX = json.loads(text)
    #     totalImages_m = datapX['totalImages']
    #     for imgx in datapX['images']:
    #         src_m = imgx['src']
    #         title_m = imgx['title']

    #     if valueImg == '5':
    #         line_bot_api.reply_message(
    #         event.reply_token,
    #         ImageSendMessage(url, url)
    #     )
    #         line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text=event.postback.params['date'])
    #         )

@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))


@handler.add(MemberJoinedEvent)
def handle_member_joined(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got memberJoined event. event={}'.format(
                event)))


@handler.add(MemberLeftEvent)
def handle_member_left(event):
    app.logger.info("Got memberLeft event")


@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=5000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()

    app.run(debug=options.debug, port=5000)
