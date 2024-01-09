from sqlalchemy import MetaData, Table, Column, Integer, String, Date

arkikAnalizeReportsMeta = MetaData()

arkikAnalizeReportsModel = Table(
    "arkikAnalizeReports", arkikAnalizeReportsMeta,
    Column("arkikAnalizeReportsID", Integer, primary_key=True),
    Column("fecha", Date, nullable=True),
    Column("Nombre", String(255), nullable=True),
)
