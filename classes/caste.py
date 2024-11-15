import mysql.connector


class casteController:
    def __init__(self, host):
        self.host = host
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',  # --------  DATABASE CONNECTION
                                      host=self.host,
                                      database='ICSApplication')
        self.cursor = cnx.cursor(dictionary=True)
        self.cnx = cnx
        # self.cnx = cnx
        # self.cursor = cursor

    def get_all_caste_details(self):
        self.cursor.execute("SELECT * from tbl_master_caste")
        result = self.cursor.fetchall()
        return result
