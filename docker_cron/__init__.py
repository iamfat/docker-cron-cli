# -*- coding: utf-8 -*-

import subprocess, sys
import getopt
import crontab

def usage():
    print "Usage: docker-cron [container1 container2 ...] [-h]\n"

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
            def readable_name(container):
                try:
                    return subprocess.check_output(
                                "docker inspect -f {{.Name}} %s" % container,
                                shell=True).lstrip('/').rstrip('\n')
                except subprocess.CalledProcessError as e:
                    return container
            containers = map(readable_name, containers)
        except subprocess.CalledProcessError as e:
            print ("%r" % str(e))
            sys.exit()

    for container in containers:
        # if container == '': continue
        try:
            cmd = ("docker exec -t %s sh -lc '[ -d /etc/cron.d ] && find /etc/cron.d -type f -exec cat \{\} \;'" % container)
            tab = subprocess.check_output(cmd, shell=True).replace('\t', ' ')
        except subprocess.CalledProcessError as e:
            continue

        if tab == '': continue;
        
        cron = crontab.CronTab(tab=tab, user=False)
        # cron.write()
        print("################# DOCKER CRON FOR %s #################" % container)
        for job in cron:
            if job.user == "root":
                sudo = ""
            else:
                sudo = " sudo -u " + job.user
            job.user = "root"
            command = "docker exec {container}{sudo} sh -lc '{command}'"
            job.set_command(command.format(
                container=container, sudo=sudo, 
                command=job.command.replace("'", "'\\''")))
            print(job.render())
        # print(cron.render())
        print("")

if __name__ == "__main__":
    main()
