from cipher import CaesarSalad

cs = CaesarSalad()

msg = "Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum"
key = "013313ece231ffbd5acf5096b6678c5bbf6ed1de80588c4f04c40a02b95918bd"

enc = cs.cs_encode(msg, key)
print("Encoded: " + enc)
dec = cs.cs_decode(enc, key)
print("Decoded: " + dec)