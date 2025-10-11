# setup.py
from setuptools import setup, find_packages

setup(
    name="autenticat",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "bcrypt>=3.2.0",
        "PyJWT>=2.0.0",
        # python-dotenv removido para simplificar
    ],
    python_requires=">=3.7",
    author="Davi Parente da Silva",
    description="Sistema de autenticação modular e seguro com criptografia XOR",
    keywords="authentication security crypto xor",
)