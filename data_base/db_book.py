import sqlite3


class BookDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def review_exists(self, user_id):
        try:
            result = self.sql.execute("SELECT `id` FROM `book` WHERE `user_id` = ?", (user_id,))
            return bool(len(result.fetchall()))
        except Exception as s:
            print(s, "user_exists")

    def add_review(self, user_id, text, status):
        try:
            self.sql.execute("INSERT INTO `book` (`user_id`, `review`, `status`) VALUES (?, ?, ?)", (user_id, text, status,))
        except Exception as e:
            print(e, "add_review")
        return self.db.commit()

    def get_reviews(self):
        try:
            result = self.sql.execute("SELECT `user_id` FROM `book`")
            return result.fetchall()
        except Exception as s:
            print(type(s))

    def get_reviews_by_status(self, status):
        try:
            result = self.sql.execute("SELECT `user_id` FROM `book` WHERE status = ?", (status,))
            return result.fetchall()
        except Exception as s:
            print(type(s))

    def delete_review(self, user_id):
        try:
            self.sql.execute("DELETE FROM book WHERE user_id = ?", (user_id,))
        except Exception as e:
            pass
        return self.db.commit()

    def delete_all_reviews(self):
        user_list = self.get_reviews()
        print(user_list)
        try:
            for i in user_list:
                self.delete_review(i[0])
        except Exception as e:
            print(e)
        return self.db.commit()

    def get_review(self, user_id):
        try:
            result = self.sql.execute("SELECT review FROM book WHERE user_id = ?", (user_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_review")

    def edit_review(self, user_id, new_review):
        try:
            self.sql.execute("UPDATE `book` SET review = ? WHERE user_id = ?", (new_review, user_id))
        except Exception as e:
            print(e, "edit_review")
        return self.db.commit()

    def set_status(self, user_id, status):
        try:
            self.sql.execute("UPDATE `book` SET status = ? WHERE user_id = ?", (status, user_id))
        except Exception as e:
            print(e, "set_status")
        return self.db.commit()

    def get_status(self, user_id):
        try:
            result = self.sql.execute("SELECT status FROM book WHERE user_id = ?", (user_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_status")


