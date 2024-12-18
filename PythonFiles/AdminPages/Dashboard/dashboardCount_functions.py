from Classes.database import HostConfig, ConfigPaths, ConnectParam

def total_application_count(year):
    """
    This function returns the total number of applications for a given year.
    :param year: Year for which the total count is required.
    :return: Total application count as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = "SELECT COUNT(*) FROM application_page WHERE phd_registration_year=%s"
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def completed_applications(year):
    """
    This function returns the count of completed applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of completed applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """SELECT COUNT(*) 
               FROM application_page 
               WHERE form_filled = 1 AND phd_registration_year = %s"""
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def incomplete_applications(year):
    """
    This function returns the count of incomplete applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of incomplete applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """SELECT COUNT(*) 
               FROM application_page 
               WHERE form_filled = 0 AND phd_registration_year = %s"""
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def accepted_applications(year):
    """
    This function returns the count of accepted applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of accepted applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """SELECT COUNT(*) 
               FROM application_page 
               WHERE final_approval = 'accepted' AND phd_registration_year = %s"""
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def rejected_applications(year):
    """
    This function returns the count of rejected applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of rejected applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """
               SELECT COUNT(*) 
               FROM application_page 
               WHERE phd_registration_year = %s  
               AND final_approval = 'rejected' 
               OR scrutiny_status = 'rejected' 
               OR status = 'rejected'
            """
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def male_applications(year):
    """
    This function returns the count of rejected applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of rejected applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """
               SELECT COUNT(*) 
               FROM application_page 
               WHERE phd_registration_year = %s  
               AND gender = 'Male'
            """
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def female_applications(year):
    """
    This function returns the count of rejected applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of rejected applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """
               SELECT COUNT(*) 
               FROM application_page 
               WHERE phd_registration_year = %s  
               AND gender = 'Female'
            """
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0



