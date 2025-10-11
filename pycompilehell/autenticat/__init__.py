# autenticat/__init__.py
from .core import Autenticat, auth, User, AuthResult
from .utils import XORCipher

__version__ = "3.0.0"
__all__ = ['Autenticat', 'auth', 'User', 'AuthResult', 'XORCipher']