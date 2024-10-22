<!--
 Copyright 2020 Tata Elxsi

 Licensed under the Apache License, Version 2.0 (the License); you may
 not use this file except in compliance with the License. You may obtain
 a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an AS IS BASIS, WITHOUT
 WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 License for the specific language governing permissions and limitations
 under the License.

 For those usages not covered by the Apache License, Version 2.0 please
 contact: canonical@tataelxsi.onmicrosoft.com

 To get in touch with the maintainers, please contact:
 canonical@tataelxsi.onmicrosoft.com
-->

# UE

## Description

Charm to deploy UE application pod.

## Usage

SSH has to be enabled inside pod with port 22 such that RAN application
can modify the ip interface in UE pod

## Prerequisite

1. Install Charmcraft

```bash
sudo snap install charmcraft --beta
```

### Deploy

To deploy UE from Charmstore, use the following command

```bash
juju deploy cs:~tata-charmers/ue
```

NOTE: UE requries RAN to be up for successful deployment

#### Deploy from local repository

a. Build using the following command

```bash
charmcraft build
```

b. Deploy using the following command

```bash
juju deploy ./ue.charm --resource image=tataelxsi5g/ue:4.0
```

## Developing

Create and activate a virtualenv with the development requirements:

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements-dev.txt

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

./run_tests
