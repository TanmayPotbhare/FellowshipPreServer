import mysql.connector


class HostConfig:
    hostserver = '43.240.64.151'
    localserver = '127.0.0.1'
    host = localserver


class ConnectParam:
    def __init__(self, host):
        self.host = host

    def connect(self, use_dict=False):
        cnx = mysql.connector.connect(
            user='root',
            password='A9CALcsd7lc%7ac',
            host=self.host,
            database='ICSApplication'
        )
        cursor = cnx.cursor(dictionary=use_dict)
        return cnx, cursor


class ConfigPaths:
    paths = {
        HostConfig.localserver: {
            'USER_DOC_SEC_FIVE': '/var/www/fellowship/fellowship/FellowshipPreServer/static/uploads/user_doc_secfive/',
            'RENT_AGREEMENT_REPORT': '/var/www/fellowship/fellowship/FellowshipPreServer/static/uploads/rent_agreement/',
            'HALF_YEARLY_REPORTS': '/var/www/fellowship/fellowship/FellowshipPreServer/static/uploads/half_yearly/',
            'PRESENTY_REPORTS': '/var/www/fellowship/fellowship/FellowshipPreServer/static/uploads/presenty_reports/',
            'UPLOAD_PHOTO_SECTION1': '/var/www/fellowship/fellowship/FellowshipPreServer/static/uploads/image_retrive/',
            'PDF_STORAGE_PATH': '/var/www/fellowship/fellowship/FellowshipPreServer/static/pdf_application_form/pdfform.pdf',
            'AWARD_LETTER': '/var/www/fellowship/fellowship/FellowshipPreServer/static/pdf_application_form/award_letter.pdf',
            'JOINING_REPORT': '/var/www/fellowship/fellowship/FellowshipPreServer/static/uploads/joining_reports/',
            'PDF_CERTIFICATE': '/var/www/fellowship/fellowship/FellowshipPreServer/static/uploads/phd_certificate/',
            'UPLOAD_THESIS': '/var/www/fellowship/fellowship/FellowshipPreServer/static/uploads/upload_thesis/',
            'EMAIL_DOCS': '/var/www/fellowship/fellowship/FellowshipPreServer/static/uploads/sendbulkemails/',
            'ASSESSMENT_REPORT': '/var/www/fellowship/fellowship/FellowshipPreServer/static/uploads/assessment_report/',
            'UNDERTAKING_REPORT': '/var/www/fellowship/fellowship/FellowshipPreServer/static/uploads/undertaking_doc/',
            # Add other paths here
        },
        HostConfig.hostserver: {
            'USER_DOC_SEC_FIVE': 'static/uploads/user_doc_secfive/',
            'RENT_AGREEMENT_REPORT': 'static/uploads/rent_agreement/',
            'HALF_YEARLY_REPORTS': 'static/uploads/half_yearly/',
            'PRESENTY_REPORTS': 'static/uploads/presenty_reports/',
            'UPLOAD_PHOTO_SECTION1': 'static/uploads/image_retrive/',
            'PDF_STORAGE_PATH': 'static/pdf_application_form/pdfform.pdf',
            'AWARD_LETTER': 'static/pdf_application_form/award_letter.pdf',
            'JOINING_REPORT': 'static/uploads/joining_reports/',
            'PDF_CERTIFICATE': 'static/uploads/phd_certificate/',
            'UPLOAD_THESIS': 'static/uploads/upload_thesis/',
            'EMAIL_DOCS': 'static/uploads/sendbulkemails/',
            'ASSESSMENT_REPORT': 'static/uploads/assessment_report/',
            'UNDERTAKING_REPORT': 'static/uploads/undertaking_doc/',
            # Add other paths here
        }
    }


class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor

    def fetch_all(self, cursor):
        return cursor.fetchall()

    def fetch_one(self, cursor):
        return cursor.fetchone()
