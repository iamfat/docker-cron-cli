# Docker Cron

Automatically scan /etc/cron.d in specific docker containers and output it to stdout

```bash
pip install docker-cron
docker-cron <container>
sudo docker-cron > /etc/cron.d/docker-cron
```