import hashlib
# Data to hash
data = "Network security with SHA-256"
# Encode to bytes
data_bytes = data.encode('utf-8')
# Create SHA-256 hash object
hash_object = hashlib.sha256()
hash_object.update(data_bytes)
# Get hexadecimal digest
hash_hex = hash_object.hexdigest()
print("SHA-256 Digest:", hash_hex)