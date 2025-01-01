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
        self.cursor.execute("""
                SELECT DISTINCT caste, unique_number 
                FROM ICSApplication.caste_subcaste
            """)
        result = self.cursor.fetchall()
        return result

    def get_subcastes_by_unique_number(self, unique_number):
        self.cursor.execute("""
            SELECT subcaste 
            FROM ICSApplication.caste_subcaste 
            WHERE unique_number = %s
        """, (unique_number,))
        result = self.cursor.fetchall()
        return [row['subcaste'] for row in result]

    def get_all_caste_validity_auth(self):
        self.cursor.execute("""
                SELECT *
                FROM ICSApplication.CasteValidityAuthority
            """)
        result = self.cursor.fetchall()
        return result

    def get_taluka_from_district(self, district_id):
        self.cursor.execute("""
            SELECT taluka_name
            FROM ICSApplication.talukas
            WHERE district_id_fk = %s
        """, (district_id,))
        result = self.cursor.fetchall()
        return [row['taluka_name'] for row in result]
