import rsa
import ecdsa

def generate_keys() :
    (pub, priv) = rsa.newkeys(2048)
    sign = ecdsa.SigningKey.generate()
    verif = sign.verifying_key
    return pub, priv, sign, verif

def encrypt_message(public_key, message) :
    enc_msg = message.encode('utf8')
    encrypted_message = rsa.encrypt(enc_msg, public_key)
    return encrypted_message

def decrypt_message(private_key, cryptid) :
    decrypted_message = rsa.decrypt(cryptid, private_key)
    orig_message = decrypted_message.decode('utf8')
    return orig_message

def sign_message(signing_key, encrypted_message, target_id) :
    new_msg = encrypted_message + bytes(target_id)
    sig = signing_key.sign(new_msg)
    return sig

def verify_signature(verification_key, encrypted_message, target_id, signature) :
    new_msg = encrypted_message + bytes(target_id) # + bytes(1) # to show failure
    try :
        verified = verification_key.verify(signature, new_msg)
    except ecdsa.keys.BadSignatureError :
        verified = False
    return verified

def construct_transmission(message, target_id, target_pk, signing_key) :
    return

def deconstruct_transmission(transmission, private_key) :
    return


if __name__ == "__main__" :
    secret_message = "This is a secret!"
    target_id = 8081337

    bob_pub, bob_priv, bob_sign, bob_verif = generate_keys()

    # rsa encryption, decryption
    secret_encrypted = encrypt_message(bob_pub, secret_message)
    secret_decrypted = decrypt_message(bob_priv, secret_encrypted)

    # ecdsa signature creation, verification
    secret_signature = sign_message(bob_sign, secret_encrypted, target_id)
    secret_verified  = verify_signature(bob_verif, secret_encrypted, target_id, secret_signature)

    # print all results
    print(secret_message)
    print(secret_encrypted)
    print(secret_signature)
    print(secret_verified)
    print(secret_decrypted)
