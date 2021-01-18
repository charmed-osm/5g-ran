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
```

#### B. Install Juju

a. Install Juju with the following commands,

```bash
sudo snap install juju --classic --channel 2.8/stable
juju bootstrap microk8s
```

### Deploy

To deploy 5G RAN Emulator from Charmstore, use the following command

```bash
juju deploy cs:~tataelxsi-charmers/ran-5g
```

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
