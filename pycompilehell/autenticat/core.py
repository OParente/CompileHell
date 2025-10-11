# autenticat/core.py
import secrets
import hashlib
import hmac
import json
import base64
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional

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

class PasswordHasher:
    """Implementação segura de hash de senhas sem bcrypt"""
    
    @staticmethod
    def hash_password(password: str, pepper: str = "", rounds: int = 100000) -> str:
        """Hash seguro de senha usando PBKDF2"""
        salt = secrets.token_bytes(16)
        password_peppered = password + pepper
        
        # Deriva a chave usando PBKDF2
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password_peppered.encode('utf-8'),
            salt,
            rounds,
            32  # 32 bytes = 256 bits
        )
        
        # Combina salt + hash em uma string
        return base64.b64encode(salt + hashed).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str, pepper: str = "") -> bool:
        """Verifica se a senha corresponde ao hash"""
        try:
            # Decodifica a string base64
            decoded = base64.b64decode(hashed_password.encode('utf-8'))
            
            # Extrai salt (primeiros 16 bytes) e hash (restante)
            salt = decoded[:16]
            original_hash = decoded[16:]
            
            password_peppered = password + pepper
            
            # Calcula o hash da senha fornecida
            test_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password_peppered.encode('utf-8'),
                salt,
                100000,
                32
            )
            
            # Comparação segura contra timing attacks
            return hmac.compare_digest(original_hash, test_hash)
            
        except Exception:
            return False

class SimpleJWT:
    """Implementação simples de JWT sem dependências externas"""
    
    @staticmethod
    def encode(payload: dict, secret: str) -> str:
        """Codifica payload em JWT simples"""
        header = {"alg": "HS256", "typ": "JWT"}
        
        # Codificar header e payload em base64url
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        
        # Criar assinatura HMAC
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
            
            # Decodificar payload (adicionar padding se necessário)
            padding = 4 - len(payload_b64) % 4
            if padding != 4:
                payload_b64 += '=' * padding
                
            payload_json = base64.urlsafe_b64decode(payload_b64)
            payload = json.loads(payload_json)
            
            # Verificar expiração
            if 'exp' in payload:
                exp_timestamp = payload['exp']
                current_timestamp = datetime.utcnow().timestamp()
                if current_timestamp > exp_timestamp:
                    return None
                
            return payload
            
        except Exception:
            return None

class Autenticat:
    def __init__(self, secret_key: str = None, pepper: str = None, token_expiry: int = 3600):
        """
        Sistema de autenticação sem dependências externas
        
        Args:
            secret_key: Chave secreta para JWT
            pepper: Pepper adicional para senhas
            token_expiry: Tempo de expiração do token em segundos
        """
        self.secret_key = secret_key or "chave_secreta_padrao_mude_em_producao"
        self.pepper = pepper or "pimenta_padrao_mude_em_producao"
        self.token_expiry = token_expiry
        self.users_db = {}
        self.hasher = PasswordHasher()
        self.jwt = SimpleJWT()
        
    def create_user(self, username: str, email: str, password: str, user_id: str = None) -> User:
        """Cria um novo usuário"""
        if user_id is None:
            user_id = secrets.token_urlsafe(16)
            
        hashed_password = self.hasher.hash_password(password, self.pepper)
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
        """Autentica usuário"""
        user = self.users_db.get(identifier)
        
        if not user or not user.is_active:
            return AuthResult(success=False, message="Usuário não encontrado ou inativo")
        
        if not self.hasher.verify_password(password, user.hashed_password, self.pepper):
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
        """Verifica token JWT e retorna usuário"""
        payload = self.jwt.decode(token, self.secret_key)
        if not payload:
            return None
            
        user_id = payload.get('sub')
        return self.users_db.get(user_id)
    
    def refresh_token(self, refresh_token: str) -> Optional[AuthResult]:
        """Renova token usando refresh token"""
        user = self.verify_token(refresh_token)
        if not user:
            return None
            
        new_token = self._create_jwt_token(user)
        xor_key = self._generate_xor_key(user)
        
        return AuthResult(
            success=True,
            user=user,
            token=new_token,
            refresh_token=refresh_token,
            xor_key=xor_key
        )
    
    def _create_jwt_token(self, user: User) -> str:
        """Cria token JWT"""
        payload = {
            'sub': user.id,
            'username': user.username,
            'email': user.email,
            'exp': (datetime.utcnow() + timedelta(seconds=self.token_expiry)).timestamp(),
            'iat': datetime.utcnow().timestamp()
        }
        return self.jwt.encode(payload, self.secret_key)
    
    def _create_refresh_token(self, user: User) -> str:
        """Cria refresh token"""
        payload = {
            'sub': user.id,
            'type': 'refresh',
            'exp': (datetime.utcnow() + timedelta(days=30)).timestamp(),
            'iat': datetime.utcnow().timestamp()
        }
        return self.jwt.encode(payload, self.secret_key)
    
    def _generate_xor_key(self, user: User, key_length: int = 32) -> str:
        """Gera chave XOR única e reproduzível"""
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
        """Recupera a mesma chave XOR para um usuário"""
        return self._generate_xor_key(user, key_length)

# Instância global para uso fácil
auth = Autenticat()