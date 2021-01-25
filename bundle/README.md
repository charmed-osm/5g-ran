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

# 5G RAN Operators

## Description

5G Ran Emulator is implemented as microk8s applications using Juju Charms and Microk8s
Contains charm folder consisting of 2 k8s charm applications

* ue_app: ue pod is required for running User Equipment(UE) applications
* ran: Radio Access Network(RAN) generates gNodeB and UE

## Usage

### Prepare environment

#### A. Install Microk8s

a. Install Microk8s using the following commands,

```bash
sudo snap install microk8s --classic --channel 1.19/stable
sudo usermod -a -G microk8s `whoami`
newgrp microk8s
microk8s.status --wait-ready
```

The ouput "microk8s is running" signifies that Microk8s is successfully installed.

b. Enable the following required addons for Microk8s to deploy 5G Ran

```bash
microk8s.enable storage dns
microk8s.enable multus
microk8s.enable rbac
microk8s.enable metallb
```

NOTE: 5G RAN requires 2 loadbalancer IP addresses mandatorily. So allocate 2
IP addresses while enabling metallb.

#### B. Install Juju

a. Install Juju with the following commands,

```bash
sudo snap install juju --classic --channel 2.8/stable
juju bootstrap microk8s
```

### Deploy

To deploy 5G RAN Emulator from Charmstore, follow the steps below,

a. Deploy ran applications

```bash
juju deploy cs:~tataelxsi-charmers/ran-5g
```

b. Configuring interface

For the deployment to get completed successfully, update master_interface field
to your server's main interface name with the following command,

```bash
juju config ran master_interface="<interface_name>"
```

where interface_name stands for server's main interface name where ran is
deployed

#### Deploy from local repository

To deploy 5G Ran from local repository, follow the steps below,

a. Clone the 5g-ran repository

```bash
git clone https://github.com/charmed-osm/5g-ran
cd 5g-ran/
```

b. Enable Microk8s registry for storing images

```bash
microk8s.enable registry
```

c. Build and push 5G Ran images to registry

```bash
./build_docker_images.sh
docker push localhost:32000/ran:1.0
docker push localhost:32000/ue:1.0
```

d. Execute the following script to build all the 5G Ran charms using Charmcraft,

```bash
./build_charms.sh
```

e. Create a model in Juju and deploy 5G Ran,

```bash
juju add-model 5g-Ran
juju deploy ./bundle_local.yaml
```

f. Configuring interface

For the deployment to get completed successfully, update master_interface field
to your server's main interface name with the following command,

```bash
juju config ran master_interface="<interface_name>"
```

where interface_name stands for server's main interface name where ran is
deployed

### Integration

5G Ran exposes its following services in order to facilitate control plane and
data plane interactions with CORE,

* TCP Service - For Control Plane User Registration and Attach Scenario.
* UDP Service - For Data Transfer scneario

In order to achieve this, 5G Ran needs 2 Loadbalancer services to be exposed
and published. This is done using,

```bash
microk8s.enable metallb
```

#### Juju Actions:

Note: Make sure 5G-Core(https://github.com/charmed-osm/5g-core) is deployed and
5G-core actions are done before performing the following actions in 5G-RAN,

a. Action "config-gnb" is used to configure the gNB with the operator specific
parameters such as PLMN, Tracking area code, Global gNB Id, and the core
interfacing parameters such as AMF IP, UPF IP etc.,

```bash
juju run-action ran/<unit_id> config-gnb amf-ip='<AMF_LB_IP>' upf-ip='<UPF_LB_IP>'
```

where unit_id is the Unit number of the respective unit,
AMF_LB_IP and UPF_LB_IP are the respective loadbalancer IP addresses of
5G-Core's AMF and UPF applications.

b. Action "connect-amf" is used to initiate a SCTP connection with the AMF.
On a result of this action the core and RAN negotiate the parameters and NGAP
connection is established between RAN and Core.,

```bash
juju run-action ran/<unit_id> connect-amf
```

where unit_id is the Unit number of the respective unit,

c. Action "config-ue" which will be used to set UE’s context in RAN,

```bash
juju run-action ran/<unit_id> config-ue ue-mgmt-ip='<UE_eth0_IP>' ue-pdu-macaddress='<UE_eth1_mac>'
```

where unit_id is the Unit number of the respective unit,
UE_eth0_IP is the IP address of UE application's eth0 interface and
UE_eth1_mac is the mac address of UE application's eth1 interface.

After executing each action, an ID will be generated like below,
Action queued with id: "ID"
This ID can be used to check the action status using the following command,

```bash
juju show-action-output <ID>
```

Check for the status of the action in the output which should be "completed".

#### Actions Verification:

"config-gnb", "connect-amf" and "config-ue" actions can be verified in RAN
application pod in /var/log/free5gc.log file. The IP addresses of Core set,
the SCTP connection successful message and the UE application's IP and MAC
address set can be verified in this log file.

### 5G Scenarios

#### 5G User Registration

After 5G-Core(https://github.com/charmed-osm/5g-core) and 5G-RAN are deployed
and actions are completed, the user registration can be triggered through the
following rest API call with POST method,

```bash
http://ran-loadbalancerip:8081/attachtrigger/1
```

> Sample response for successful attach,
> Response Message: "Triggered Attach for the requested UE!"
> Response Code: 200 OK

#### Internet Traffic Flow

Once registration is successful, 5G-RAN's UE application would be enabled to
access the data network. Test the following in UE application,

a. ICMP TRAFFIC

```bash
ping 8.8.8.8
```

b. TCP TRAFFIC

```bash
wget google.com
```

c. UDP TRAFFIC

```bash
nc -u <netcat server-ip> port
```

where netcat server-ip is the IP address of the server where netcat server is
running.
Note: for UDP traffic netcat server should be running in another server. To do
that use the following commands in another server.

```bash
apt-get install netcat
nc -u -l -p <any unused port>
```

#### Voice Traffic Flow

Voice traffic flow can be tested once
5G-Core(https://github.com/charmed-osm/5g-core),
5G-RAN and 5G-IMS(https://github.com/charmed-osm/5g-ims) are deployed
and actions are completed. To test voice traffic flows, a SIP client called
PJSIP is already installed in the UE application. Follow the below steps,

a. Traverse to /pjproject directory in the UE pod.

b. alice.cfg is configured for an user named alice which is already available
in IMS by default.

Note: The username, password and id can be changed to any user added from day-2
action of IMS as well.

c. Add the following content to /etc/hosts file,

> <PCSCF_LB_IP> mnc001.mcc001.3gppnetwork.org
> <PCSCF-LB_IP> pcscf.mnc001.mcc001.3gppnetwork.org

Where <PCSCF-LB_IP> is the loadbalancer IP of PCSCF application and
mnc001.mcc001.3gppnetwork.org is the domain added in coredns of IMS cluster.

d. Execute the following command to register the user alice with IMS,

```bash
pjsua --config-file alice.cfg --log-level=3
```

Note: Peform the above steps to register another user say bob with IMS so that SIP calls
can be tested between the two users.

e. After registration of both users, press ‘m’ from UE application's alice
and then press enter to initiate a SIP call.

f. Give bob’s id and then press enter. The message “Calling”
can be observed in alice’s UE pod.

g. Then in bob’s server, the following message can be seen,

> Press ‘a’ to answer or ‘h’ to hangup

h. Press a and then enter. Then the following message will be displayed,

> Answer with code:

i. Type 200 and enter.

j. After this “Confirmed” message can be seen in both alice and bob
indicating that the call between alice and bob is successful and that RTP
packets are being sent between alice and bob. The same can be verified by
capturing SIP packets using ngrep, tcpdump or wireshark.

k. Then to end/hangup the call, press h and then enter from alice. Verify the
“Disconnected” message in both alice and bob.

## Testing

Run Integration and Unit tests to test and verify the 5G Ran Charms.

### Integration tests

Functional tests for 5G Ran were created using zaza.

#### Install tox

```bash
apt-get install tox
```

To run zaza integration test,

```bash
tox -e func_test
```

This command will create a model, deploy the charms, run tests and destroy the
model.

### Unit tests

Unit tests has to be executed in all the 5G Ran components/charms.
The following commands show how to perform unit test in RAN,

```bash
cd charms/ran-operator
./run_tests
```

Similarly, unit tests can be run for all the other components/charms.

## Get in touch

Found a bug?: <https://github.com/charmed-osm/5g-ran/issues>
Email: canonical@tataelxsi.onmicrosoft.com
