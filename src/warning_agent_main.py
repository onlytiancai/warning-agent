from time import sleep
from daemonize import Daemonize
from pprint import pprint

import sysinfo
import counter_loger


def main():
    while True:
        result = sysinfo.get_sysinfo()
        pprint(result)
        counter_loger.log(result)
        sleep(5)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '-D':
        pid = "/tmp/wawa-warning-agent.pid"
        daemon = Daemonize(app="warning_agent", pid=pid, action=main) 
        daemon.start()
    else:
        main()
