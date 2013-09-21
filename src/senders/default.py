# -*- coding: utf-8 -*-
import logging


class Sender(object):
    'Sender插件类，必须使用Sender作为类名'
     
    def __init__(self, options):
        '插件初始化方法，options是插件配置数据'
        self.options = options

    def send(self, title, content, level=0, cate='default', host='default', appname='default'):
        '插件方法，必须实现'
        logging.info('sender.default send:%s %s %s', level, title, content)
