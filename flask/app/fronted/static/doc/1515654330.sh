#!/bin/bash
cd `dirname $0`
eval $(ps -ef | grep "[s]s-local" | awk '{print "kill "$2}')

