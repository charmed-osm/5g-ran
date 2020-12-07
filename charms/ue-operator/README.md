# ran

## Description

Charm to deploy UE application pod.

## Usage

SSH has to be enabled inside pod with port 22 such that RAN application can modify the ip interface in UE pod


## Developing

Create and activate a virtualenv with the development requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

    ./run_tests
