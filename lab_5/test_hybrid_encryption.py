"""
Unit tests for the HybridEncryption class.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from pathlib import Path
from HybridEncryption import HybridEncryption
from SymmetricCryptography import SymmetricCryptography
from AsymmetricCryptography import AsymmetricCryptography


class TestHybridEncryption:
    @pytest.fixture
    def setup_hybrid(self, tmp_path: Path) -> HybridEncryption:
        """
        Fixture to provide an instance of HybridEncryption with temporary paths.
        """
        text_path = tmp_path / "text.txt"
        symmetric_key_path = tmp_path / "symmetric.txt"
        encrypted_text_path = tmp_path / "encrypted_text.txt"
        decrypted_text_path = tmp_path / "decrypted_text.txt"

        symmetric_crypto = SymmetricCryptography(key_len=256)
        asymmetric_crypto = AsymmetricCryptography(
            private_key_path=tmp_path / "private.pem",
            public_key_path=tmp_path / "public.pem",
        )

        with open(text_path, "w") as f:
            f.write("Sample text for hybrid encryption")

        return HybridEncryption(
            str(text_path),
            str(symmetric_key_path),
            str(encrypted_text_path),
            str(decrypted_text_path),
            symmetric_crypto,
            asymmetric_crypto,
        )

    def test_generate_keys(self, setup_hybrid: HybridEncryption) -> None:
        """
        Test that keys are generated and the symmetric key file is created.
        """
        setup_hybrid.generate_keys()

        assert os.path.exists(setup_hybrid.symmetric_key_path), "Symmetric key file not found"
        assert os.path.exists(setup_hybrid.asymmetric_crypto.private_key_path), "Private key file not found"
        assert os.path.exists(setup_hybrid.asymmetric_crypto.public_key_path), "Public key file not found"

    def test_encrypt_decrypt_text(self, setup_hybrid: HybridEncryption) -> None:
        """
        Test encryption and decryption functionality.
        """
        setup_hybrid.generate_keys()
        setup_hybrid.encrypt_text()
        setup_hybrid.decrypt_text()

        with open(setup_hybrid.decrypted_text_path, "r") as f:
            decrypted_text = f.read()

        with open(setup_hybrid.text_path, "r") as f:
            original_text = f.read()

        assert decrypted_text == original_text

    def test_generate_keys_exception(self, setup_hybrid: HybridEncryption) -> None:
        """
        Test exception handling during key generation.
        """
        with patch.object(setup_hybrid.symmetric_crypto, "generate_key", side_effect=Exception("Test Exception")):
            with patch("logging.error") as mock_logging_error:
                setup_hybrid.generate_keys()
                mock_logging_error.assert_called_once_with("An error occurred while generating the keys: Test Exception")

    def test_encrypt_text_exception(self, setup_hybrid: HybridEncryption) -> None:
        """
        Test exception handling during text encryption.
        """
        with patch("CryptoUtility.CryptoUtility.deserialize_key", side_effect=Exception("Test Exception")):
            with patch("logging.error") as mock_logging_error:
                setup_hybrid.encrypt_text()
                mock_logging_error.assert_called_once_with("An error occurred while encrypting the text: Test Exception")

    def test_decrypt_text_exception(self, setup_hybrid: HybridEncryption) -> None:
        """
        Test exception handling during text decryption.
        """
        with patch("CryptoUtility.CryptoUtility.deserialize_key", side_effect=Exception("Test Exception")):
            with patch("logging.error") as mock_logging_error:
                setup_hybrid.decrypt_text()
                mock_logging_error.assert_called_once_with("An error occurred while decrypting the text: Test Exception")
