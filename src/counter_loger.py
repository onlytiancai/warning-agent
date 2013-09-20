# -*- coding: utf-8 -*-
import logging
import logging.handlers
import json

from log_watcher import LogWatcher

LOG_FILENAME = '/var/log/wawa-warning-agent-counter.log'

my_logger = logging.getLogger('counter')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=100*1000*1000, backupCount=10)
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
my_logger.addHandler(handler)

def log(counter_data):
    my_logger.info(json.dumps(counter_data))

def readlog(n=10):
    lines = LogWatcher.tail(LOG_FILENAME, 10)
    results = [] 
    for line in lines:
        if line.find('{') == -1: continue
        pos = line.index('{')
        result = json.loads(line[pos:]) 
        results.append(result)
    return results


if __name__ == '__main__':
    results = readlog()
    import pprint
    pprint.pprint(results)
