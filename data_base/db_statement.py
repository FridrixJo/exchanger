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

    def set_open_bank(self, open_bank, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET open_bank = ? WHERE id = ?", (open_bank, id))
        except Exception as e:
            print(e, "set_open_bank")
        return self.db.commit()

    def get_open_bank(self, id=1):
        try:
            result = self.sql.execute("SELECT open_bank FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_open_bank")

    def set_qiwi(self, qiwi, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET qiwi = ? WHERE id = ?", (qiwi, id))
        except Exception as e:
            print(e, "set_qiwi")
        return self.db.commit()

    def get_qiwi(self, id=1):
        try:
            result = self.sql.execute("SELECT qiwi FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_qiwi")

    def set_btc_address(self, btc_address, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET btc_address = ? WHERE id = ?", (btc_address, id))
        except Exception as e:
            print(e, "set_btc_address")
        return self.db.commit()

    def get_btc_address(self, id=1):
        try:
            result = self.sql.execute("SELECT btc_address FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_btc_address")

    def set_eth_address(self, eth_address, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET eth_address = ? WHERE id = ?", (eth_address, id))
        except Exception as e:
            print(e, "set_eth_address")
        return self.db.commit()

    def get_eth_address(self, id=1):
        try:
            result = self.sql.execute("SELECT eth_address FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_eth_address")

    def set_ltc_address(self, ltc_address, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET ltc_address = ? WHERE id = ?", (ltc_address, id))
        except Exception as e:
            print(e, "set_ltc_address")
        return self.db.commit()

    def get_ltc_address(self, id=1):
        try:
            result = self.sql.execute("SELECT ltc_address FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_ltc_address")

    def set_xmr_address(self, xmr_address, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET xmr_address = ? WHERE id = ?", (xmr_address, id))
        except Exception as e:
            print(e, "set_xmr_address")
        return self.db.commit()

    def get_xmr_address(self, id=1):
        try:
            result = self.sql.execute("SELECT xmr_address FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_xmr_address")
