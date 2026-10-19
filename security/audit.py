

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class AuditEvent:
    DATA_ACCESS = "data_access"
    SECRET_ACCESS = "secret_access"
    PIPELINE_RUN = "pipeline_run"
    AUTHZ_DENIED = "authz_denied"


@dataclass
class AuditRecord:
    event: str
    actor: str
    resource: str
    outcome: str
    detail: Optional[Dict[str, Any]] = None
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if not self.timestamp:
            data["timestamp"] = datetime.now(timezone.utc).isoformat()
        return data


class AuditLogger:
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger("pipeline.security.audit")

    def log(self, record: AuditRecord) -> None:
        self.logger.info("AUDIT %s", json.dumps(record.to_dict()))


_audit = AuditLogger()


def audit_log(
    event: str,
    actor: str,
    resource: str,
    outcome: str,
    detail: Optional[Dict[str, Any]] = None,
) -> None:
    _audit.log(AuditRecord(event=event, actor=actor, resource=resource, outcome=outcome, detail=detail))