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

osm package-create vnf ran
osm package-create ns ran

charms="ran-operator ue-operator"


for charm_directory in $charms; do
    mkdir -p "ran_vnf/charms/$charm_directory" && \
    cp -rf ../charms/$charm_directory/build "ran_vnf/charms/$charm_directory"
done

mkdir -p "ran_vnf/juju-bundles" && cp bundle.yaml "ran_vnf/juju-bundles"

cp ran_vnfd.yaml "ran_vnf/"
cp ran_nsd.yaml "ran_ns/"

tar -cvzf ran_vnf.tar.gz ran_vnf/
tar -cvzf ran_ns.tar.gz ran_ns/
