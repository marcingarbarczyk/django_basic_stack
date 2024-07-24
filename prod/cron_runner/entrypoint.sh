#!/bin/bash

env >> /etc/environment && \
/usr/bin/crontab -l | { cat /prod/cron_runner/crons; } | /usr/bin/crontab - && \
/etc/init.d/cron start && sleep infinity