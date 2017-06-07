#!/bin/bash
cat <<'EOF' >>  ~ec2-user/.bash_profile
FSLDIR=/usr/local/fsl
. ${FSLDIR}/etc/fslconf/fsl.sh
PATH=${FSLDIR}/bin:${PATH}
export FSLDIR PATH
EOF
mkdir -p /usr/local
cd /usr/local
aws s3 cp s3://BUCKET/fsl-5.0.9-centos6_64.tar .
tar xvf fsl-5.0.9-centos6_64.tar 
rm -f fsl-5.0.9-centos6_64.tar 

