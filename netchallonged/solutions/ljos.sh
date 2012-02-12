#!/bin/sh
# @author ljos

exec 3<>/dev/tcp/pompel.komsys.org/1337;echo ljos>&3;read m<&3;echo $[$m]>&3;read m<&3;echo $m


