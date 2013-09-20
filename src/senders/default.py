# -*- coding: utf-8 -*-
import logging

def send(title, content, level=0, cate='default', host='default', appname='default'):
    '所有报警发送器必须实现'
    logging.info('sender.default send:%s %s', level, title) 
