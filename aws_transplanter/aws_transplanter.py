from __future__ import annotations

import argparse

from aws_transplanter.utils import aws_org_utils


def main() -> None:
    parser = argparse.ArgumentParser("AWS Transplanter")
    parser.add_argument(
        "-r",
        "--root",
        type=str,
        help="AWS Organization 'root' or 'OU' Id to be explored. "
        + "If not provided it will find the Organization root.",
    )
    parser.add_argument(
        "-rf",
        "--regex-filter",
        type=str,
        help='Regex to filter OUs or Account names. Default: ".*"',
        default=".*",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output type. Default: tree",
        choices=["json", "yaml", "tree"],
        default="tree",
    )
    args = parser.parse_args()

    if args.root:
        root = aws_org_utils.AwsOrganizationMember(
            args.root, "root", aws_org_utils.AwsOrganizationMemberType.ROOT
        )
    else:
        root = aws_org_utils.get_root()

    full_tree = aws_org_utils.get_deep_child_tree(
        parent=root, name_filter_regex=args.regex_filter
    )

    if args.output == "json":
        print(full_tree.toJSON())
    elif args.output == "yaml":
        print(full_tree.toYAML())
    elif args.output == "tree":
        print(full_tree.toAsciiTree())


if __name__ == "__main__":
    main()
