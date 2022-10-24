# Contributing guidelines

Thank you for investing your time to improve this tool.

## Pre-commit

We use pre-commit to unsure that that our code meets common standards and practices.
If you intend to contribute to this project, make sure to setup `pre-commit` and that it runs
before your code is pushed.

1. [Install pre-commit](https://pre-commit.com/#install)
   - It is also part of requirements-dev.txt and should be covered if you install those
1. Setup pre-commit to run before push
   ```bash
   pre-commit install --hook-type pre-push
   ```
1. Test
   ```bash
   pre-commit run --all-files
   ```

## pip-tools

### Update requirements

```bash
pip-compile requirements-dev.in
```
