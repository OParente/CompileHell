# autenticat_sem_jwt.py
import bcrypt
import secrets
import hashlib
import json
import base64
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional
import hmac

@dataclass
class User:
    id: str
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_verified: bool = False

@dataclass
class AuthResult:
    success: bool
    user: Optional[User] = None
    token: Optional[str] = None
    refresh_token: Optional[str] = None
    xor_key: Optional[str] = None
    message: str = ""

class SimpleJWT:
    """Implementação simples de JWT sem dependências externas"""
    
    @staticmethod
    def encode(payload: dict, secret: str) -> str:
        """Codifica payload em JWT simples"""
        header = {"alg": "HS256", "typ": "JWT"}
        
        # Codificar header e payload
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        
        # Criar assinatura
        message = f"{header_b64}.{payload_b64}"
        signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
        
        return f"{header_b64}.{payload_b64}.{signature_b64}"
    
    @staticmethod
    def decode(token: str, secret: str) -> Optional[dict]:
        """Decodifica e verifica JWT"""
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None
                
            header_b64, payload_b64, signature_b64 = parts
            
            # Verificar assinatura
            message = f"{header_b64}.{payload_b64}"
            expected_signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
            expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode().rstrip('=')
            
            if not hmac.compare_digest(signature_b64, expected_signature_b64):
                return None
            
            # Decodificar payload
            payload_json = base64.urlsafe_b64decode(payload_b64 + '=' * (4 - len(payload_b64) % 4))
            payload = json.loads(payload_json)
            
            # Verificar expiração
            if 'exp' in payload and datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
                return None
                
            return payload
            
        except Exception:
            return None

class AutenticatSimples:
    def __init__(self, secret_key: str = None, pepper: str = None, token_expiry: int = 3600):
        self.secret_key = secret_key or "chave_secreta_padrao_mude_em_producao"
        self.pepper = pepper or "pimenta_padrao_mude_em_producao"
        self.token_expiry = token_expiry
        self.users_db = {}
        self.jwt = SimpleJWT()
        
    def create_user(self, username: str, email: str, password: str, user_id: str = None) -> User:
        if user_id is None:
            user_id = secrets.token_urlsafe(16)
            
        hashed_password = self._hash_password(password)
        user = User(
            id=user_id,
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        
        self.users_db[user_id] = user
        self.users_db[username] = user
        self.users_db[email] = user
        
        return user
    
    def authenticate(self, identifier: str, password: str) -> AuthResult:
        user = self.users_db.get(identifier)
        
        if not user or not user.is_active:
            return AuthResult(success=False, message="Usuário não encontrado ou inativo")
        
        if not self._verify_password(password, user.hashed_password):
            return AuthResult(success=False, message="Senha incorreta")
        
        # Gerar tokens
        token = self._create_jwt_token(user)
        refresh_token = self._create_refresh_token(user)
        xor_key = self._generate_xor_key(user)
        
        return AuthResult(
            success=True,
            user=user,
            token=token,
            refresh_token=refresh_token,
            xor_key=xor_key,
            message="Autenticação bem-sucedida"
        )
    
    def verify_token(self, token: str) -> Optional[User]:
        payload = self.jwt.decode(token, self.secret_key)
        if not payload:
            return None
            
        user_id = payload.get('sub')
        return self.users_db.get(user_id)
    
    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt(rounds=12)
        peppered_password = password + self.pepper
        return bcrypt.hashpw(peppered_password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        try:
            peppered_password = password + self.pepper
            return bcrypt.checkpw(peppered_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False
    
    def _create_jwt_token(self, user: User) -> str:
        payload = {
            'sub': user.id,
            'username': user.username,
            'email': user.email,
            'exp': (datetime.utcnow() + timedelta(seconds=self.token_expiry)).timestamp(),
            'iat': datetime.utcnow().timestamp()
        }
        return self.jwt.encode(payload, self.secret_key)
    
    def _create_refresh_token(self, user: User) -> str:
        payload = {
            'sub': user.id,
            'type': 'refresh',
            'exp': (datetime.utcnow() + timedelta(days=30)).timestamp(),
            'iat': datetime.utcnow().timestamp()
        }
        return self.jwt.encode(payload, self.secret_key)
    
    def _generate_xor_key(self, user: User, key_length: int = 32) -> str:
        base_string = f"{user.id}{user.username}{self.secret_key}"
        salt = user.id.encode('utf-8')
        key = hashlib.pbkdf2_hmac(
            'sha256',
            base_string.encode('utf-8'),
            salt,
            100000,
            key_length
        )
        return key.hex()
    
    def get_xor_key(self, user: User, key_length: int = 32) -> str:
        return self._generate_xor_key(user, key_length)

class XORCipher:
    @staticmethod
    def encrypt(data: bytes, xor_key: str) -> bytes:
        key_bytes = bytes.fromhex(xor_key)
        key_length = len(key_bytes)
        encrypted = bytearray()
        
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key_bytes[i % key_length])
            
        return bytes(encrypted)
    
    @staticmethod
    def decrypt(encrypted_data: bytes, xor_key: str) -> bytes:
        return XORCipher.encrypt(encrypted_data, xor_key)
    
    @staticmethod
    def encrypt_file(input_path: str, output_path: str, xor_key: str, chunk_size: int = 8192):
        with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                encrypted_chunk = XORCipher.encrypt(chunk, xor_key)
                f_out.write(encrypted_chunk)
    
    @staticmethod
    def decrypt_file(input_path: str, output_path: str, xor_key: str, chunk_size: int = 8192):
        XORCipher.encrypt_file(input_path, output_path, xor_key, chunk_size)

# Instância global
auth = AutenticatSimples()