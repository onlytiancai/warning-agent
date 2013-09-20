# -*= coding: utf-8 -*-

from time import sleep
import logging
import sys

import config

logging.basicConfig(level=logging.DEBUG)

warning_rules = []
warning_counters = []
warning_senders = []
counter_logger = None


def init():
    '动态加载各种插件'

    # 动态加载计数器
    for counter_name in config.counter_names:
        try:
            logging.info('counter init %s', counter_name)
            counter = __import__('counters.%s' % counter_name)
            counter = getattr(counter, counter_name)
            warning_counters.append(counter)
        except:
            logging.exception('init counter error:%s', counter_name)

    # 动态加载报警规则
    for rule_name in config.rule_names:
        try:
            logging.info('rule init %s', rule_name)
            rule = __import__('rules.%s' % rule_name)
            rule = getattr(rule, rule_name)
            warning_rules.append(rule)
        except:
            logging.exception('init rule error:%s', rule_name)

    # 动态加载报警发送器
    for sender_name in config.sender_names:
        try:
            logging.info('sender init %s', sender_name)
            sender = __import__('senders.%s' % sender_name)
            sender = getattr(sender, sender_name)
            warning_senders.append(sender)
        except:
            logging.exception('init sender error:%s', sender_name)

    # 动态加载Logger
    logging.info('logger init %s', config.logger_name)
    logger = __import__('loggers.%s' % config.logger_name)
    logger = getattr(logger, config.logger_name)
    global counter_logger
    counter_logger = logger


def log_uncaught_exceptions(ex_cls, ex, tb):
    '对未处理异常记录日志'
    import traceback
    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(ex_cls, ex))

sys.excepthook = log_uncaught_exceptions


def send_warning(data):
    for sender in warning_senders:
        try:
            sender.send(data)
        except:
            logging.exception('send_warning(error:%s', sender.__name__)


def counter_handler(data):
    '遍历每一个报警规则来处理当前数据'
    for rule in warning_rules:
        try:
            if rule.process(data, counter_logger.get_log_caches()):
                send_data = rule.get_send_data(data, counter_logger.get_log_caches())
                send_warning(send_data)
        except:
            logging.exception('counter_handler error:%s', rule.__name__)


def get_counter_data():
    result = {}
    for counter in warning_counters:
        try:
            data = counter.get_data()
            result.update(data)
        except:
            logging.exception('get_counter_dataerror:%s', counter.__name__)
    return result


def main():
    while True:
        try:
            data = get_counter_data()
            logging.debug('gen_counter:%s', data)

            counter_logger.log(data)
            counter_handler(data)

            sleep(5)
        except KeyboardInterrupt:
            raise
        except:
            logging.exception('main error')

if __name__ == '__main__':
    init()
    main()
