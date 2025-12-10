# analysis.py
import pandas as pd

def load_dataframes(engine):
    """
    EXERCÍCIO 7: Carrega as tabelas do banco para DataFrames.
    Retorna: (df_movies, df_series)
    """
    print("--> Lendo dados do banco de dados...")
    try:
        df_movies = pd.read_sql_table('movies', engine)
        df_series = pd.read_sql_table('series', engine)
        
        return df_movies, df_series
    
    except ValueError:
        print("Aviso: As tabelas ainda não existem no banco. (Rode o Ex 6 primeiro)")
        return pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        print(f"Erro ao ler banco de dados: {e}")
        return pd.DataFrame(), pd.DataFrame()

def classify_rating(rating):
    """
    Função auxiliar para o EXERCÍCIO 9.
    Classifica o filme com base na nota.
    """
    if rating >= 9.0:
        return "Obra-prima"
    elif 8.5 <= rating < 9.0:
        return "Excelente"
    elif 7.5 <= rating < 8.5:
        return "Muito Bom"
    elif 6.0 <= rating < 7.5:
        return "Bom"
    else:
        return "Mediano"

def analyze_and_export(df_movies, df_series):
    """
    EXERCÍCIO 8: Análise e Exportação.
    1. Ordena por nota (maior para menor).
    2. Filtra notas > 9.0.
    3. Exporta tudo para CSV e JSON.
    Retorna: O DataFrame filtrado (para ser exibido no main).
    """
    print("--> Iniciando análise e exportação...")

    if df_movies.empty:
        print("Aviso: DataFrame de filmes está vazio.")
        return pd.DataFrame()

    # 1. Ordenar os filmes pela coluna de nota (maior para o menor)
    df_sorted = df_movies.sort_values(by='rating', ascending=False)

    # 2. Filtrar apenas os filmes com nota maior que 9.0
    df_filtered = df_sorted[df_sorted['rating'] > 9.0].copy()

    # 3. Exportação com try-except
    try:
        # Exportando CSV (sem o índice numérico do pandas)
        df_sorted.to_csv('movies.csv', index=False)
        df_series.to_csv('series.csv', index=False)
        
        # Exportando JSON (orient='records' cria uma lista de objetos, indent=4 deixa legível)
        df_sorted.to_json('movies.json', orient='records', indent=4, force_ascii=False)
        df_series.to_json('series.json', orient='records', indent=4, force_ascii=False)
        
        print(f"Sucesso! Arquivos gerados: 'movies.csv', 'series.csv', 'movies.json', 'series.json'.")
        
    except PermissionError:
        print("Erro: Permissão negada ao salvar o arquivo. Verifique se ele está aberto.")
    except Exception as e:
        print(f"Erro ao exportar arquivos: {e}")

    # Retorna o dataframe filtrado para exibir no main
    return df_filtered

def generate_summary(df_movies):
    """
    EXERCÍCIO 9 e 10:
    - Aplica classificação textual (apply).
    - Gera tabela dinâmica (pivot_table).
    Retorna: (summary_table, df_movies_classificado)
    """
    if df_movies.empty:
        return pd.DataFrame(), pd.DataFrame()

    # --- EXERCÍCIO 9: Classificação (Apply) ---
    # Cria uma nova coluna 'categoria' baseada na nota
    df_movies['categoria'] = df_movies['rating'].apply(classify_rating)

    # --- EXERCÍCIO 10: Tabela Resumo (Pivot/Group) ---
    summary = df_movies.pivot_table(
        index='year',           
        columns='categoria',   
        values='title',       
        aggfunc='count',       
        fill_value=0            
    )

    return summary, df_movies
    
