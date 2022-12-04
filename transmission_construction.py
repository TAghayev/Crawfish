import rsa
import ecdsa
import pickle

enc_standard = 'utf8'
def generate_keys() :
    (pub, priv) = rsa.newkeys(2048)
    sign = ecdsa.SigningKey.generate()
    verif = sign.verifying_key
    return pub, priv, sign, verif

def encrypt_message(public_key, message) :
    enc_msg = message.encode(enc_standard)
    encrypted_message = rsa.encrypt(enc_msg, public_key)
    return encrypted_message

def decrypt_message(private_key, cryptid) :
    decrypted_message = rsa.decrypt(cryptid, private_key)
    orig_message = decrypted_message.decode(enc_standard)
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

def construct_transmission(message, target_id, target_pubkey, signing_key) :
    # take in message, target_id, target_pk, and signing_key
    # encrypt the message, sign it, and send it all in an encoded tuple.

    encrypted_message = encrypt_message(target_pubkey, message)
    signature = sign_message(signing_key, encrypted_message, target_id)
    transmission = pickle.dumps((target_id, encrypted_message, signature))
    return transmission

def deconstruct_transmission(transmission, private_key, keys) :
    # take in encoded tuple, rip it apart
    # verify the message and decrypt the message.
    target_id, encrypted_message, signature, origin_id = pickle.loads(transmission)
    nick, _, verification_key = keys[origin_id]
    decrypted_message = decrypt_message(private_key, encrypted_message)
    message_verified = verify_signature(verification_key, encrypted_message, target_id, signature)
    if not message_verified :
        print("MALFORMED MESSAGE DETECTED")
    return decrypted_message, nick

def server_pass_mod(transmission, origin_id) :
    target_id, encrypted_message, signature = pickle.loads(transmission)
    mod_tr = pickle.dumps((target_id, encrypted_message, signature, origin_id))
    print(target_id, mod_tr)
    return target_id, mod_tr

if __name__ == "__main__" :
    secret_message = "This is a secret!"
    target_id = 8081337
    origin_id = 1010101

    print(secret_message)

    #THESE WOULD BE GENERATED INDEPENDANTLY!!! but, im doing this to save time.
    bob_pub, bob_priv, alice_sign, alice_verif = generate_keys()

    # alice creating a transmission to send
    transmission = construct_transmission(secret_message, target_id, bob_pub, alice_sign)
    print(transmission)

    # this is what a hacker is able to decode from the transmission
    print(pickle.loads(transmission))
    
    # server finds the target_id, to determine the message is meant for bob
    target_id = server_pass_mod(transmission, origin_id)
    print(target_id)

    # bob after recieving transmission
    recieved_message = deconstruct_transmission(transmission, bob_priv, alice_verif)
    print(recieved_message)


    # # rsa encryption, decryption
    # secret_encrypted = encrypt_message(bob_pub, secret_message)
    # secret_decrypted = decrypt_message(bob_priv, secret_encrypted)

    # # ecdsa signature creation, verification
    # secret_signature = sign_message(bob_sign, secret_encrypted, target_id)
    # secret_verified  = verify_signature(bob_verif, secret_encrypted, target_id, secret_signature)

    # # print all results
    # print(secret_message)
    # print(secret_encrypted)
    # print(secret_signature)
    # print(secret_verified)
    # print(secret_decrypted)
