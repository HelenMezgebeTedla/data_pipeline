

import os
import logging

log = logging.getLogger("pipeline.security.secrets")


class SecretNotConfigured(Exception):



def get_secret(name: str, default=None, required: bool = False) -> str:

    value = os.environ.get(name)
    if value:
        return value

    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project:
        try:
            from google.cloud import secretmanager

            client = secretmanager.SecretManagerServiceClient()
            name_path = f"projects/{project}/secrets/{name}/versions/latest"
            response = client.access_secret_version(request={"name": name_path})
            return response.payload.data.decode("UTF-8")
        except Exception as exc:
            log.debug("Secret Manager lookup for %s failed: %s", name, exc)

    if default is not None:
        return default

    if required:
        raise SecretNotConfigured(f"Required secret not configured: {name}")
    return ""