from sqlmodel import create_engine
from config import cfg


#数据库访问地址
# SQLALCHEMY_DATABASE_URL = "sqlite:///./api.db"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:valor123456@localhost:3306/valor_database"
# SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://valor:valor123456@localhost/valor_database"

engine = create_engine(cfg.SQLALCHEMY_DATABASE_URL)

# db_session = Session(bind=engine)