# Setup pre-commit hook
This repository contains a pre-commit hook to ensure that files added in commits are correctly styled and formatted. The pre-commit hook is defined in `.pre-commit-config.yaml` and runs `black` to format code, `isort` to organise imports and `flake8` to lint and check conformance with PEP recommendations. 

To install the pre-commit hook to your local `.git` first install `pre-commit`
```shell
pip install pre-commit
```
then install the hook:
```shell
pre-commit install
```
The hook will then be run whenever you perform a commit and report on any failures. You can check this is working by manually running the hook on all files:
```shell
pre-commit run --all-files
```
