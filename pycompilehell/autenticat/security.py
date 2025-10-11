# autenticat/security.py
import bcrypt
import secrets
import hashlib
import hmac
from typing import Optional, Tuple

class SecurityManager:
    """
    Gerenciador de segurança simplificado
    """
    
    def __init__(self, secret_key: str = None, pepper: str = None):
        self.secret_key = secret_key or "chave_secreta_padrao"
        self.pepper = pepper or "pimenta_padrao"

    def hash_password(self, password: str) -> str:
        """Hash seguro da senha usando bcrypt com pepper"""
        password_peppered = password + self.pepper
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_peppered.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica se a senha corresponde ao hash"""
        try:
            password_peppered = password + self.pepper
            return bcrypt.checkpw(password_peppered.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False

    def generate_secure_token(self, length: int = 32) -> str:
        """Gera token seguro"""
        return secrets.token_urlsafe(length)

    def generate_xor_key(self, user_id: str, username: str, key_length: int = 32) -> str:
        """Gera chave XOR única e reproduzível"""
        base_string = f"{user_id}{username}{self.secret_key}"
        salt = user_id.encode('utf-8')
        key = hashlib.pbkdf2_hmac(
            'sha256',
            base_string.encode('utf-8'),
            salt,
            100000,
            key_length
        )
        return key.hex()

    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Valida a força da senha"""
        if len(password) < 8:
            return False, "A senha deve ter pelo menos 8 caracteres"
        
        if not any(c.isupper() for c in password):
            return False, "A senha deve ter pelo menos uma letra maiúscula"
            
        if not any(c.islower() for c in password):
            return False, "A senha deve ter pelo menos uma letra minúscula"
            
        if not any(c.isdigit() for c in password):
            return False, "A senha deve ter pelo menos um número"
            
        return True, "Senha forte"

# Instância global
security = SecurityManager()