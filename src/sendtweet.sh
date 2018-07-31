#!/bin/sh
D=`date +%F-%H-%M`
echo $D >> /home/ubuntu/text_writer/src/tweeted.log
/usr/bin/python3 /home/ubuntu/text_writer/src/maketweet.py >> /home/ubuntu/text_writer/src/tweeted.log
