#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import subprocess
import sys
import getopt

from crontab import CronTab
from docker import Client

__version__ = '0.1.12'

def usage():
    print("Usage: docker-cron [container1 container2 ...] [-h]")

def main():

    cli = Client()

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h")
    except getopt.GetoptError as e:
        # print help information and exit:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == "-h":
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"
    
    if len(args) == 0:
        containers = map(lambda c: c['Names'][0][1:], cli.containers())
    else:
        containers = args

    for container in containers:
        cmd = "sh -lc '[ -d /etc/cron.d ] && find /etc/cron.d -type f -exec cat \{\} \;'"
        exec_id = cli.exec_create(container=container, cmd=cmd, tty=True)['Id']
        tab = cli.exec_start(exec_id=exec_id, tty=True).replace('\t', ' ')
        if tab == '':
            continue

        cron = CronTab(tab=tab, user=False)
        # cron.write()
        print("################# DOCKER CRON FOR {container} #################".format(container=container))
        for job in cron:
            if job.user == "root":
                sudo = ""
            else:
                sudo = " sudo -u " + job.user
            job.user = "root"
            command = "docker exec -t {container}{sudo} sh -lc '{command}'"
            job.set_command(command.format(
                container=container, sudo=sudo, 
                command=job.command.replace("'", "'\\''")))
            print(job.render())
        # print(cron.render())
        print("")

if __name__ == "__main__":
    main()
