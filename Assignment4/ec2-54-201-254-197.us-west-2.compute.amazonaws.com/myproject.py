import os
import json
import requests

from flask import Flask, request, Response
import mechanize
import cookielib


application = Flask(__name__)

# FILL THESE IN WITH YOUR INFO
my_bot_name = 'rong_bot' #e.g. zac_bot
my_slack_username = 'rong' #e.g. zac.wentzell


slack_inbound_url = 'https://hooks.slack.com/services/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'


# this handles POST requests sent to your server at SERVERIP:41953/slack
@application.route('/slack', methods=['POST'])
def inbound():
    print '========POST REQUEST @ /slack========='
    response = {'username': my_bot_name, 'icon_emoji': ':robot_face:', 'text': ''}
    print 'FORM DATA RECEIVED IS:'
    print request.form

    channel = request.form.get('channel_name') #this is the channel name where the message was sent from
    username = request.form.get('user_name') #this is the username of the person who sent the message
    text = request.form.get('text') #this is the text of the message that was sent
    inbound_message = username + " in " + channel + " says: " + text
    print '\n\nMessage:\n' + inbound_message

    if username in [my_slack_username, 'rong']:
        # Your code for the assignment must stay within this if statement

        # A sample response:
        if text == "What's your favorite color?":
        # you can use print statments to debug your code
            print 'Bot is responding to favorite color question'
            response['text'] = 'Blue!'
            print 'Response text set correctly'

        if "<BOTS_RESPOND>" in text:
        # you can use print statments to debug your code
            print 'Bot is responding question'
            response['text'] = 'Hello, my name is rong_bot. I belong to rong. I live at 54.201.254.197.'
            print 'Response text set correctly'

        if '<I_NEED_HELP_WITH CODING>:' in text:
            # Browser
            br = mechanize.Browser()

            # Cookie Jar
            cj = cookielib.LWPCookieJar()
            br.set_cookiejar(cj)

            # Browser options
            br.set_handle_equiv(True)
            br.set_handle_gzip(True)
            br.set_handle_redirect(True)
            br.set_handle_referer(True)
            br.set_handle_robots(False)

            # Follows refresh 0 but not hangs on refresh > 0
            br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

            # Want debugging messages?
            # br.set_debug_http(True)
            # br.set_debug_redirects(True)
            # br.set_debug_responses(True)

            # User-Agent (this is cheating, ok?)
            br.addheaders = [('User-agent',
                              'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36')]

            q = text.split(':', 1)[1]
            q=q.split(' ')
            res = q[0]
            for i in range(1, len(q) - 1, 1):
                res = res + '+' + q[i]
            res='http://stackoverflow.com/search?q='+res
            r = br.open(res)
            html = r.read()

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