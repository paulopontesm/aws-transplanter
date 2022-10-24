import pytest

from aws_transplanter.utils.aws_org_utils import (  # fmt: off
    AwsOrganizationMember,
    AwsOrganizationMemberType,
)


class TestAwsOrganizationMember:
    @pytest.fixture
    def org_tree(self) -> AwsOrganizationMember:

        root = AwsOrganizationMember(
            "0", "root", AwsOrganizationMemberType.ROOT
        )
        ou_1 = AwsOrganizationMember("1", "ou_1", AwsOrganizationMemberType.OU)
        ou_2 = AwsOrganizationMember("2", "ou_2", AwsOrganizationMemberType.OU)
        account_1 = AwsOrganizationMember(
            "1", "account_1", AwsOrganizationMemberType.ACCOUNT
        )
        account_2 = AwsOrganizationMember(
            "2", "account_2", AwsOrganizationMemberType.ACCOUNT
        )
        root.children.append(ou_1)
        ou_1.children.append(ou_2)
        ou_2.children.append(account_1)
        root.children.append(account_2)

        return root

    def test_toAsciiTree(self, org_tree: AwsOrganizationMember) -> None:
        print(org_tree.toAsciiTree())
        expected = """🏦 root (0)
 +--🏘 ou_1 (1)
 |   +--🏘 ou_2 (2)
 |   |   +--🏡 account_1 (1)
 +--🏡 account_2 (2)"""

        assert org_tree.toAsciiTree() == expected

    def test_toYAML(self, org_tree: AwsOrganizationMember) -> None:
        print(org_tree.toYAML())
        expected = """children:
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
"""
        assert org_tree.toYAML() == expected

    def test_toJSON(self, org_tree: AwsOrganizationMember) -> None:
        print(org_tree.toJSON())
        expected = """{"id": "0", "name": "root", "type": 1, "children": [{"id": "1", "name": "ou_1", "type": 2, "children": [{"id": "2", "name": "ou_2", "type": 2, "children": [{"id": "1", "name": "account_1", "type": 3, "children": []}]}]}, {"id": "2", "name": "account_2", "type": 3, "children": []}]}"""
        assert org_tree.toJSON() == expected
