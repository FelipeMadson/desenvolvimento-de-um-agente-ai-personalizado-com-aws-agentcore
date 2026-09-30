import unittest
from app.core.security import SecurityService

class TestSecurityService(unittest.TestCase):
    def test_generate_and_verify_token(self):
        token = SecurityService.create_api_token("tenant_corp", "admin", ttl_seconds=3600)
        self.assertTrue(token.startswith("ai_"))

        payload = SecurityService.verify_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["tenant_id"], "tenant_corp")
        self.assertEqual(payload["role"], "admin")

    def test_tampered_token_fails(self):
        token = SecurityService.create_api_token("tenant_corp", "admin")
        parts = token.split(".")
        tampered = f"{parts[0]}.forged_signature_12345"
        self.assertIsNone(SecurityService.verify_token(tampered))
