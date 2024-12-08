import pytest
from AsymmetricCryptography import AsymmetricCryptography
from cryptography.hazmat.primitives.asymmetric import rsa
import os

class TestAsymmetricCryptography:
    @pytest.fixture
    def asymmetric_crypto(self, tmp_path):
        private_key_path = tmp_path / "private.pem"
        public_key_path = tmp_path / "public.pem"
        return AsymmetricCryptography(str(private_key_path), str(public_key_path))
    
    @pytest.mark.parametrize("key_size", [2048, 4096])
    def test_generate_key_pair(self, asymmetric_crypto, key_size):
        private_key, public_key = asymmetric_crypto.generate_key_pair(key_size)
        assert isinstance(private_key, rsa.RSAPrivateKey)
        assert isinstance(public_key, rsa.RSAPublicKey)
    
    def test_key_serialization_and_deserialization(self, asymmetric_crypto):
        private_key, public_key = asymmetric_crypto.generate_key_pair(2048)
        asymmetric_crypto.serialize_private_key(private_key)
        asymmetric_crypto.serialize_public_key(public_key)

        deserialized_private_key = asymmetric_crypto.deserialize_private_key()
        deserialized_public_key = asymmetric_crypto.deserialize_public_key()

        assert deserialized_private_key.private_numbers() == private_key.private_numbers()
        assert deserialized_public_key.public_numbers() == public_key.public_numbers()
    
    @pytest.mark.parametrize("text,expected_encrypted", [
        (b"Test data for encryption", True),
        (b"Another piece of data", True),
        (b"Sensitive information!", True),
    ])
    def test_encrypt_decrypt_with_keys(self, asymmetric_crypto, text, expected_encrypted):
        private_key, public_key = asymmetric_crypto.generate_key_pair(2048)

        encrypted_text = asymmetric_crypto.encrypt_with_public_key(public_key, text)
        assert encrypted_text != text if expected_encrypted else True

        decrypted_text = asymmetric_crypto.decrypt_with_private_key(private_key, encrypted_text)
        assert decrypted_text == text
