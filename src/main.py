# main.py
import json
import os
import sys
from typing import List, Dict, Any, Tuple
from sqlalchemy.engine import Engine
import pandas as pd

# Módulos locais (Importação direta pois estão na mesma pasta src/)
import scraper
import database
import analysis
from models import TV, Movie, Series

# --- CONFIGURAÇÕES E UTILITÁRIOS ---

def load_config() -> Dict:
    """Carrega as configurações do JSON."""
    # Procura o config.json na mesma pasta onde o main.py está rodando
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, 'config.json')
    
    if not os.path.exists(config_path):
        # Tenta procurar na pasta anterior caso não ache (fallback)
        config_path = 'config.json' 
        if not os.path.exists(config_path):
            return {}

    with open(config_path, 'r') as f:
        return json.load(f)

def print_header(title: str):
    """Função auxiliar para imprimir cabeçalhos padronizados."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

# --- DEFINIÇÃO DOS EXERCÍCIOS (FUNÇÕES) ---

def exercicio_1_scraping(config: Dict) -> List[Dict]:
    """Realiza o scraping do Top 250."""
    print_header(">>> EXERCÍCIO 1: Scraping básico do IMDb Top 250")
    
    raw_data = scraper.get_imdb_data(config)
    
    if raw_data:
        print(f"Sucesso! Total extraído: {len(raw_data)}")
        print("[Exibindo os 10 primeiros títulos]:")
        for item in raw_data[:10]:
            print(f" - {item['title']}")
        return raw_data
    else:
        print("Erro crítico: Nenhum dado extraído.")
        sys.exit(1)

def exercicio_2_formatacao(raw_data: List[Dict]):
    """Exibe os dados formatados (Título, Ano, Nota)."""
    print_header(">>> EXERCÍCIO 2: Título, ano e nota dos filmes")
    
    print("[Exibindo os 5 primeiros filmes formatados]:")
    for item in raw_data[:5]:
        print(f"{item['title']} ({item['year']}) – Nota: {item['rating']}")

def exercicio_3_classe_tv():
    """Testa a classe base TV."""
    print_header(">>> EXERCÍCIO 3: Classe base TV (Teste Unitário)")
    
    # Teste isolado
    exemplo_tv = TV("Guerra Mundial Z", 2013)
    print("Objeto da classe TV criado.")
    print(f"Teste do método __str__: {exemplo_tv}")

def exercicio_4_classes_filhas():
    """Testa as classes Movie e Series."""
    print_header(">>> EXERCÍCIO 4: Classes Movie e Series (Herança)")
    
    filme = Movie("O Poderoso Chefão", 1972, 9.2)
    serie = Series("Breaking Bad", 2008, 5, 62)
    
    print("Testando a formatação (método __str__) sobrescrita:")
    print(f"Filme: {filme}")
    print(f"Série: {serie}")

def exercicio_5_criar_catalogo(raw_data: List[Dict]) -> List[TV]:
    """Converte dados brutos em objetos e adiciona séries manuais."""
    print_header(">>> EXERCÍCIO 5: Lista de objetos (Scraping + Manuais)")
    
    catalog = []
    
    # 1. Scraping -> Objetos Movie
    for item in raw_data:
        catalog.append(Movie(item['title'], item['year'], item['rating']))
    print(f"Filmes convertidos do scraping: {len(catalog)}")
    
    # 2. Séries Manuais -> Objetos Series
    s1 = Series("Breaking Bad", 2008, 5, 62)
    s2 = Series("Game of Thrones", 2011, 8, 73)
    catalog.extend([s1, s2])
    
    print("Séries manuais adicionadas.")
    
    # 3. Verificação
    print("\n[Verificando Polimorfismo - Amostra]:")
    print(f"Primeiro item (Filme): {catalog[0]}")
    print(f"Último item (Série): {catalog[-1]}")
    
    return catalog

def exercicio_6_banco_dados(catalog: List[TV]) -> Engine:
    """Salva o catálogo no SQLite."""
    print_header(">>> EXERCÍCIO 6: Persistência no SQLite")
    
    engine = database.setup_database()
    print("Banco conectado.")
    
    if catalog:
        database.save_catalog_to_db(engine, catalog)
    else:
        print("Aviso: Catálogo vazio.")
        
    return engine

def exercicio_7_pandas_leitura(engine: Engine) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Lê do banco para DataFrames."""
    print_header(">>> EXERCÍCIO 7: DataFrames com Pandas")
    
    df_movies, df_series = analysis.load_dataframes(engine)
    
    if not df_movies.empty:
        print("[Filmes - Top 5]:")
        print(df_movies.head(5).to_string(index=False))
    
    if not df_series.empty:
        print("\n[Séries - Top 5]:")
        print(df_series.head(5).to_string(index=False))
        
    return df_movies, df_series

def exercicio_8_exportacao(df_movies: pd.DataFrame, df_series: pd.DataFrame) -> pd.DataFrame:
    """Filtra melhores filmes e exporta arquivos."""
    print_header(">>> EXERCÍCIO 8: Filtragem (> 9.0) e Exportação")
    
    df_best = analysis.analyze_and_export(df_movies, df_series)
    
    if not df_best.empty:
        print("\n[Top 5 Filmes com Nota > 9.0]:")
        print(df_best[['title', 'rating', 'year']].head(5).to_string(index=False))
    else:
        print("Nenhum filme acima de 9.0 encontrado.")
        
    return df_best

def exercicio_9_classificacao(df_movies: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Aplica classificação textual (apply)."""
    print_header(">>> EXERCÍCIO 9: Classificação Automática")
    
    summary_table, df_classified = analysis.generate_summary(df_movies)
    
    print("Amostra da nova coluna 'categoria':")
    print(df_classified[['title', 'rating', 'categoria']].head(10).to_string(index=False))
    
    return summary_table, df_classified

def exercicio_10_resumo(summary_table: pd.DataFrame):
    """Exibe tabela pivô."""
    print_header(">>> EXERCÍCIO 10: Tabela Resumo (Filmes por Ano)")
    
    print("Contagem de filmes (últimos 5 anos):")
    print(summary_table.tail(5))

# --- FUNÇÃO PRINCIPAL (ORQUESTRADOR) ---

def main():
    print("INICIANDO ASSESSMENT (MODO PROFISSIONAL)")
    
    # Configuração Inicial
    config = load_config()
    
    # --- FLUXO DE EXECUÇÃO (PIPELINE) ---
    try:
        # Ex 1: Coleta
        raw_data = exercicio_1_scraping(config)
        
        # Ex 2: Visualização
        exercicio_2_formatacao(raw_data)
        
        # Ex 3 & 4: Testes de Classes
        exercicio_3_classe_tv()
        exercicio_4_classes_filhas()
        
        # Ex 5: Criação dos Objetos (Transformação)
        catalog = exercicio_5_criar_catalogo(raw_data)
        
        # Ex 6: Banco de Dados (Carga)
        engine = exercicio_6_banco_dados(catalog)
        
        # Ex 7: Leitura para Análise
        df_movies, df_series = exercicio_7_pandas_leitura(engine)
        
        if df_movies.empty:
            print("Erro: Sem dados para análise. Encerrando.")
            return

        # Ex 8: Análise e Exportação
        exercicio_8_exportacao(df_movies, df_series)
        
        # Ex 9: Classificação
        summary_table, _ = exercicio_9_classificacao(df_movies)
        
        # Ex 10: Relatório Final
        exercicio_10_resumo(summary_table)

    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário.")
    except Exception as e:
        # Importante: Imprime o erro completo para debug
        import traceback
        traceback.print_exc()
    finally:
        print_header("FIM DO PROGRAMA")

if __name__ == "__main__":
    main()