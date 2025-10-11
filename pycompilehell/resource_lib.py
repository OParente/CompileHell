import base64

# --- Configuração ---
SECRET_KEY = 0x9989  # chave XOR simples (pode mudar)
HEADER = "# RESXX FILE v2\n"

def xor_encrypt(text: str) -> str:
    return ''.join(chr(ord(c) ^ SECRET_KEY) for c in text)


def xor_decrypt(text: str) -> str:
    return ''.join(chr(ord(c) ^ SECRET_KEY) for c in text)


def encode_line(line: str) -> str:
    encrypted = xor_encrypt(line)
    return base64.b64encode(encrypted.encode()).decode()


def decode_line(line: str) -> str:
    decoded = base64.b64decode(line).decode()
    return xor_decrypt(decoded)


def save_resxx(path: str, data: dict):
    """
    Salva um dicionário no formato .resxx
    data = {
        "Section1": {"key1": "val1", "key2": "val2"},
        "Section2": {"x": "10", "y": "20"},
    }
    """
    lines = [HEADER]
    for section, items in data.items():
        lines.append(encode_line(f"Section: {section}"))
        for k, v in items.items():
            lines.append(encode_line(f"{k}={v}"))
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"Arquivo salvo: {path}")


def load_resxx(path: str) -> dict:
    """Carrega e decodifica um arquivo .resxx"""
    data = {}
    section = None
    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            decoded = decode_line(line)
            if decoded.startswith("Section: "):
                section = decoded.split(": ", 1)[1]
                data[section] = {}
            elif "=" in decoded and section:
                k, v = decoded.split("=", 1)
                data[section][k] = v
    return data
