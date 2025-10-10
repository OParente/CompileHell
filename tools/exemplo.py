# exemplo.py
from autenticat import auth, XORCipher

# Criar usuário
user = auth.create_user(
    username="joao",
    email="joao@email.com", 
    password="SenhaForte123!"
)

print(f"Usuário criado: {user.username}")

# Autenticar
result = auth.authenticate("joao", "SenhaForte123!")

if result.success:
    print("✅ Login bem-sucedido!")
    print(f"Token: {result.token[:50]}...")
    print(f"Chave XOR: {result.xor_key}")
    
    # Testar criptografia
    texto = "Meus segredos importantes!"
    print(f"Texto original: {texto}")
    
    # Criptografar
    encrypted = XORCipher.encrypt(texto.encode('utf-8'), result.xor_key)
    print(f"Texto criptografado: {encrypted.hex()[:50]}...")
    
    # Descriptografar
    decrypted = XORCipher.decrypt(encrypted, result.xor_key)
    print(f"Texto descriptografado: {decrypted.decode('utf-8')}")
    
    # Verificar se é a mesma chave
    mesma_chave = auth.get_xor_key(result.user)
    print(f"Chaves são iguais: {result.xor_key == mesma_chave}")
else:
    print(f"❌ Erro: {result.message}")