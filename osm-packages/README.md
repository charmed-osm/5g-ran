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

# Create and Onboard 5g-ran osm packages

> To create osm vnf and ns packages, use the following commands which will
> generate a vnf package structure named ran_vnf and ns package structure named
> ran_ns

```bash
osm package-create vnf ran
osm package-create ns ran
```

> Copy the desriptor into corresponding directory

```bash
cp ran_vnfd.yaml ran_vnf/
cp ran_nsd.yaml ran_ns/
```

Note: Inorder to attach to 5g-core, ensure to change amf-ip, db-ip, upf-ip under
day1 action(config-gnb) section of ran_vnfd.yaml.
These are the external loadbalancer ips of amf,upf and mongodb service
running in 5g-core.

> To place the bundles in vnf package

```bash
mkdir -p "ran_vnf/juju-bundles" && cp ../bundle/bundle.yaml "ran_vnf/juju-bundles"
```

> To onboard packages into OSM, use the following commands

```bash
osm nfpkg-create ran_vnf
osm nspkg-create ran_ns
```

> Onboarded packages can be verified with the following commands

```bash
osm nfpkg-list
osm nspkg-list
```

# Adding vim-account and k8scluster to OSM

## Vim-Account

```bash
osm vim-create --name <vim_name> --user <username> --password <password>
 --auth_url <openstack-url> --tenant <tenant_name> --account_type openstack
```

vim-create command helps to add vim to OSM where,

- "vim_name" is the name of the vim being created.

- "username"and "password" are the credentials of Openstack.

- "tenant_name" is the tenant to be associated to the user in the Openstack.

- "openstack-url" is the URL of Openstack which will be used as VIM

## K8sCluster

```bash
osm k8scluster-add --creds <kube.yaml> --version '1.19' --vim <vim_name>
 --description "RAN Cluster"
 --k8s-nets '{"net1": "<network-name>"}' <cluster_name>
```

K8scluster add helps to attach a cluster with OSM which will be used for
knf deployment.
where

-"kube.yaml" is the configuration of microk8s cluster obtained from
"microk8s config>kube.yaml".

-"vim_name" is the vim created in the last setup.

-"cluster_name" a unique name to identify your cluster.

Note:[Prerequisites and microk8s setup for 5g-core](../README.md)

# Launching the 5g-ran

```bash
osm ns-create --ns_name ran --nsd_name ran_nsd --vim_account <vim_name>
```

> ns-create will instantiate the 5g-ran network service use
> "vim_name" thats added to osm.

## Verifying the services

```bash
osm ns-list
```

> Will display the ns-created with ns-id, with status active and configured
> which means the service is up along with its day1 operations.

```bash
osm ns-show
```

> Will show detailed information of the network service.

```bash
microk8s kubectl get all –n ran-kdu-<ns-id>
```

> will dispaly 2 components deployed from bundle in vnfd.

## 5g-ran day2 operation

```bash
osm ns-action ran --vnf_name 1 --kdu_name ran-kdu --action_name config-ue
 --params '{application-name: ran,msin: "00007487",mcc: 208,mnc: 93,
routing-indicator: "0fff",k: 5463,opc: 451011,ue-mgmt-ip: "10.1.135.52",
pdu-session-id: 1,data-network-name: internet,
ue-pdu-macaddress: "8e:14:95:4b:b0:29",sst: 1,sd: "010203",
protection-scheme : "" }'
```

where
. "ran" refers to the network service name,"1" points to vnf member index and
"ran-kdu" is the kdu name used in package.

. Parameters values to be used are as follows,
msin: "00007487", should match digits of imsi number 20893*00007487* added in core.
mcc: 208, should match the digits of imsi number *208*9300007487 added in core.
mnc: 93, should match the digits of imsi number 208*93*00007487 added in
core.ue-mgmt-ip: "10.1.135.5", ue managemet ip is UE pod's eth0 interface ip.
ue-pdu-macaddress: "8e:14:95:4b:b0:29", ue pod's eth1 interface mac address
