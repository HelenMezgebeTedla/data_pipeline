

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Set


class Role:
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"


ALL_ROLES = (Role.VIEWER, Role.ANALYST, Role.ADMIN)


@dataclass
class DataAccessPolicy:


    grants: Dict[str, Set[str]] = field(default_factory=dict)

    def grant(self, role: str, table_ref: str) -> None:
        self.grants.setdefault(role, set()).add(table_ref)

    def allowed(self, role: str, table_ref: str) -> bool:
        return table_ref in self.grants.get(role, set())


DEFAULT_POLICY = DataAccessPolicy()
DEFAULT_POLICY.grant(Role.VIEWER, "grants.summary")
DEFAULT_POLICY.grant(Role.VIEWER, "people.directory")
DEFAULT_POLICY.grant(Role.ANALYST, "grants.summary")
DEFAULT_POLICY.grant(Role.ANALYST, "grants.details")
DEFAULT_POLICY.grant(Role.ANALYST, "finance.transactions")
DEFAULT_POLICY.grant(Role.ANALYST, "people.directory")
DEFAULT_POLICY.grant(Role.ADMIN, "grants.summary")
DEFAULT_POLICY.grant(Role.ADMIN, "grants.details")
DEFAULT_POLICY.grant(Role.ADMIN, "finance.transactions")
DEFAULT_POLICY.grant(Role.ADMIN, "people.directory")
DEFAULT_POLICY.grant(Role.ADMIN, "people.salaries")


def principal_has_access(role: str, table_ref: str, policy: DataAccessPolicy) -> bool:

    if role not in ALL_ROLES:
        return False
    return policy.allowed(role, table_ref)