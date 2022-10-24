# AWS Transplanter

AWS Transplanter is a tool that creates a tree structure of your
Organization and helps you understand its structure.

Why "AWS Transplanter"? It's what AWS would name it if it was a service.

## Usage

```bash
$ aws_transplanter --help
usage: AWS Transplanter [-h] [-r ROOT] [-rf REGEX_FILTER] [-o {json,yaml,tree}]

options:
  -h, --help            show this help message and exit
  -r ROOT, --root ROOT  AWS Organization 'root' or 'OU' Id to be explored. If not provided it will find the Organization root.
  -rf REGEX_FILTER, --regex-filter REGEX_FILTER
                        Regex to filter OUs or Account names. Default: ".*"
  -o {json,yaml,tree}, --output {json,yaml,tree}
                        Output type. Default: tree
```

## Examples

1.  Tree from `root`:

    ```bash
        $ aws_transplanter

        🏦 root (0)
        +--🏘 ou_1 (1)
        |   +--🏘 ou_2 (2)
        |   |   +--🏡 account_1 (1)
        +--🏡 account_2 (2)
    ```

2.  Tree from `ou_1`:

    ```bash
        $ aws_transplanter -r ou_1

        🏘 ou_1 (1)
        +--🏘 ou_2 (2)
        |   +--🏡 account_1 (1)
    ```

3.  Output `yaml` format:

    ```yaml
      $ aws_transplanter -o yaml

      children:
      - children:
        - children:
          - children: []
            id: '1'
            name: account_1
            type: 3
          id: '2'
          name: ou_2
          type: 2
        id: '1'
        name: ou_1
        type: 2
      - children: []
        id: '2'
        name: account_2
        type: 3
      id: '0'
      name: root
      type: 1
    ```
