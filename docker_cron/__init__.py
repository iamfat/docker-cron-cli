#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import subprocess
import sys
import getopt
import docker

from crontab import CronTab

__version__ = '0.3.0'

def usage():
    print("Usage: docker-cron [container1 container2 ...] [-h]")

def main():

    cli = docker.from_env()

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
        containers = cli.containers.list(all=True)
    else:
        containers = map(lambda nm: cli.containers.get(nm), args)

    for container in containers:
        cmd = "sh -c '[ -d /etc/cron.d ] && find /etc/cron.d -type f -exec cat \{\} \;'"
        exit_code, output = container.exec_run(cmd=cmd, stderr=False, tty=True)
        tab = output.decode().replace('\t', ' ')
        if tab == '':
            continue

        cron = CronTab(tab=tab, user=False)
        # cron.write()
        print("################# DOCKER CRON FOR {container} #################".format(container=container.name))
        for job in cron:
            if job.user == "root":
                sudo = ""
            else:
                sudo = " sudo -u " + job.user
            job.user = "root"
            command = "docker exec -t {container}{sudo} sh -lc '{command}'"
            job.set_command(command.format(
                container=container.name, sudo=sudo, 
                command=job.command.replace("'", "'\\''")))
            print(job.render())
        # print(cron.render())
        print("")

if __name__ == "__main__":
    main()
