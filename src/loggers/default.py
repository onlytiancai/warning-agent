# -*- coding: utf-8 -*-
import logging
import logging.handlers
import json
from datetime import datetime

from log_watcher import LogWatcher

LOG_FILENAME = '/var/log/wawa-warning-agent-counter.log'
MAX_LOG_CACHE = 20

my_logger = logging.getLogger('counter')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=100 * 1000 * 1000, backupCount=10)
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
my_logger.addHandler(handler)


log_caches = []  # 


def log(counter_data):
    '所有logger必须实现，保存日志数据'
    my_logger.info(json.dumps(counter_data))
    if len(log_caches) >= MAX_LOG_CACHE:
        log_caches.pop(0)

    counter_data['time'] = datetime.now()
    log_caches.append(counter_data)


def get_log_caches():
    '所有logger必须实现，返回最近几条计数器日志，用于在报警判断逻辑中使用'
    return log_caches


def readlog_from_file(n=10):
    '从日志里读取计数器信息'
    lines = LogWatcher.tail(LOG_FILENAME, 10)
    results = []
    for line in lines:
        if line.find('{') == -1:
            continue
        pos = line.index('{')
        result = json.loads(line[pos:])
        results.append(result)
    return results


if __name__ == '__main__':
    results = readlog_from_file()
    import pprint
    pprint.pprint(results)
