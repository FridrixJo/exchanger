import sqlite3


class StatementDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def set_btc(self, btc, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET btc = ? WHERE id = ?", (btc, id))
        except Exception as e:
            print(e, "set_btc")
        return self.db.commit()

    def set_eth(self, eth, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET eth = ? WHERE id = ?", (eth, id))
        except Exception as e:
            print(e, "set_eth")
        return self.db.commit()

    def set_ltc(self, ltc, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET ltc = ? WHERE id = ?", (ltc, id))
        except Exception as e:
            print(e, "set_ltc")
        return self.db.commit()

    def set_xmr(self, xmr, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET xmr = ? WHERE id = ?", (xmr, id))
        except Exception as e:
            print(e, "set_btc")
        return self.db.commit()

    def get_btc(self, id=1):
        try:
            result = self.sql.execute("SELECT btc FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_btc")

    def get_ltc(self, id=1):
        try:
            result = self.sql.execute("SELECT ltc FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_ltc")

    def get_eth(self, id=1):
        try:
            result = self.sql.execute("SELECT eth FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_eth")

    def get_xmr(self, id=1):
        try:
            result = self.sql.execute("SELECT xmr FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_xmr")

    def set_sber(self, sber, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET sber = ? WHERE id = ?", (sber, id))
        except Exception as e:
            print(e, "set_sber")
        return self.db.commit()

    def get_sber(self, id=1):
        try:
            result = self.sql.execute("SELECT sber FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_sber")

    def set_tinkoff(self, tinkoff, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET tinkoff = ? WHERE id = ?", (tinkoff, id))
        except Exception as e:
            print(e, "set_tinkoff")
        return self.db.commit()

    def get_tinkoff(self, id=1):
        try:
            result = self.sql.execute("SELECT tinkoff FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_tinkoff")
