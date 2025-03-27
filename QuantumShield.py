import hashlib
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode, b64decode

class QuantumShield:
    def __init__(self):
        self.key_size = 4096  # Increased key size for post-quantum resistance

    def generate_keypair(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    def save_keys(self, private_key, public_key, private_path='private.pem', public_path='public.pem'):
        with open(private_path, 'wb') as priv_file:
            priv_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open(public_path, 'wb') as pub_file:
            pub_file.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    
    def encrypt_data(self, public_key, data):
        encrypted = public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return b64encode(encrypted).decode()

    def decrypt_data(self, private_key, encrypted_data):
        decrypted = private_key.decrypt(
            b64decode(encrypted_data),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()
    
    def sign_data(self, private_key, data):
        signature = private_key.sign(
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return b64encode(signature).decode()
    
    def verify_signature(self, public_key, data, signature):
        try:
            public_key.verify(
                b64decode(signature),
                data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    def hybrid_encryption(self, data, recipient_public_key):
        symmetric_key = os.urandom(32)
        iv = os.urandom(16)
        
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padded_data = data + (16 - len(data) % 16) * ' '
        encrypted_data = encryptor.update(padded_data.encode()) + encryptor.finalize()
        
        encrypted_symmetric_key = self.encrypt_data(recipient_public_key, symmetric_key.hex())
        return {
            "iv": b64encode(iv).decode(),
            "encrypted_data": b64encode(encrypted_data).decode(),
            "encrypted_key": encrypted_symmetric_key
        }
    
    def hybrid_decryption(self, encrypted_data, encrypted_key, iv, private_key):
        decrypted_symmetric_key = self.decrypt_data(private_key, encrypted_key)
        
        cipher = Cipher(algorithms.AES(bytes.fromhex(decrypted_symmetric_key)), modes.CBC(b64decode(iv)))
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(b64decode(encrypted_data)) + decryptor.finalize()
        return decrypted_data.strip().decode()

# Example Usage
quantum_shield = QuantumShield()
private_key, public_key = quantum_shield.generate_keypair()
message = "Confidential Data"
encrypted = quantum_shield.encrypt_data(public_key, message)
decrypted = quantum_shield.decrypt_data(private_key, encrypted)
assert message == decrypted
