# -*- coding: utf-8 -*-

import subprocess, sys
import getopt
import crontab

def usage():
    print "Usage: docker-cron -c <config-file> <zmq-address>\n"
    print "    <config-file>: path to config file in YAML format, e.g. /etc/debade/courier.yml"
    print "    <zmq-address>: ZeroMQ address to listen, e.g. ipc:///path/to/ipc, tcp://0.0.0.0:3333"

def main():

    # docker-cron [container1 container2 ...] [-h]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h")
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
    
    if len(args) > 0:
        containers = args
    else:
        # enumerate all containers via `docker ps`
        try:
            containers = subprocess.check_output("docker ps -q", shell=True).splitlines()
        except subprocess.CalledProcessError, e:
            print ("%r" % str(e))
            sys.exit()

    
    for container in containers:
        # if container == '': continue
        try:
            cmd = ("docker exec %s sh -c '[ -d /etc/cron.d ] && find /etc/cron.d -type f -exec cat \{\} \;'" % container)
            tab = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError, e:
            continue
        
        if tab == '': continue;
        
        cron = crontab.CronTab(tab=tab, user=False)
        # cron.write()
        for job in cron:
            job.set_command("docker exec %s sh -c '%s'" % (container, job.command.replace("'", "'\\''")))

        print("################# DOCKER CRON FOR %s #################" % container)
        print(cron)

if __name__ == "__main__":
    main()