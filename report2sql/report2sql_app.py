import tomllib
from pathlib import Path
from typing import Optional

import sqlalchemy.engine
from sqlalchemy import create_engine
import pandas as pd

from report2sql.core.models import arkikAnalizeReportsMeta


class Report2SQLApp:
    def __init__(self):
        # default var
        self.TOML_FILE: Path = Path(__file__).parent.joinpath("r2s_config.toml")
        self.config: Optional[dict] = None
        self.excel_files: list = []

        # run tasks
        self.task_at_start()
        # self.get_sql_test()

    def task_at_start(self):
        # TODO check files
        # load toml config
        with open(str(self.TOML_FILE), "rb") as config_file:
            self.config = tomllib.load(config_file)

        # check paths
        Path(self.config["config"]["ruta_reportes_nuevos"]).mkdir(parents=True, exist_ok=True)
        Path(self.config["config"]["ruta_reportes_procesados"]).mkdir(parents=True, exist_ok=True)

        #

    def get_files(self):
        self.excel_files.clear()
        # if self.config["config"]["ruta_absoluta"]:
        get_from_dir: Path = Path(self.config["config"]["ruta_reportes_nuevos"])
        self.excel_files.extend(get_from_dir.glob("*.xls?"))

    def get_engine(self) -> sqlalchemy.engine.Engine:
        str_driver = r"Driver={0};".format(
            self.config["connection"]["odbc_driver"]
        )
        str_server = r"Server={0};".format(
            self.config["connection"]["server_instancename"]
        )
        str_database = r"Database={0};".format(
            self.config["connection"]["database"]
        )
        str_user = r"UID={0};".format(
            self.config["connection"]["username"]
        )
        str_psw = r"PWD={0};".format(
            self.config["connection"]["password"]
        )
        conn_str = f"{str_driver}{str_server}{str_database}{str_user}{str_psw}"
        conn_string = r"mssql+pyodbc:///?odbc_connect={}".format(conn_str)
        return create_engine(conn_string)

    def create_table(self):
        engine = self.get_engine()
        arkikAnalizeReportsMeta.create_all(engine)

    def get_sql_test(self):
        str_driver = r"Driver={0};".format(
            self.config["connection"]["odbc_driver"]
        )
        str_server = r"Server={0};".format(
            self.config["connection"]["server_instancename"]
        )
        str_database = r"Database={0};".format(
            self.config["connection"]["database"]
        )
        str_user = r"UID={0};".format(
            self.config["connection"]["username"]
        )
        str_psw = r"PWD={0};".format(
            self.config["connection"]["password"]
        )
        conn_str = f"{str_driver}{str_server}{str_database}{str_user}{str_psw}"
        conn_string = r"mssql+pyodbc:///?odbc_connect={}".format(conn_str)
        engine = create_engine(conn_string)

        with engine.connect() as conn, conn.begin():
            data = pd.read_sql_table("ListaEmpresas", conn)
            print(data)






if __name__ == "__main__":
    app = Report2SQLApp()
    app.get_files()
    print(app.excel_files)
