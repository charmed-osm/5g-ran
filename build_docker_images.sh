#!/bin/bash
# Copyright 2020 Tata Elxsi
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# For those usages not covered by the Apache License, Version 2.0 please
# contact: canonical@tataelxsi.onmicrosoft.com
#
# To get in touch with the maintainers, please contact:
# canonical@tataelxsi.onmicrosoft.com
dir=dockerfiles
if [ -z `which docker` ]; then
    sudo apt-get update
    sudo apt-get install -y docker.io
fi
cd $dir
echo "Building image for RAN"
cd ran
sudo docker build -t localhost:32000/ran:1.0 .
cd ..
echo "Building image for UE"
cd ue_app
sudo docker build -t localhost:32000/ue:1.0 .
echo "Images are build successfully"
sudo docker images | grep "ran"
sudo docker images | grep "ue"
