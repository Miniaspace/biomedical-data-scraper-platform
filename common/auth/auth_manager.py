"""
Authentication Manager

Centralized credential management for all platforms.
Supports multiple authentication methods and secure credential storage.
"""

import os
import yaml
import logging
from typing import Dict, Optional, Any
from cryptography.fernet import Fernet
import base64
from pathlib import Path


class AuthManager:
    """
    Manages authentication credentials for all platforms.
    
    Features:
    - Encrypted credential storage
    - Multiple authentication methods (Basic, OAuth, API Key, Session)
    - Credential rotation support
    - Audit logging
    """
    
    def __init__(self, config_path: str = "config/credentials.yaml", 
                 encryption_key: Optional[str] = None):
        """
        Initialize the authentication manager.
        
        Args:
            config_path: Path to credentials configuration file
            encryption_key: Encryption key for sensitive data (from env var if not provided)
        """
        self.config_path = Path(config_path)
        self.logger = logging.getLogger('auth_manager')
        
        # Initialize encryption
        self.encryption_key = encryption_key or os.getenv('CREDENTIAL_ENCRYPTION_KEY')
        if self.encryption_key:
            self.cipher = Fernet(self.encryption_key.encode())
        else:
            self.logger.warning("No encryption key provided. Credentials will not be encrypted.")
            self.cipher = None
        
        # Load credentials
        self.credentials = self._load_credentials()
        
        self.logger.info(f"AuthManager initialized with {len(self.credentials)} platforms")
    
    def _load_credentials(self) -> Dict[str, Dict[str, Any]]:
        """
        Load credentials from configuration file.
        
        Returns:
            Dictionary of platform credentials
        """
        if not self.config_path.exists():
            self.logger.warning(f"Credentials file not found: {self.config_path}")
            return {}
        
        try:
            with open(self.config_path, 'r') as f:
                raw_credentials = yaml.safe_load(f) or {}
            
            # Decrypt sensitive fields if encryption is enabled
            if self.cipher:
                return self._decrypt_credentials(raw_credentials)
            else:
                return raw_credentials
                
        except Exception as e:
            self.logger.error(f"Failed to load credentials: {e}")
            return {}
    
    def _decrypt_credentials(self, credentials: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Decrypt sensitive credential fields.
        
        Args:
            credentials: Raw credentials dictionary
            
        Returns:
            Decrypted credentials dictionary
        """
        decrypted = {}
        
        for platform, creds in credentials.items():
            decrypted[platform] = {}
            for key, value in creds.items():
                if key in ['password', 'api_key', 'secret', 'token']:
                    try:
                        # Decrypt if value is encrypted (starts with 'enc:')
                        if isinstance(value, str) and value.startswith('enc:'):
                            encrypted_value = value[4:]  # Remove 'enc:' prefix
                            decrypted_value = self.cipher.decrypt(encrypted_value.encode()).decode()
                            decrypted[platform][key] = decrypted_value
                        else:
                            decrypted[platform][key] = value
                    except Exception as e:
                        self.logger.error(f"Failed to decrypt {key} for {platform}: {e}")
                        decrypted[platform][key] = value
                else:
                    decrypted[platform][key] = value
        
        return decrypted
    
    def get_credentials(self, platform: str) -> Optional[Dict[str, Any]]:
        """
        Get credentials for a specific platform.
        
        Args:
            platform: Platform name
            
        Returns:
            Credentials dictionary or None if not found
        """
        creds = self.credentials.get(platform)
        
        if creds:
            self.logger.info(f"Retrieved credentials for platform: {platform}")
        else:
            self.logger.warning(f"No credentials found for platform: {platform}")
        
        return creds
    
    def add_credentials(self, platform: str, credentials: Dict[str, Any], 
                       encrypt: bool = True) -> bool:
        """
        Add or update credentials for a platform.
        
        Args:
            platform: Platform name
            credentials: Credentials dictionary
            encrypt: Whether to encrypt sensitive fields
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Encrypt sensitive fields if requested
            if encrypt and self.cipher:
                credentials = self._encrypt_sensitive_fields(credentials)
            
            # Update in-memory credentials
            self.credentials[platform] = credentials
            
            # Save to file
            self._save_credentials()
            
            self.logger.info(f"Added/updated credentials for platform: {platform}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add credentials for {platform}: {e}")
            return False
    
    def _encrypt_sensitive_fields(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encrypt sensitive credential fields.
        
        Args:
            credentials: Raw credentials dictionary
            
        Returns:
            Credentials with encrypted sensitive fields
        """
        encrypted = {}
        
        for key, value in credentials.items():
            if key in ['password', 'api_key', 'secret', 'token'] and isinstance(value, str):
                encrypted_value = self.cipher.encrypt(value.encode()).decode()
                encrypted[key] = f"enc:{encrypted_value}"
            else:
                encrypted[key] = value
        
        return encrypted
    
    def _save_credentials(self):
        """Save credentials to configuration file."""
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                yaml.dump(self.credentials, f, default_flow_style=False)
            
            self.logger.info("Credentials saved successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to save credentials: {e}")
            raise
    
    def remove_credentials(self, platform: str) -> bool:
        """
        Remove credentials for a platform.
        
        Args:
            platform: Platform name
            
        Returns:
            True if successful, False otherwise
        """
        if platform in self.credentials:
            del self.credentials[platform]
            self._save_credentials()
            self.logger.info(f"Removed credentials for platform: {platform}")
            return True
        else:
            self.logger.warning(f"No credentials found for platform: {platform}")
            return False
    
    def list_platforms(self) -> list:
        """
        List all platforms with stored credentials.
        
        Returns:
            List of platform names
        """
        return list(self.credentials.keys())
    
    def validate_credentials(self, platform: str) -> bool:
        """
        Validate that required credential fields are present.
        
        Args:
            platform: Platform name
            
        Returns:
            True if valid, False otherwise
        """
        creds = self.get_credentials(platform)
        
        if not creds:
            return False
        
        # Check for required fields based on auth method
        auth_method = creds.get('auth_method', 'basic')
        
        if auth_method == 'basic':
            required = ['username', 'password']
        elif auth_method == 'api_key':
            required = ['api_key']
        elif auth_method == 'oauth':
            required = ['client_id', 'client_secret']
        elif auth_method == 'session':
            required = ['session_token']
        else:
            self.logger.warning(f"Unknown auth method: {auth_method}")
            return False
        
        missing = [field for field in required if field not in creds]
        
        if missing:
            self.logger.error(f"Missing required fields for {platform}: {missing}")
            return False
        
        return True


# Utility function to generate encryption key
def generate_encryption_key() -> str:
    """
    Generate a new encryption key for credential storage.
    
    Returns:
        Base64-encoded encryption key
    """
    return Fernet.generate_key().decode()


if __name__ == "__main__":
    # Example usage
    print("Generated encryption key:")
    print(generate_encryption_key())
    print("\nSet this as CREDENTIAL_ENCRYPTION_KEY environment variable")
