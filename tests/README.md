> Please, format the readme properly
> These commands do not work. Make sure the steps are clear, complete, and of course working.
> If the main readme is complete, you may not need this one.

To run the RAN FT:

Command to create venv:
   tox -e test  #test is the venv created for RAN inorder to install sctp-dev package

Command to login inside venv:
   .tox/test/bin/activate

Command to test all functional charms:
   functest-run-suite -b bundle

Command to prepare model:
   functest-prepare -m <model-name>

Command to deploy bundle:
   functest-deploy -m <model-name> -b ./tests/bundle/bundle.yaml

Command to test the FT script:
   functest-test -m <model-name>
