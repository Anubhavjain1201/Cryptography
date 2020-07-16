#The required Modules
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad
import os

#Secret key to be shared beforeHand securely
key = b'Q\xcb\xef\xff\x17\xac\x8czfr!O\x94\xa4\xd9\xa2'

#The class to Encrypt the files
class Encryptor:

    #constructor which intializes the key
    def __init__(self, key):
        self.key = key
    

    #Function to Pad the data which is a multiple of the block size
    def pad(self, s):
        padded = pad(s, AES.block_size)
        
        return padded


    #The main function which encrypts the passed data
    def encrypt(self, message, key):
        message = self.pad(message)
        
        cipher = AES.new(key, AES.MODE_CBC)
        
        iv = cipher.iv
        
        cipherInBytes = cipher.encrypt(message)
        
        return iv + cipherInBytes

    #function to encrypt the file
    def encrypt_file(self, file_name):
        
        file = open(file_name, 'rb')
        content = file.read()
        file.close()
        
        cipherBytes = self.encrypt(content, self.key)
        
        file = open(file_name + '.enc', 'wb')
        file.write(cipherBytes)
        file.close()
        
        os.remove(file_name) 
    
    #The main function to decrypt the data
    def decrypt(self, cipherInbytes, key):
        iv = cipherInbytes[:AES.block_size]
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        plaintext = unpad(cipher.decrypt(cipherInbytes[AES.block_size:]), AES.block_size)
        
        return plaintext

    #function to decrypt the file
    def decrypt_file(self, file_name):
        
        file = open(file_name, 'rb')
        cipherinbytes = file.read()
        file.close()

        plaintext = self.decrypt(cipherinbytes, self.key)
        
        file = open(file_name[:-4], 'w')
        file.write(plaintext.decode())
        file.close()
        
        os.remove(file_name)


#Instantiate the Encryptor class
enc = Encryptor(key)

##Comment one of the function(encrypt_file() or decrypt_file()) before using the program

#Input the file name to encrypt
enc.encrypt_file(str(input('file_name: ')))

#Input the file name to decrypt
enc.decrypt_file(str(input('file_name: ')))

