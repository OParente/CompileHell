# autenticat/utils.py
class XORCipher:
    """Utilitário simples para criptografia XOR usando a chave gerada"""
    
    @staticmethod
    def encrypt(data: bytes, xor_key: str) -> bytes:
        """
        Criptografa dados usando XOR
        
        Args:
            data: Dados a serem criptografados
            xor_key: Chave XOR em hexadecimal
            
        Returns:
            Dados criptografados
        """
        key_bytes = bytes.fromhex(xor_key)
        key_length = len(key_bytes)
        encrypted = bytearray()
        
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key_bytes[i % key_length])
            
        return bytes(encrypted)
    
    @staticmethod
    def decrypt(encrypted_data: bytes, xor_key: str) -> bytes:
        """
        Descriptografa dados usando XOR (mesma operação que encrypt)
        
        Args:
            encrypted_data: Dados criptografados
            xor_key: Chave XOR em hexadecimal
            
        Returns:
            Dados descriptografados
        """
        return XORCipher.encrypt(encrypted_data, xor_key)  # XOR é reversível
    
    @staticmethod
    def encrypt_file(input_path: str, output_path: str, xor_key: str, chunk_size: int = 8192):
        """
        Criptografa um arquivo usando XOR
        
        Args:
            input_path: Caminho do arquivo original
            output_path: Caminho do arquivo criptografado
            xor_key: Chave XOR em hexadecimal
            chunk_size: Tamanho do chunk para processamento
        """
        with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                encrypted_chunk = XORCipher.encrypt(chunk, xor_key)
                f_out.write(encrypted_chunk)
    
    @staticmethod
    def decrypt_file(input_path: str, output_path: str, xor_key: str, chunk_size: int = 8192):
        """
        Descriptografa um arquivo usando XOR
        
        Args:
            input_path: Caminho do arquivo criptografado
            output_path: Caminho do arquivo descriptografado
            xor_key: Chave XOR em hexadecimal
            chunk_size: Tamanho do chunk para processamento
        """
        XORCipher.encrypt_file(input_path, output_path, xor_key, chunk_size)  # Mesma operação