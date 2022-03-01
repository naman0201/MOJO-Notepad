import os.path
import string
from tkinter import filedialog


class File_Model:
    def __init__(self):
        self.url = ""
        self.key = string.ascii_letters + ''.join([str(x) for x in range(0, 10)])
        self.offset = 5

    def encrypt(self, plaintext):
        result = ""
        for x in plaintext:
            index = self.key.find(x)
            if (index == -1):
                result += x
            else:
                new_index = (index + self.offset) % len(self.key)
                result += self.key[new_index]
        return result

    def decrypt(self, ciphertext):
        result = ""
        for x in ciphertext:
            index = self.key.find(x)
            if (index == -1):
                result += x
            else:
                new_index = (index - self.offset) % len(self.key)
                result += self.key[new_index]
        return result

    def open_file(self):
        self.url = filedialog.askopenfilename(title="Select File", filetypes=[("Text Documents", "*.*")])

    def new_file(self):
        self.url = ""

    def save_as(self, msg):
        msg = self.encrypt(msg)
        if self.url is None:
            return
        self.url = filedialog.asksaveasfile(mode="w", title="Save File As",
                                            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        self.url.write(msg)
        filepath = self.url.name
        self.url.close()
        self.url = filepath

    def save_file(self, msg):
        if self.url == "":
            self.url = filedialog.asksaveasfilename(title="Select File name",
                                                    filetypes=[("Text Documents", "*.txt")],
                                                    defaultextension=[("Encrypted Files", "*.ntxt")])
        file_name, file_ext = os.path.splitext(self.url)
        if file_ext == ".ntxt":
            msg = self.encrypt(msg)
        with open(self.url, "wb") as fw:
            fw.write(msg.encode("UTF-8"))

    def read_file(self, url=''):
        if url != "":
            self.url = url
        else:
            self.open_file()
        basename = os.path.basename(self.url)
        file_name, file_ext = os.path.splitext(basename)
        fr = open(self.url, "r")
        contents = fr.read()
        if file_ext == ".ntxt":
            contents = self.decrypt(contents)
        fr.close()
        return contents, basename
