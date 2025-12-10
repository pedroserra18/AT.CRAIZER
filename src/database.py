# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError
from src.models import Movie, Series

# Base do SQLAlchemy para criar as tabelas
Base = declarative_base()

# --- Definição da Tabela Movies ---
class MovieDB(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)  
    year = Column(Integer)
    rating = Column(Float)

# --- Definição da Tabela Series ---
class SeriesDB(Base):
    __tablename__ = 'series'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True) # unique=True para evitar repetição
    year = Column(Integer)
    seasons = Column(Integer)
    episodes = Column(Integer)

def setup_database():
    """Cria o arquivo imdb.db e as tabelas se não existirem."""
    engine = create_engine('sqlite:///imdb.db')
    Base.metadata.create_all(engine)
    return engine

def save_catalog_to_db(engine, catalog):
    """
    Recebe a conexão (engine) e a lista de objetos (catalog).
    Salva cada item na tabela correta tratando duplicatas.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print(f"--> Iniciando inserção de {len(catalog)} itens no banco...")
    
    novos = 0
    duplicados = 0
    
    for item in catalog:
        db_obj = None
        
        # Verifica se o item da lista é Filme ou Série para criar o objeto de Banco correspondente
        if isinstance(item, Movie):
            db_obj = MovieDB(
                title=item.title,
                year=item.year,
                rating=item.rating
            )
        elif isinstance(item, Series):
            db_obj = SeriesDB(
                title=item.title,
                year=item.year,
                seasons=item.seasons,
                episodes=item.episodes
            )
            
        if db_obj:
            try:
                # Tenta adicionar e salvar
                session.add(db_obj)
                session.commit()
                novos += 1
            except IntegrityError:
                # Se der erro de integridade (duplicata), faz rollback e segue o baile
                session.rollback()
                duplicados += 1
        

    session.close()
    print(f"Processo finalizado. Novos inseridos: {novos} | Duplicados ignorados: {duplicados}")
