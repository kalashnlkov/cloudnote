#!/bin/bash
cd `dirname $0`
eval $(ps -ef | grep "[s]s-local" | awk '{print "kill "$2}')
ulimit -n 512000
nohup ss-local -c /etc/shadowsocks-libev/config.json >> /dev/null 2>&1 &

