from traceback import *

from cx_Oracle import *


class Db_Model:

    def __init__(self):
        self.file_dict = {}
        self.db_status = True
        self.conn = None
        self.curr = None
        try:
            self.conn = connect("mojo/mojo@127.0.0.1/xe")
            print("Connection opened successfully")
            self.curr = self.conn.cursor()
        except DatabaseError:
            self.db_status = False
            print("DB Error: ", format_exc())

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.curr is not None:
            self.curr.close()
        if self.conn is not None:
            self.conn.close()
        print("Disconnected successfully from DB")

    def add_file(self, file_name, file_path, file_owner, file_pwd):
        self.file_dict[file_name] = (file_path, file_owner, file_pwd)
        print("file added successfully: ", self.file_dict[file_name])

    def get_file_path(self, file_name):
        return self.file_dict.get(file_name)[0]

    def add_file_to_db(self, file_name, file_path, file_owner, file_pwd):
        self.curr.execute("Select max(file_id) from mysecurefiles")
        last_file_id = self.curr.fetchone()[0]
        next_file_id = 1

        if last_file_id is not None:
            next_file_id = last_file_id + 1

        self.curr.execute("insert into mysecurefiles values(:1,:2,:3,:4,:5)",
                          (next_file_id, file_name, file_path, file_owner, file_pwd))
        self.conn.commit()
        return "file sucessfully added to the database"

    def load_files_from_db(self):
        self.curr.execute("select file_name,file_path,file_owner,file_pwd from mysecurefiles")
        record_added = False
        for file_name, file_path, file_owner, file_pwd in self.curr:
            self.file_dict[file_name] = (file_path, file_owner, file_pwd)
            record_added = True
        if record_added == True:
            return "Files populated from the DB"
        else:
            return "No files present in your DB"

    def remove_file_from_db(self, file_name):
        self.curr.execute("delete from mysecurefiles where file_name=:1", (file_name,))
        n = self.curr.rowcount
        if n == 0:
            return "File not present in the DB"
        else:
            self.file_dict.pop(file_name)
            self.conn.commit()
            return "file deleted from DB"

    def is_secure_files(self, file_name):
        return file_name in self.file_dict

    def get_file_pwd(self, file_name):
        return self.file_dict.get(file_name)[2]

    def get_file_count(self):
        return len(self.file_dict)
