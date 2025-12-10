# models.py

class TV:
    """
    Classe Base (Exercício 3)
    """
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return f"{self.title} ({self.year})"


class Movie(TV):
    """
    Exercício 4: Especialização para Filmes.
    Adiciona: rating (nota).
    """
    def __init__(self, title, year, rating):
        super().__init__(title, year) # Chama o construtor da classe TV
        self.rating = rating

    def __str__(self):
        # Formato pedido: Título (Ano) – Nota: X.X
        return f"{self.title} ({self.year}) – Nota: {self.rating}"


class Series(TV):
    """
    Exercício 4: Especialização para Séries.
    Adiciona: seasons (temporadas) e episodes (episódios totais).
    """
    def __init__(self, title, year, seasons, episodes):
        super().__init__(title, year)
        self.seasons = seasons
        self.episodes = episodes

    def __str__(self):
        # Formato pedido: Título (Ano) – Temporadas: N, Episódios: M
        return f"{self.title} ({self.year}) – Temporadas: {self.seasons}, Episódios: {self.episodes}"