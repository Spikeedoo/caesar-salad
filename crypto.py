import subprocess

# Class that calls OpenSSL commands to generate the Diffie-Hellman exchange components
class CryptoManager:
    def __init__(self):
        pass

    SHARED_BASE = "keys/dhp.pem"
    PUBLIC_KEY = "keys/dhpub.pem"
    PRIVATE_KEY = "keys/dhpriv.pem"
    SHARED_SECRET = "keys/shared.bin"

    # Generators #
    def generate_shared_base(self):
        args = ['openssl', 'genpkey', '-genparam', '-algorithm', 'DH', '-out', self.SHARED_BASE]
        subprocess.call(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def generate_private_key(self):
        args = ['openssl', 'genpkey', '-paramfile', self.SHARED_BASE, '-out', self.PRIVATE_KEY]
        subprocess.call(args)

    def generate_public_key(self):
        args = ['openssl', 'pkey', '-in', self.PRIVATE_KEY, '-pubout', '-out', self.PUBLIC_KEY]
        subprocess.call(args)

    def derive_shared_secret(self):
        args = ['openssl', 'pkeyutl', '-derive', '-inkey', self.PRIVATE_KEY, '-peerkey', 'keys/peer.pem', '-out', self.SHARED_SECRET]
        subprocess.call(args)

    # Encrypt/Decrypt #
    # def encrypt_message(self, msg):
    #     args = ['echo', '-n', msg, '|', 'openssl', 'enc', '-aes-256-cbc', '-pass', 'file:./keys/shared.bin']
    #     subprocess.call(args, stdout=subprocess.PIPE)


    # Readers #
    def read_key(self, type_file):
        key = ""
        try:
            with open(type_file) as f:
                lines = f.readlines()
                for l in lines:
                    # If line is the start or end marker- keep going
                    l.rstrip("\n")
                    if l[0:5] == "-----":
                        continue
                    # If it is not marker--add it to the key
                    else:
                        key += l
            return key.strip().lstrip('\n')
        except FileNotFoundError:
            print("ERROR! Your key file type is not valid!")
