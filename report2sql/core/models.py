from sqlalchemy import MetaData, Table, Column, BigInteger,Integer, String, DateTime, Float, PrimaryKeyConstraint

metadata_obj = MetaData()


arkikAnalizeReportsModel = Table(
	"arkikAnalizeReports", metadata_obj,
	Column("RowVersion", BigInteger, autoincrement=True, index=True),
	Column("Fecha de Ticket", DateTime, nullable=False, primary_key=True),
	Column("Número de Pedido", String(15), nullable=False, primary_key=True),
	Column("Código de Cliente", String, nullable=False),
	Column("Nombre de Cliente", String, nullable=False),
	Column("RFC", String, nullable=True),
	Column("Código de Obra", String, nullable=True),
	Column("Nombre de Obra", String, nullable=True),
	Column("Tipo de Envío", String, nullable=True),
	Column("Número de Carga", String(15), nullable=False, primary_key=True),
	Column("Planta", String, nullable=True),
	Column("Nombre de Planta", String, nullable=True),
	Column("Estatus de la orden", String, nullable=True),
	Column("Solicitante de la Cancelación", DateTime, nullable=True),
	Column("Razón de la Cancelación", String, nullable=True),
	Column("Descripción de la Cancelación", DateTime, nullable=True),
	Column("Comentarios externos", String, nullable=True),
	Column("Bombeable", String, nullable=True),
	Column("Estatus de Item", String, nullable=True),
	Column("Tipo de Producto", String, nullable=True),
	Column("Código de Producto", String, nullable=False),
	Column("Nombre Corto de Producto", String, nullable=False),
	Column("Nombre Largo de Producto", String, nullable=True),
	Column("Unidad de Medida", String, nullable=True),
	Column("Cantidad", Float, nullable=True),
	Column("Número de Entrega", String, nullable=True),
	Column("Número de Remisión", String, nullable=True),
	Column("Número de Transporte", String, nullable=True),
	Column("Vehículo", String, nullable=True),
	Column("Código de Chofer", String, nullable=True),
	Column("Nombre del Chofer", String, nullable=True),
	Column("Hora de Carga", DateTime, nullable=True),
	Column("Duración de Carga", Float, nullable=True),
	Column("Hora de Fin de Carga", DateTime, nullable=True),
	Column("Duración Post Fabricación", Float, nullable=True),
	Column("Hora Salida a Obra", DateTime, nullable=True),
	Column("Duración hacia Obra", Float, nullable=True),
	Column("Hora Llegada a Obra", DateTime, nullable=True),
	Column("Duración en Obra", Float, nullable=True),
	Column("Hora Inicio Descarga", DateTime, nullable=True),
	Column("Duración de Descarga", Float, nullable=True),
	Column("Hora Fin de Descarga", DateTime, nullable=True),
	Column("Duración de Lavado", Float, nullable=True),
	Column("Hora Salida a Planta", DateTime, nullable=True),
	Column("Duración hacia Planta", Float, nullable=True),
	Column("Hora Llegada a Planta", DateTime, nullable=True),
	Column("Tiempo de Ciclo", Float, nullable=True),
	PrimaryKeyConstraint("Fecha de Ticket", "Número de Pedido", "Número de Carga", name="aar_pk")
)

