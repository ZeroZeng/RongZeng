# coding=utf-8
import os
import json
import requests
import random

from flask import Flask, request, Response
import time


application = Flask(__name__)

# FILL THESE IN WITH YOUR INFO
my_bot_name = 'rong_bot' #e.g. zac_bot
my_slack_username = 'rong' #e.g. zac.wentzell


slack_inbound_url = 'https://hooks.slack.com/services/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'
# slack_inbound_url = 'https://hooks.slack.com/services/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'


# this handles POST requests sent to your server at SERVERIP:41953/slack
@application.route('/slack', methods=['POST'])
def inbound():
    delay = random.uniform(0, 20)
    time.sleep(delay)
    print '========POST REQUEST @ /slack========='
    response = {'username': my_bot_name, 'icon_emoji': ':robot_face:', 'text': '', 'attachments': ''}
    print 'FORM DATA RECEIVED IS:'
    print request.form

    channel = request.form.get('channel_name') #this is the channel name where the message was sent from
    username = request.form.get('user_name') #this is the username of the person who sent the message
    text = request.form.get('text') #this is the text of the message that was sent
    inbound_message = username + " in " + channel + " says: " + text
    print '\n\nMessage:\n' + inbound_message

    if username in [my_slack_username, 'zac.wentzell']:
        # Your code for the assignment must stay within this if statement

        # A sample response:
        if text == "What's your favorite color?":
        # you can use print statments to debug your code
            print 'Bot is responding to favorite color question'
            response['text'] = 'Blue!'
            print 'Response text set correctly'

        if 'BOTS_RESPOND' in text:
        # you can use print statments to debug your code
            print 'Bot is responding question'
            response['text'] = 'Hello, my name is rong_bot. I belong to rong. I live at 54.201.254.197.'
            print 'Response text set correctly'

        if 'I_NEED_HELP_WITH_CODING' in text:
            a = text
            a = a.split(':', 1)[1].strip()
            b = a.split('[')
            q = b[0]

            if len(b) > 1:
                tag = b[1][:-1]
                for i in range(2, len(b)):
                    tag = tag + ';' + b[i][:-1]
                http = 'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=' + q + '&tagged=' + tag + '&site=stackoverflow'
            else:
                http = 'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=' + q + '&site=stackoverflow'


            res0 = requests.get(http)
            time.sleep(0.01)
            res1 = res0.json()
            res = res1['items'][:5]
            data = [(row['link'], row['title'], row['answer_count'],time.strftime('%m-%d-%Y', time.localtime(row['creation_date']))) for row in res]
            for i in range(len(data)):
                text = text + '\n'+str(i+1)+'. <' + str(data[i][0]) + '|' + str(data[i][1]) + '> (' + str(data[i][2]) + ' responses), ' + str(
                    data[i][3])
            time.sleep(0.01)
            response['text'] = text
            print 'Response text set correctly'

        if 'WHAT\'S_THE_WEATHER_LIKE_AT' in text:
            a = text
            a = a.split(':', 1)[1].strip()
            b = a.replace(' ','+')
            http='https://maps.googleapis.com/maps/api/geocode/json?address='+b+'&key=AIzaSyArrI7ZRhK-6hfP1TIo1WlnaJt7BuLmGyQ'
            res0 = requests.get(http)
            time.sleep(0.1)
            res1 = res0.json()
            lat = res1['results'][0]['geometry']['location']['lat']
            lng = res1['results'][0]['geometry']['location']['lng']
            http1 = 'https://api.darksky.net/forecast/4e7dd16acefa920fc8580be10c0a02df/{0},{1}'.format(lat,lng)
            res2 = requests.get(http1)
            time.sleep(0.1)
            res3 = res2.json()
            cur = res3['currently']
            today = res3['daily']['data'][0]
            tomo = res3['daily']['data'][1]
            cur_temperature= 'Temperature: {0} °F'.format(cur['temperature'])
            cur_summary=str(cur['summary'])
            cur_humidity= 'Humidity {0} %'.format(cur['humidity'] * 100)
            cur_pressure=str(cur['pressure'])+' hPa'
            cur_windSpeed=str(cur['windSpeed'])+' mph'
            cur_precipIntensity= 'PrecipIntensity {0} in'.format(cur['precipIntensity'])
            cur_precipProbability= 'PrecipProbability {0} %'.format(cur['precipProbability'] * 100)
            cur_time= str(cur['time'])
            today_temperature = 'High {0}|Low {1} °F'.format(today['temperatureMax'], today['temperatureMin'])
            tomo_summary = str(tomo['summary'])
            tomo_temperature = 'High {0}|Low {1} °F'.format(tomo['temperatureMax'], tomo['temperatureMin'])
            tomo_precipIntensity = 'Precip Intensity {0} in'.format(tomo['precipIntensity'])
            tomo_precipProbability = 'Precip Probability {0} %'.format(tomo['precipProbability'] * 100)
            tomo_humidity = 'Humidity {0} %'.format(tomo['humidity'] * 100)
            value1 = '{0}\n{1}\n{2}\n{3}\n{4}'.format(cur_summary, cur_temperature, today_temperature,cur_humidity, cur_precipProbability)
            value2 = '{0}\n{1}\n{2}\n{3}'.format(tomo_summary, tomo_temperature, tomo_humidity,tomo_precipProbability)

            if 'snow' in cur_summary or 'Snow' in cur_summary:
                image_url='http://img.sc115.com/uploads2/sc/png/4311/307.png'
            elif 'rain' in cur_summary or 'Rain' in cur_summary:
                image_url='http://img.sc115.com/uploads2/sc/png/4311/311.png'
            elif 'drizzle' in cur_summary or 'Drizzle' in cur_summary:
                image_url='http://img.sc115.com/uploads2/sc/png/4311/314.png'
            elif 'foggy' in cur_summary or 'Foggy' in cur_summary:
                image_url='http://img.sc115.com/uploads2/sc/png/4311/309.png'
            elif 'Overcast' in cur_summary or 'overcast' in cur_summary:
                image_url = 'http://img.sc115.com/uploads2/sc/png/4311/310.png'
            elif 'cloudy' in cur_summary or 'Cloudy' in cur_summary:
                image_url = 'http://img.sc115.com/uploads2/sc/png/4311/319.png'
            elif 'clear' in cur_summary or 'Clear' in cur_summary:
                image_url = 'http://img.sc115.com/uploads2/sc/png/4311/322.png'
            else:
                image_url = "http://cn.technode.com/files/2015/03/C1304067039357.jpg"

            true='true'
            false='false'

            text1=[
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": "#36a64f",
                    "pretext": "",
                    "author_name": "",
                    "author_link": "",
                    "author_icon": "",
                    "title": "Weather Forecast",
                    "title_link": "",
                    "text": "",
                    "fields": [
                        {
                            "title": "Today",
                            "value": value1,
                            "short": true
                        },
                        {
                            "title": "Tomorrow",
                            "value": value2,
                            "short": true
                        }
                    ],
                    "image_url": image_url,
                    "thumb_url": "",
                    "footer": "Dark Sky",
                    "ts": cur_time
                }
            ]

            response['text']= text
            response['attachments'] = text1

            print 'Response text set correctly'


        if slack_inbound_url and response['text']:
            r = requests.post(slack_inbound_url, json=response)

    print '========REQUEST HANDLING COMPLETE========\n\n'

    return Response(), 200


# this handles GET requests sent to your server at SERVERIP:41953/
@application.route('/', methods=['GET'])
def test():
    return Response('Your flask app is running!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)