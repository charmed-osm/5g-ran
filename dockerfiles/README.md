<!--
 Copyright 2020 Tata Elxsi

 Licensed under the Apache License, Version 2.0 (the "License"); you may
 not use this file except in compliance with the License. You may obtain
 a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 License for the specific language governing permissions and limitations
 under the License.

 For those usages not covered by the Apache License, Version 2.0 please
 contact: canonical@tataelxsi.onmicrosoft.com

 To get in touch with the maintainers, please contact:
 canonical@tataelxsi.onmicrosoft.com
-->
# 5G RAN Emulator docker files

This directory holds the docker files to build the docker images for ran-emulator and UE app.

## Description

Consists of 2 docker files
* ran
* ue_app

## Prerequisites

Copy rantest to ran folder. Example: 
cp rantest ran/.

Copy ran.so to ran folder. Example:
cp ran.so ran/.


## Usage

cd ran
sudo docker build . -t <image_name>:tag
cd ue_app
sudo docker build . -t <image_name>:tag

## Exposed Ports

----------------------------------------------------------
|     NF       |   Exposed Ports  | Dependencies         |
----------------------------------------------------------
|   ran        |   2152,8081,9487 |      NA              |
----------------------------------------------------------
|   ue_app     |        22        |      NA              |
----------------------------------------------------------

