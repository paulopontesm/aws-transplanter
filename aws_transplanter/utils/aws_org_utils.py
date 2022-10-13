from __future__ import annotations

import json
import re
from copy import deepcopy
from enum import Enum, auto

import boto3
import yaml
from mypy_boto3_organizations import Client
from mypy_boto3_organizations.type_defs import (
    ListAccountsForParentResponseTypeDef,
    ListOrganizationalUnitsForParentResponseTypeDef,
    ListRootsResponseTypeDef,
)


class AwsOrganizationMemberType(Enum):
    ROOT = auto()
    OU = auto()
    ACCOUNT = auto()
    SERVICE_CONTROL_POLICY = auto()


client: Client = boto3.client("organizations")

_MEMBER_ICON_MAP = {
    AwsOrganizationMemberType.ROOT: "🏦",
    AwsOrganizationMemberType.OU: "🏘",
    AwsOrganizationMemberType.ACCOUNT: "🏡",
}


class AwsOrganizationMember:
    id: str
    name: str
    type: AwsOrganizationMemberType
    children: list[AwsOrganizationMember]

    def __init__(
        self,
        _id: str,
        _name: str,
        _type: AwsOrganizationMemberType,
    ) -> None:
        self.id = _id
        self.name = _name
        self.type = _type
        self.children = []

    def __repr__(self) -> str:
        return f"Id: {self.id}, Name: {self.name}"

    def toYAML(self) -> str:
        return yaml.safe_dump(json.loads(self.toJSON()))

    def toJSON(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "name": self.name,
                "type": self.type.value,
                "children": [c.toJSON() for c in self.children],
                "children": [json.loads(c.toJSON()) for c in self.children],
            }
        )

    def toAsciiTree(self, base_level: int = 0) -> str:
        output: str = ""
        tab = ""
        if base_level > 0:
            tab = " |  " * (base_level - 1)
            output += tab
            output += " +--"
        output += _MEMBER_ICON_MAP[self.type]
        output += " "
        output += self.name
        output += " "
        output += "(" + self.id + ")"
        for c in self.children:
            output += "\n"
            output += c.toAsciiTree(base_level + 1)

        return output


def get_root() -> AwsOrganizationMember:
    response: ListRootsResponseTypeDef = client.list_roots()
    root = response["Roots"][0]
    return AwsOrganizationMember(
        root["Id"], root["Name"], AwsOrganizationMemberType.ROOT
    )


def get_organizations(
    parent_id: str, name_filter_regex: str = ".*"
) -> list[AwsOrganizationMember]:
    organization_units: list[AwsOrganizationMember] = []

    response: ListOrganizationalUnitsForParentResponseTypeDef = (
        client.list_organizational_units_for_parent(ParentId=parent_id)
    )
    organization_units_list = response["OrganizationalUnits"]

    while "NextToken" in response:
        response = client.list_organizational_units_for_parent(
            ParentId=parent_id, NextToken=response["NextToken"]
        )
        organization_units_list.extend(response["OrganizationalUnits"])

    for ou in organization_units_list:
        if re.search(name_filter_regex, ou["Name"]):
            new_org = AwsOrganizationMember(
                ou["Id"], ou["Name"], AwsOrganizationMemberType.OU
            )
            organization_units.append(new_org)

    return organization_units


def get_accounts_for_org(
    parent_id: str, name_filter_regex: str = ".*"
) -> list[AwsOrganizationMember]:
    accounts: list[AwsOrganizationMember] = []

    response: ListAccountsForParentResponseTypeDef = (
        client.list_accounts_for_parent(ParentId=parent_id)
    )
    accounts_list = response["Accounts"]

    while "NextToken" in response:
        response = client.list_accounts_for_parent(
            ParentId=parent_id, NextToken=response["NextToken"]
        )
        accounts_list.extend(response["Accounts"])

    for a in accounts_list:
        if re.search(name_filter_regex, a["Name"]):
            new_acc = AwsOrganizationMember(
                a["Id"], a["Name"], AwsOrganizationMemberType.ACCOUNT
            )

            accounts.append(new_acc)

    return accounts


def get_deep_child_tree(
    parent: AwsOrganizationMember,
    get_accounts: bool = True,
    name_filter_regex: str = ".*",
) -> AwsOrganizationMember:
    """Gets the full tree of child AWS OUs and Accounts for a given AWS Org.

    root = get_child_members(root)

    Args:
        parent (AwsOrganizationMember): The AwsOrganizationMember for which
            childs should be retrieved
        get_accounts (boot): If `false` it will get only the child OUs and
            ignore AWS Accounts

    Returns:
        AwsOrganizationMember: The AwsOrganizationMember object filled with
            all the children
    """
    if parent.type == AwsOrganizationMemberType.ACCOUNT:
        return parent

    res: AwsOrganizationMember = deepcopy(parent)
    organizations = get_organizations(parent.id, name_filter_regex)
    for o in organizations:
        o = get_deep_child_tree(o, get_accounts, name_filter_regex)
        res.children.append(o)

    if get_accounts:
        accounts = get_accounts_for_org(parent.id, name_filter_regex)
        res.children.extend(accounts)
    return res
