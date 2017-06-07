#!/bin/bash
version="5.3.0"
dest=/usr/local/freesurfer/stable5_3
umask 022

mkdir -p /usr/local/freesurfer
cd /usr/local/freesurfer
aws s3 cp s3://BUCKET/freesurfer-Linux-centos6_x86_64-stable-pub-v${version}.tar.gz -C /usr/local/freesurfer
tar xvfz freesurfer-Linux-centos*
aws s3 cp s3://BUCKET/license.txt  ${dest}/license.txt



