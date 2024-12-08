import pytest
from SymmetricCryptography import SymmetricCryptography

class TestSymmetricCryptography:
    @pytest.fixture
    def symmetric_crypto(self):
        return SymmetricCryptography(key_len=256)
    
    def test_generate_key(self, symmetric_crypto):
        key = symmetric_crypto.generate_key()
        assert len(key) == 32

    def test_encrypt_decrypt_text(self, symmetric_crypto):
        symmetric_key = symmetric_crypto.generate_key()
        text = b"Test data for encryption"
        encrypted_text = symmetric_crypto.encrypt_text(symmetric_key, text)
        assert encrypted_text != text

        decrypted_text = symmetric_crypto.decrypt_text(symmetric_key, encrypted_text)
        assert decrypted_text == text
