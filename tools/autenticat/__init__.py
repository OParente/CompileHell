# autenticat/__init__.py
from .core import Autenticat, auth, User, AuthResult
from .security import SecurityManager, security
from .utils import XORCipher

__version__ = "2.0.0"
__all__ = [
    'autenticat', 
    'auth', 
    'User', 
    'AuthResult', 
    'SecurityManager', 
    'security', 
    'XORCipher'
]