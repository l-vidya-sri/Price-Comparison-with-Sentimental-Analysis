# Importing the hashlib library
import hashlib
data = 'sajid24x4@gmail.com'
hash_value = hashlib.md5(data.encode()).hexdigest()
print(hash_value)