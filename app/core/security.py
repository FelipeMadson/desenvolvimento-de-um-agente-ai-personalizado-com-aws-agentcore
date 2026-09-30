import hmac
import hashlib
import time
import json
import base64
from typing import Optional, Dict, Any
from app.core.config import settings

class SecurityService:
    @staticmethod
    def create_api_token(tenant_id: str, role: str = "member", ttl_seconds: int = 86400) -> str:
        payload = {
            "tenant_id": tenant_id,
            "role": role,
            "exp": int(time.time()) + ttl_seconds
        }
        encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
        signature = hmac.new(
            settings.SECRET_KEY.encode(),
            encoded_payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"ai_{encoded_payload}.{signature}"

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        if not token or not token.startswith("ai_"):
            return None
        parts = token[3:].split(".")
        if len(parts) != 2:
            return None
        encoded_payload, received_sig = parts
        expected_sig = hmac.new(
            settings.SECRET_KEY.encode(),
            encoded_payload.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(received_sig, expected_sig):
            return None

        try:
            payload = json.loads(base64.urlsafe_b64decode(encoded_payload.encode()).decode())
            if time.time() > payload.get("exp", 0):
                return None
            return payload
        except Exception:
            return None
