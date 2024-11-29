from PIL import Image
import numpy as np
from imetadata.utils import (
    extract_metadata, aes_encrypt, rsa_encrypt, embed_metadata_second_lsb, apply_dct, generate_rsa_keys
)

from imetadata.utils import (
    rsa_decrypt, apply_inverse_dct, extract_metadata_second_lsb, aes_decrypt
)


def encrypt_image(image_path):
    # Step 1: Extract Metadata
    metadata = extract_metadata(image_path)
    
    # Step 2: Calculate Modularity (block size placeholder)
    block_size = len(metadata) % 16 or 16  # Placeholder logic

    # Step 3: AES Key Generation and Encryption
    encrypted_metadata, aes_key, aes_iv = aes_encrypt(metadata)

    # Step 4: RSA Key Generation and Encryption
    public_key, private_key = generate_rsa_keys()
    encrypted_aes_key = rsa_encrypt(aes_key, public_key)

    # Step 5: Embed Metadata into Second LSB
    image = Image.open(image_path)
    image_array = np.array(image)
    stego_array = embed_metadata_second_lsb(image_array, encrypted_metadata)

    # Step 6: Apply DCT for Compression
    compressed_array = apply_dct(stego_array)

    # Step 7: Encrypt Stego Image with RSA
    encrypted_stego = rsa_encrypt(compressed_array.tobytes(), public_key)

    return {
        "encrypted_image": encrypted_stego,
        "public_key": public_key,
        "private_key": private_key,
        "aes_iv": aes_iv
    }


def decrypt_image(encrypted_image, private_key, aes_iv, metadata_length):
    # Step 1: RSA Decrypt Stego Image
    compressed_array = rsa_decrypt(encrypted_image, private_key)
    stego_array = np.frombuffer(compressed_array, dtype=np.uint8)

    # Step 2: Apply Inverse DCT
    restored_array = apply_inverse_dct(stego_array)

    # Step 3: Extract Metadata from Second LSB
    encrypted_metadata = extract_metadata_second_lsb(restored_array, metadata_length)

    # Step 4: Decrypt Metadata with AES
    metadata = aes_decrypt(encrypted_metadata, private_key, aes_iv)

    return metadata
