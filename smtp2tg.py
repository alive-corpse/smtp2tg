# Based on https://cdnnow.ru/blog/smtp2tg/

import os
import io
import asyncore
import requests
import smtpd
from datetime import datetime

# Optional:
listen_addr = os.environ['SMTP2TG_LISTEN_ADDR'] if 'SMTP2TG_LISTEN_ADDR' in os.environ else '0.0.0.0'
listen_port = os.environ['SMTP2TG_LISTEN_PORT'] if 'SMTP2TG_LISTEN_PORT' in os.environ else 2525
# Required:
bot_token   = os.environ['SMTP2TG_BOT_TOKEN']
chat_id     = os.environ['SMTP2TG_CHAT_ID']

class smtp2tg(smtpd.SMTPServer):

    def formatter(self, data):
        sdata = data.split('\n\n')
        headers = sdata[0].split('\n')
        body = '\n\n'.join(sdata[1:])
        res = ''
        fh = {'received': '', 'from': '', 'to': '', 'subject': '', 'date': ''} # Filtered headers
        for h in headers:
            for hname in fh.keys():
                if h.lower().startswith('%s: ' % hname):
                    fh[hname] = h
        return '✉ %s\n📅 %s\n\n↗ %s\n↙ %s\n\n📝 %s\n\n```\n%s\n```' % (fh['received'], fh['date'], fh['from'], fh['to'], fh['subject'], body)

    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        nowstr   = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #content = '**%s:**\n\n%s' % (mailfrom, data.decode("utf-8"))
        msgfmt   = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=Markdown&text=%s'
        content = self.formatter(data.decode("utf-8"))
        print('%s\n%s%s\n' % (content, '=-'*20, '='))
        response = requests.get(msgfmt % (bot_token, chat_id, content))
        #print("%s -- from=%s to=%s response=%s\n" %
        #    (nowstr, mailfrom, rcpttos, response.json()))

server = smtp2tg((listen_addr, int(listen_port)), None)
print("Started on %s:%s..." % (listen_addr, listen_port))

try:
    asyncore.loop()
except KeyboardInterrupt:
    pass
