# 5G RAN Operators

Contains charm folder consisting of 2 k8s charm applications


## Description

Consists of 2 applications
* ue
* ran

## Usage
Build

sudo snap install charmcraft --beta

cd Application-operator
  
charmcraft build
  
Deploy

juju deploy ./juju-bundles/bundle.yaml

### Integration

Ran integration with core using loadbalancer service for SCTP and Attach trigger
