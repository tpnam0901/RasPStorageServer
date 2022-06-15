import os
import hashlib
from .settings import SERVER_DATA_DIR

class RangeFileWrapper (object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data

class StringEncrypter(object):
    """A simple encryption algorithm that encrypts a string using a key."""
    def __init__(self):
        # Init hash table
        self.key_decrypt= {}
        self.encrypt(SERVER_DATA_DIR)
        self.get_hash_dict(SERVER_DATA_DIR)
    
    def reset_key_decrypt(self):
        self.key_decrypt = {self.encrypt(SERVER_DATA_DIR):SERVER_DATA_DIR}
        self.get_hash_dict(SERVER_DATA_DIR)
        
    def get_hash_dict(self,path):
        sub_elements = self.get_sub_path(path)
        for sub in sub_elements:
            if os.path.isfile(sub):
                self.key_decrypt.update({self.encrypt(sub): sub})
            else:
                self.key_decrypt.update({self.encrypt(sub): sub})
                self.get_hash_dict(sub)
                
    def encrypt(self, string):
        hashed_string = hashlib.sha256(string.encode('utf-8')).hexdigest()
        if string.startswith(SERVER_DATA_DIR):
            self.key_decrypt.update({hashed_string: string})
        return hashed_string

    def decrypt(self, hashed_string):
        return self.key_decrypt.get(hashed_string,SERVER_DATA_DIR)

    def get_sub_path(self, path):
        sub_files = []
        list_files = os.listdir(path)
        for f_name in list_files:
            if ".Trash-1000" == f_name:
                continue
            sub_files.append(os.path.join(path, f_name))
        return sub_files