import tomllib
from pathlib import Path
from shutil import move
from typing import Optional

import pandas as pd
import sqlalchemy.engine
from loguru import logger
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import insert

from report2sql.core.models import metadata_obj


class Report2SQLApp:
    def __init__(self):
        # default var
        self.TOML_FILE: Path = Path(__file__).parent.joinpath("r2s_config.toml")
        self.config: Optional[dict] = None
        logger.add("r2s_log.log")

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

        # Create tables
        metadata_obj.create_all(self.get_engine())

        # load xmls to sql
        self.xmls2sql()

    def get_excel_files(self):
        excel_files = []
        # if self.config["config"]["ruta_absoluta"]:
        get_from_dir: Path = Path(self.config["config"]["ruta_reportes_nuevos"])
        excel_files.extend(get_from_dir.glob("*.xls?"))
        return excel_files

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
        return create_engine(conn_string, echo=True)

    def create_tables(self):
        engine = self.get_engine()
        metadata_obj.create_all(engine)

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

    def move2processed(self, file_path: Path):
        try:
            move(str(file_path),
                 self.config["config"]["ruta_reportes_procesados"])
            logger.info(f"{file_path.stem}: Se movio a procesados")
        except KeyError as e:
            logger.error(f"{type(e)}: {e}")
            return
        except Exception as e:
            logger.error(f"{type(e)}: {e}")
            return

    def xmls2sql(self):
        def insert_on_conflict_nothing(table, conn, keys, data_iter):
            # TODO AGREGAR ROW COUNT return result.rowcount
            # "a" is the primary key in "conflict_table"
            data = [dict(zip(keys, row)) for row in data_iter]
            for r_dict in data:
                try:
                    stmt = insert(table.table).values([r_dict])
                    result = conn.execute(stmt)
                except IntegrityError as e:
                    logger.info(f"{e.orig}")
                    continue

        xml_files = self.get_excel_files()

        for xml_file in xml_files:
            process_error: bool = False
            try:
                xml_dataframe = pd.read_excel(xml_file)
                xml_dataframe.to_sql(
                    name=self.config["connection"]["table"],
                    con=self.get_engine(),
                    if_exists="append",
                    index=False,
                    method=insert_on_conflict_nothing
                )
                if not process_error:
                    self.move2processed(xml_file)

            except PermissionError as e:
                process_error = True
                logger.error(f"{e}")
                continue
            except TypeError as e:
                process_error = True
                logger.error(f"{xml_file}: {e}")
                continue
            finally:
                pass


if __name__ == "__main__":
    app = Report2SQLApp()

