# exemplo.py
from autenticat import auth, XORCipher

print("🚀 AUTENTICAT")
print("=" * 50)

# Criar usuário
try:
    user = auth.create_user(
        username="davi",
        email="davi@email.com",
        password="MinhaSenhaSuperSegura123!"
    )
    print(f"✅ Usuário criado: {user.username}")
    print(f"📧 Email: {user.email}")
    print(f"🆔 ID: {user.id}")
except Exception as e:
    print(f"❌ Erro ao criar usuário: {e}")

# Autenticar
print("\n🔐 TENTATIVA DE LOGIN")
result = auth.authenticate("davi", "MinhaSenhaSuperSegura123!")

if result.success:
    print("✅ Login bem-sucedido!")
    print(f"👤 Usuário: {result.user.username}")
    print(f"🔑 Token: {result.token}")
    print(f"🔄 Refresh Token: {result.refresh_token}")
    print(f"🔐 Chave XOR: {result.xor_key}")
    
    # Testar criptografia
    print("\n🔒 TESTE DE CRIPTOGRAFIA")
    mensagem_secreta = "Esta mensagem é ultra secreta e importante!"
    
    print(f"📝 Mensagem original: {mensagem_secreta}")
    
    # Criptografar
    encrypted = XORCipher.encrypt(mensagem_secreta.encode('utf-8'), result.xor_key)
    print(f"🔒 Mensagem criptografada (hex): {encrypted.hex()}")
    
    # Descriptografar
    decrypted = XORCipher.decrypt(encrypted, result.xor_key)
    print(f"🔓 Mensagem descriptografada: {decrypted.decode('utf-8')}")
    
    # Verificar se a chave é sempre a mesma
    print("\n🔑 VERIFICAÇÃO DA CHAVE")
    mesma_chave = auth.get_xor_key(result.user)
    print(f"Chave original: {result.xor_key}")
    print(f"Chave recuperada: {mesma_chave}")
    print(f"✅ Chaves são iguais: {result.xor_key == mesma_chave}")
    
    # Testar verificação de token
    print("\n🎫 VERIFICAÇÃO DO TOKEN")
    user_verificado = auth.verify_token(result.token)
    if user_verificado:
        print(f"✅ Token válido! Usuário: {user_verificado.username}")
    else:
        print("❌ Token inválido!")
        
else:
    print(f"❌ Falha na autenticação: {result.message}")

# Teste com senha errada
print("\nTESTE COM SENHA")
result_errado = auth.authenticate("davi", "MinhaSenhaSuperSegura123!")
print(f"Resultado: {'✅' if result_errado.success else '❌'} {result_errado.message}")

print("\n" + "=" * 50)
print("🎉 SISTEMA PRONTO PARA USO!")