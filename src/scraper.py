import requests
from bs4 import BeautifulSoup

def get_imdb_data(config):
    """
    Acessa o Top 250 do IMDb e retorna uma lista de dicionários.
    """
   
    url = "https://www.imdb.com/pt/chart/top/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    print(f"--> Acessando {url} (Configurado para Português)...")
    
    try:
        response = requests.get(url, headers=headers)
        # Verifica se deu erro de conexão (ex: 404 ou 500)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, "html.parser")
        movies = []
        
        # Seleciona a lista de filmes
        items = soup.select('li.ipc-metadata-list-summary-item')
        
        # Define o limite baseado na config ou pega 250
        limit = config.get('limit', 250)

        for item in items[:limit]:
            try:
                # Extração do Título 
                title_tag = item.select_one('h3.ipc-title__text')
                full_title = title_tag.text.strip()
                
                # Limpeza: Transforma "1. Um Sonho de Liberdade" em "Um Sonho de Liberdade"
                if '. ' in full_title:
                    title = full_title.split('. ', 1)[1]
                else:
                    title = full_title

                #  Extração do Ano 
                # O ano costuma ser o primeiro item de metadados
                metadata_items = item.select('span.cli-title-metadata-item')
                if metadata_items:
                    # Tenta pegar o texto e converter para int
                    year_text = metadata_items[0].text.strip()
                    # Verifica se é numérico (às vezes aparece classificação etária)
                    if year_text.isdigit():
                        year = int(year_text)
                    else:
                        year = 0 
                else:
                    year = 0
                
                # Extração da Nota
                rating_tag = item.select_one('span.ipc-rating-star')
                if rating_tag:
                   
                    rating_str = rating_tag.text.strip().split()[0]
                   
                    rating = float(rating_str.replace(',', '.'))
                else:
                    rating = 0.0

                movies.append({
                    'title': title,
                    'year': year,
                    'rating': rating
                })
                
            except Exception as e:
                # Se um filme der erro, pula para o próximo sem quebrar o programa
                continue
                
        return movies

    except Exception as e:
        print(f"Erro Crítico no Scraping: {e}")
        return []
