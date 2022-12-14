import sqlite3


class RequestDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def request_exists(self, request_id):
        try:
            result = self.sql.execute("SELECT `id` FROM `requests` WHERE `request_id` = ?", (request_id,))
            return bool(len(result.fetchall()))
        except Exception as s:
            print(s, "request_exists")

    def user_exists(self, user_id):
        try:
            result = self.sql.execute("SELECT `id` FROM `requests` WHERE `user_id` = ?", (user_id,))
            return bool(len(result.fetchall()))
        except Exception as s:
            print(s, "user_exists")

    def add_request(self, request_id, user_id, name):
        try:
            self.sql.execute("INSERT INTO `requests` (`request_id`, `user_id`, `name`) VALUES (?, ?, ?)", (request_id, user_id, name))
        except Exception as e:
            print(e, "add_request")
        return self.db.commit()

    def get_requests(self):
        try:
            result = self.sql.execute("SELECT `request_id` FROM `requests`")
            return result.fetchall()
        except Exception as s:
            print(type(s))

    def delete_request(self, request_id):
        try:
            self.sql.execute("DELETE FROM requests WHERE request_id = ?", (request_id,))
        except Exception as e:
            pass
        return self.db.commit()

    def delete_all(self):
        request_list = self.get_requests()
        print(request_list)
        try:
            for i in request_list:
                self.delete_request(i[0])
        except Exception as e:
            print(e)
        return self.db.commit()

    def set_user_id(self, request_id, user_id):
        try:
            self.sql.execute("UPDATE `requests` SET user_id = ? WHERE request_id = ?", (user_id, request_id))
        except Exception as e:
            print(e, "set_user_id")
        return self.db.commit()

    def get_user_id(self, request_id):
        try:
            result = self.sql.execute("SELECT user_id FROM requests WHERE request_id = ?", (request_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_user_id")

    def set_name(self, request_id, name):
        try:
            self.sql.execute("UPDATE `requests` SET name = ? WHERE request_id = ?", (name, request_id))
        except Exception as e:
            print(e, "name")
        return self.db.commit()

    def get_name(self, request_id):
        try:
            result = self.sql.execute("SELECT name FROM requests WHERE user_id = ?", (request_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_name")

