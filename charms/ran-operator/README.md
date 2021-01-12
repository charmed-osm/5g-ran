<!-- Copyright 2020 Tata Elxsi

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

# ran

## Description

Charm to deploy RAN application
Contains Juju action for configurating gNodeB and establishing sctp
connection with CORE.
UE configurations are also updated through action
Attach Procedure is done through RestAPI call.

## Prerequisite

1. Install Charmcraft

```bash
sudo snap install charmcraft --beta
```

## Usage

### Deploy

To deploy 5G RAN Emulator from Charmstore, use the following command

```bash
juju deploy cs:~tata-charmers/ran
```

#### Deploy from local repository

a. Build using the following command

```bash
charmcraft build
```

b. Deploy using the following command

```bash
juju deploy ran.charm
```

## Developing

To test config-gnb action,run the following command

COMMAND : juju run-action ran/< UNIT-ID > config-gnb amfip=<'amf-ip'> dbip=<'dbip'> upfip=<'upf-ip'>

The above ips are obtained from Core deployment

To check the status and output of the action ,use the following command

COMMAND:
juju show-action-status < ACTION-ID >
juju show-action-output < ACTION-ID >

Similarly other actions can be trigerred.

Commands to create and activate a virtualenv with the development
requirements, use the following command:

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements-dev.txt

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

./run_tests
