# QuantumShield

QuantumShield is a high-security cryptographic module designed for post-quantum encryption, hybrid encryption, and digital signature verification. It leverages RSA-4096 and AES-256 encryption to protect data against future quantum attacks.

## Features
- **RSA-4096 Asymmetric Encryption**: Protects data using a large key size for quantum resistance.
- **AES-256 Hybrid Encryption**: Uses symmetric AES encryption for efficient data protection.
- **Digital Signature Verification**: Ensures message integrity and authenticity.
- **Secure Key Storage**: Saves and loads keys in PEM format.

## Installation
To use QuantumShield, install the required dependencies:
```bash
pip install cryptography
```

## Usage
### Generate Key Pair
```python
from quantum_shield import QuantumShield

qs = QuantumShield()
private_key, public_key = qs.generate_keypair()
qs.save_keys(private_key, public_key)
```

### Encrypt & Decrypt Data
```python
message = "Confidential Data"
encrypted = qs.encrypt_data(public_key, message)
decrypted = qs.decrypt_data(private_key, encrypted)
assert message == decrypted
```

### Sign & Verify Data
```python
signature = qs.sign_data(private_key, message)
verified = qs.verify_signature(public_key, message, signature)
print("Signature Verified:", verified)
```

### Hybrid Encryption & Decryption
```python
encrypted_package = qs.hybrid_encryption(message, public_key)
decrypted_message = qs.hybrid_decryption(
    encrypted_package["encrypted_data"],
    encrypted_package["encrypted_key"],
    encrypted_package["iv"],
    private_key
)
assert message == decrypted_message
```

## License
MIT License

## Contribution
Feel free to fork, modify, and improve QuantumShield. Contributions are welcome!
