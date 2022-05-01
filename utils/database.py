import io
import yaml
# import psycopg2
import pandas as pd

from sqlalchemy import create_engine, select, MetaData, Table, and_

class Database():

    def __init__(self, config_file) -> None:

        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        self.username = config['pg_user']
        self.password = config['pg_password'] # FIXME: insecure
        self.host = config['pg_host']
        self.port = config['pg_port']
        self.database = config['pg_dbname']

        # conn_str = f"dbname='{config['dbname']}' "
        # conn_str += f"user='{config['pg_user']}' "
        # conn_str += f"host='{config['pg_host']}' "
        # conn_str += f"password='{config['pg_password']}'"

        conn_str = f"postgresql+psycopg2://{self.username}:"
        conn_str += f"{self.password}@{self.host}:"
        conn_str += f"{self.port}/{self.database}"

        try:
            # self.conn = psycopg2.connect(conn_str)
            self.engine = create_engine(conn_str)
            self.metadata = MetaData(bind=None)

            print("Successfully connected to database.")
        except Exception as e:
            raise e

    def upload_pd(self, df, name):

        # drop old table and creates new empty table
        df.head(0).to_sql(name, self.engine, if_exists='replace',index=False)

        conn = self.engine.raw_connection()
        cur = conn.cursor()
        output = io.StringIO()
        df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        contents = output.getvalue()
        cur.copy_from(output, name, null="") # null values become ''
        conn.commit()

        return True

    def load_table(self, table_name):
        """
        TODO: add filtering capabilities
        """
        
        table = Table(
            table_name, 
            self.metadata, 
            autoload=True, 
            autoload_with=self.engine
        )

        stmt = select(table)
        
        # [
        #     table.columns.column1, 
        #     table.columns.column2]
        # ).where(and_(
        #     table.columns.column1 == 'filter1', 
        #     table.columns.column2 == 'filter2'   
        # )

        connection = self.engine.connect()
        results = connection.execute(stmt).fetchall()

        df = pd.DataFrame(results)

        return df