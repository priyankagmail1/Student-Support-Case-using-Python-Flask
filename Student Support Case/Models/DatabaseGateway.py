from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


class DatabaseGateway(object):
    """Initialize mysql database """
    db_host = "localhost"
    db_user = "root"
    db_password = ""
    db_name = "lms"
    current_table = ""

    def __init__(self, application):
        application.config["MYSQL_DATABASE_HOST"] = self.db_host
        application.config["MYSQL_DATABASE_USER"] = self.db_user
        application.config["MYSQL_DATABASE_PASSWORD"] = self.db_password
        application.config["MYSQL_DATABASE_DB"] = self.db_name

        self.mysql_manager = MySQL(application, cursorclass=DictCursor)

    def get_cursor(self):
        return self.mysql_manager.get_db().cursor()

    def execute_query(self, sql_query):
        db_cursor = self.get_cursor()
    
        if (len(self.current_table) > 0):
            sql_query = sql_query.replace("@table", self.current_table)

        db_cursor.execute(sql_query)

        return db_cursor

    def commit_transaction(self):
        self.execute_query("COMMIT;")