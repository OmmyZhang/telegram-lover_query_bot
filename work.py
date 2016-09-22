#coding:utf-8
import urllib
import urllib2
import time
import json
import re
import sys


def work(comm,data):
    global weburl
    global token

    baseurl = weburl + token
    req = urllib2.Request(baseurl+comm,data)
    res = urllib2.urlopen(req)
    return_data = json.loads( res.read() )
    if return_data.has_key('ok'):
        if return_data['ok'] == True:
            if comm == '/getupdates':
                if len(return_data['result']):
                    global update_id
                    result = return_data['result'][-1]
                    update_id = result['update_id'] + 1

    return return_data

def sendMessage(text,send_to):
    #print text,send_to
    
    value = {
            'chat_id':send_to,
            'text' : unicode(text).encode('utf-8'),
            }
    data = urllib.urlencode(value)
    try:
        work('/sendmessage',data)
    except:
        print '['+text+']'
        print sys.exc_info(),'\ntime 1'
        try:
            work('/sendmessage',data)
        except:
            print sys.exc_info(),'\ntime 2'
    


weburl = 'https://api.telegram.org/bot'
token_file = open('token.secret','r')
token = token_file.readline()
token = token.strip()
token_file.close()

print '{'+token+'}'

print 'START:',time.strftime('%Y-%m-%d %H:%M:%S')
print work('/getme',None)

update_id = 0
while 1:
    value = {'offset' : update_id}
    data = urllib.urlencode(value)
    mess = work('/getupdates',data)
    #print mess
    for tmp in mess['result']:
        #print tmp
        if tmp.has_key('message'):
            mess = tmp['message']
        else:
            mess = tmp['edited_message']
        
        chat_id = mess['chat']['id']
        user = mess['from']

        if not user.has_key('first_name'):
            user['first_name'] = ''
        if not user.has_key('last_name'):
            user['last_name'] = ''

        if mess.has_key('text'):
            text = mess['text']
        else:
            text = ''

        if mess.has_key('new_chat_member'):
            user = mess['new_chat_member']
            if not user.has_key('last_name'):
                user['last_name'] = ''
            if not user.has_key('first_name'):
                user['first_name'] = ''
            sendMessage(u'欢迎'+user['last_name']+' '+user['first_name'] + u'进群',mess['chat']['id'])
            text = ':new user'


        
        if user.has_key('username'):
            who = user['username']
        else:
            who = unicode(user['first_name']+' '+user['last_name']).encode('utf-8')

        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(mess['date'] )), unicode(text).encode('utf-8'),'[',who,user['id'],'] (',mess['chat']['type']

        if re.match(r'/fire',text):
            sendMessage(u'烧烧烧，除了'+user['first_name']+' '+user['last_name'],chat_id)
        
        if re.match(r'/query',text):
            lovers = json.load(open('lovers.json'))
            if re.match(r'/query@lover_query_bot',text):
                name = re.search(r'/query@lover_query_bot\s*(.*?)\s*$',text).group(1)
            else:
                name = re.search(r'/query\s*(.*?)\s*$',text).group(1)
            #print '['+name+']'
            if name:
                if lovers.has_key(name):
                    sendMessage(name + u'和' + lovers[name] + u'是一对哦，嘿嘿' , chat_id)
                else:
                    if name == u'蛤':
                        sendMessage(u'感谢您的贡献,请注意查收私信',chat_id)
                        sendMessage('-1s',user['id'])
                    else:
                        sendMessage(u'没有'+name+u'的信息，会不会是单身狗(猫)呢',chat_id)
            else:
                sendMessage(u'你倒是输个名字啊',chat_id)

        if re.match(r'/speak',text):
            comm = re.search(r'/speak\s*(.*?)\s*$',text).group(1)
            print unicode(comm).encode('utf-8');
            if not comm:
                comm = u'你倒是告诉我你要说什么啊'
            sendMessage(comm,chat_id)


    time.sleep(1)
