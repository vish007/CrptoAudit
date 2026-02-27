"""Unit tests for security utilities."""
import uuid
from datetime import timedelta, datetime, timezone

import pytest
from jose import jwt

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token,
    setup_mfa_secret,
    verify_mfa_token,
    extract_tenant_id,
    extract_user_id,
)
from app.core.config import settings


@pytest.mark.unit
class TestPasswordHashing:
    """Tests for password hashing and verification."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > 0

    def test_hash_password_different_each_time(self):
        """Test that same password produces different hashes."""
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2

    def test_verify_password_valid(self):
        """Test verifying correct password."""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_invalid(self):
        """Test verifying incorrect password."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        wrong_password = "WrongPassword123!"

        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty(self):
        """Test verifying empty password."""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert verify_password("", hashed) is False


@pytest.mark.unit
class TestTokenManagement:
    """Tests for JWT token creation and verification."""

    def test_create_access_token(self):
        """Test creating access token."""
        data = {"sub": str(uuid.uuid4()), "email": "test@example.com"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_expiry(self):
        """Test creating token with custom expiry."""
        data = {"sub": str(uuid.uuid4())}
        expires_delta = timedelta(hours=1)
        token = create_access_token(data, expires_delta)

        assert isinstance(token, str)

    def test_verify_valid_token(self):
        """Test verifying valid token."""
        user_id = str(uuid.uuid4())
        data = {"sub": user_id, "email": "test@example.com"}
        token = create_access_token(data)

        payload = verify_token(token)

        assert payload["sub"] == user_id
        assert payload["email"] == "test@example.com"

    def test_verify_expired_token(self):
        """Test that expired token raises error."""
        user_id = str(uuid.uuid4())
        data = {"sub": user_id}
        # Create token that expires immediately
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta)

        with pytest.raises(Exception):
            verify_token(token)

    def test_verify_invalid_token(self):
        """Test that invalid token raises error."""
        invalid_token = "invalid.token.here"

        with pytest.raises(Exception):
            verify_token(invalid_token)

    def test_verify_tampered_token(self):
        """Test that tampered token is rejected."""
        user_id = str(uuid.uuid4())
        data = {"sub": user_id}
        token = create_access_token(data)

        # Tamper with token
        tampered_token = token[:-10] + "corrupted"

        with pytest.raises(Exception):
            verify_token(tampered_token)

    def test_token_contains_claims(self):
        """Test that token contains all claims."""
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
        data = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "email": "test@example.com",
            "is_active": True,
        }
        token = create_access_token(data)

        payload = verify_token(token)

        assert payload["sub"] == user_id
        assert payload["tenant_id"] == tenant_id
        assert payload["email"] == "test@example.com"
        assert payload["is_active"] is True


@pytest.mark.unit
class TestMFASetup:
    """Tests for MFA secret generation and verification."""

    def test_setup_mfa_secret(self):
        """Test MFA secret setup."""
        email = "test@example.com"
        secret, provisioning_uri = setup_mfa_secret(email)

        assert isinstance(secret, str)
        assert len(secret) > 0
        assert isinstance(provisioning_uri, str)
        assert "otpauth://" in provisioning_uri

    def test_verify_mfa_token_valid(self):
        """Test verifying valid MFA token."""
        email = "test@example.com"
        secret, _ = setup_mfa_secret(email)

        # Generate a valid token
        import pyotp
        totp = pyotp.TOTP(secret)
        token = totp.now()

        assert verify_mfa_token(secret, token) is True

    def test_verify_mfa_token_invalid(self):
        """Test verifying invalid MFA token."""
        email = "test@example.com"
        secret, _ = setup_mfa_secret(email)

        assert verify_mfa_token(secret, "000000") is False


@pytest.mark.unit
class TestPermissionExtraction:
    """Tests for extracting user claims from tokens."""

    def test_extract_tenant_id(self):
        """Test extracting tenant ID."""
        tenant_id = str(uuid.uuid4())
        current_user = {"tenant_id": tenant_id, "sub": str(uuid.uuid4())}

        result = extract_tenant_id(current_user)

        assert result == tenant_id

    def test_extract_tenant_id_missing(self):
        """Test that missing tenant ID raises error."""
        current_user = {"sub": str(uuid.uuid4())}

        with pytest.raises(Exception):
            extract_tenant_id(current_user)

    def test_extract_user_id(self):
        """Test extracting user ID."""
        user_id = str(uuid.uuid4())
        current_user = {"sub": user_id, "email": "test@example.com"}

        result = extract_user_id(current_user)

        assert result == user_id

    def test_extract_user_id_missing(self):
        """Test that missing user ID raises error."""
        current_user = {"email": "test@example.com"}

        with pytest.raises(Exception):
            extract_user_id(current_user)


@pytest.mark.unit
class TestTokenSecurity:
    """Tests for token security features."""

    def test_token_expiration(self):
        """Test that tokens have expiration claim."""
        data = {"sub": str(uuid.uuid4())}
        token = create_access_token(data)

        payload = verify_token(token)

        assert "exp" in payload
        assert "iat" in payload

    def test_token_algorithm(self):
        """Test that token uses correct algorithm."""
        data = {"sub": str(uuid.uuid4())}
        token = create_access_token(data)

        # Decode without verification to check header
        unverified = jwt.get_unverified_header(token)
        assert unverified["alg"] == settings.JWT_ALGORITHM

    def test_access_token_default_expiry(self):
        """Test that access token has default expiry."""
        data = {"sub": str(uuid.uuid4())}
        token = create_access_token(data)

        payload = verify_token(token)

        # Check that expiry is approximately in the future
        exp_time = payload["exp"]
        iat_time = payload["iat"]

        # Should be roughly ACCESS_TOKEN_EXPIRE_MINUTES apart
        diff_minutes = (exp_time - iat_time) / 60
        expected_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

        assert abs(diff_minutes - expected_minutes) < 1  # Allow 1 minute variance
