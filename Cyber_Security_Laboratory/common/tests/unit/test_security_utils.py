import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../common/src'))
from security_utils import SecurityUtils

class TestSecurityUtils(unittest.TestCase):
    def test_generate_secure_hash(self):
        # Test hash generation
        test_data = "test_password"
        result = SecurityUtils.generate_secure_hash(test_data)
        
        self.assertIn("hash", result)
        self.assertIn("salt", result)
        self.assertTrue(isinstance(result["hash"], str))
        self.assertTrue(isinstance(result["salt"], str))
        
    def test_verify_hash(self):
        # Test hash verification
        test_data = "test_password"
        hash_result = SecurityUtils.generate_secure_hash(test_data)
        
        # Verify correct password
        self.assertTrue(
            SecurityUtils.verify_hash(
                test_data, 
                hash_result["hash"],
                hash_result["salt"]
            )
        )
        
        # Verify incorrect password
        self.assertFalse(
            SecurityUtils.verify_hash(
                "wrong_password",
                hash_result["hash"],
                hash_result["salt"]
            )
        )
        
    def test_generate_secure_token(self):
        # Test token generation
        token = SecurityUtils.generate_secure_token()
        self.assertTrue(isinstance(token, str))
        self.assertTrue(len(token) > 0)
        
        # Test different lengths
        token_20 = SecurityUtils.generate_secure_token(20)
        token_40 = SecurityUtils.generate_secure_token(40)
        self.assertNotEqual(len(token_20), len(token_40))

if __name__ == '__main__':
    unittest.main()