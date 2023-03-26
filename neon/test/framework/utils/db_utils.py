import os

import pyodbc

from naga.test.framework.utils.report_utils import ReportUtils

data = None
cursor = None
db_rows_list = []


class DBUtils:

    cursor: pyodbc.Cursor
    data

    def __connect(servername=None, database=None, username=None, password=None):
        """Connect to SQL server

        Args:
            servername (str, optional): DB servername . Defaults to None.
            database (str, optional): database name. Defaults to None.
            username (str, optional): username. Defaults to None.
            password (str, optional): password. Defaults to None.

        Returns:
            _type_: connection
        """
        servername = os.getenv("database_server") if servername == None else servername
        database = os.getenv("database") if database == None else database
        username = os.getenv("db_uid") if username == None else username
        password = os.getenv("db_pwd") if password == None else password
        conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                              "Server=" + servername + ";"
                              "Database=" + database + ";"
                              "uid=" + username + ";pwd=" + password)
        return conn

    def read(query, servername=None, database=None, username=None, password=None):
        """Execute Select SQL statement

        Args:
            query (str): SQL query string
            servername (str, optional): DB servername . Defaults to None.
            database (str, optional): database name. Defaults to None.
            username (str, optional): username. Defaults to None.
            password (str, optional): password. Defaults to None.

        Raises:
            pyodbc.Error: Any sql based error

        Returns:
            class: DBUtils
        """
        try:
            connect = DBUtils.__connect(servername, database, username, password)
            DBUtils.cursor = connect.cursor()
            DBUtils.data = DBUtils.cursor.execute(query)
            ReportUtils.log("---Executed select query-----")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            ReportUtils.log(f"\n ****Error****: {ex}, State: {sqlstate}", ReportUtils.level_info)
            raise pyodbc.Error
        except Exception as e:
            DBUtils.data = None
            ReportUtils.log(f"SQL exception----Setting data to none \n {e}")

        return DBUtils

    def update(query, servername=None, database=None, username=None, password=None):
        """Execute Update and Insert SQL statement

        Args:
            query (str): SQL query string
            servername (str, optional): DB servername . Defaults to None.
            database (str, optional): database name. Defaults to None.
            username (str, optional): username. Defaults to None.
            password (str, optional): password. Defaults to None.

        Raises:
            pyodbc.Error: Any sql based error

        Returns:
            class: DBUtils
        """
        try:
            connect = DBUtils.__connect(servername, database, username, password)
            DBUtils.cursor = connect.cursor()
            DBUtils.data = DBUtils.cursor.execute(query)
            connect.commit()
            ReportUtils.log("---Executed insert/update query-----")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            ReportUtils.log(f"\n ****Error****: {ex}, State: {sqlstate}", ReportUtils.level_info)
            raise pyodbc.Error
        except Exception as e:
            DBUtils.data = None
            ReportUtils.log(f"SQL exception----Setting data to none \n {e}")

        return DBUtils

    def query_to_json(query, servername=None, database=None, username=None, password=None):
        """Returns SQL query output to json array object Note: This needs to be parsed later

        Args:
            query (str): SQL query string
            servername (str, optional): DB servername . Defaults to None.
            database (str, optional): database name. Defaults to None.
            username (str, optional): username. Defaults to None.
            password (str, optional): password. Defaults to None.

        Returns:
            _type_: _description_
        """
        connect = DBUtils.__connect(servername, database, username, password)
        cursor = connect.cursor()
        data = cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        json_array = []
        rows = data.fetchall()
        for row in rows:
            formatted_row = [str(i) for i in row]
            json_array.append(dict(zip(columns, map(str, formatted_row))))
        return json_array

    def get_first_row():
        """Get only First row from SQL

        Returns:
            list: List of data
        """
        row = None
        try:
            row = DBUtils.data.fetchone()[0]
        except Exception as e:
            row = None
            ReportUtils.log(f"SQL exception----Setting data to none \n {e}")
        return row

    def get_all_row():
        """Get data for multi rows

        Returns:
            list: get multiple rows of data from connected sql
        """
        rows = None
        try:
            rows = DBUtils.data.fetchall()
        except Exception as e:
            rows = None
            ReportUtils.log(f"SQL exception----Setting data to none \n {e}")
        return rows

    def assert_row_count(expected_row_count):
        """Check and verify if row count is matching

        Args:
            expected_row_count (int): expected row count should match with get row
        """
        assert expected_row_count == DBUtils.get_first_row(), "Row count is not matching"

    def close_connection():
        """ Close any open DB connection """
        if DBUtils.cursor is not None:
            DBUtils.cursor.close()

    def call_stored_proc(procName, *args):
        conn = DBUtils.__connect()
        sql = """SET NOCOUNT ON;
            DECLARE @ret int
            EXEC @ret = %s %s
            SELECT @ret""" % (procName, ','.join(['?'] * len(args)))
        output = (conn.execute(sql, args).fetchone()[0])
        conn.commit()
        return output

    #  conn_str = (r'DRIVER={ODBC Driver 17 for SQL Server};'
    #                 r'SERVER=demo-neon-db01;'
    #                 r'DATABASE=neonCMS1;'
    #                 r'Trusted_Connection=yes;')