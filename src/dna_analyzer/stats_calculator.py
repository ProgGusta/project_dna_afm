# src/dna_analyzer/stats_calculator.py
import pandas as pd

class StatsCalculator:
    """
    Calcula estatísticas descritivas a partir de um DataFrame de resultados.
    """

    def calculate_descriptive_stats(self, results_df: pd.DataFrame):
        """
        Calcula média, mediana, moda, variância, desvio padrão, quartis e decis.

        Args:
            results_df (pd.DataFrame): DataFrame contendo os resultados numéricos da análise.

        Returns:
            pd.DataFrame: Um novo DataFrame contendo as estatísticas calculadas.
        """
        if results_df.empty:
            print("Atenção: O DataFrame de resultados está vazio. Nenhuma estatística foi calculada.")
            return pd.DataFrame()

        # Garante que apenas colunas numéricas sejam usadas nos cálculos
        numeric_df = results_df.select_dtypes(include=['number'])

        stats = {
            'Média': numeric_df.mean(),
            'Mediana': numeric_df.median(),
            'Moda': numeric_df.mode().iloc[0],  # Pega a primeira moda, caso haja mais de uma
            'Variância': numeric_df.var(),
            'Desvio Padrão': numeric_df.std(),
            'Mínimo': numeric_df.min(),
            'Máximo': numeric_df.max(),
            'Q1 (25%)': numeric_df.quantile(0.25),
            'Q2 (50%) - Mediana': numeric_df.quantile(0.50),
            'Q3 (75%)': numeric_df.quantile(0.75),
            'D1 (10%)': numeric_df.quantile(0.10),
            'D9 (90%)': numeric_df.quantile(0.90)
        }

        # Cria e retorna um DataFrame a partir do dicionário de estatísticas
        stats_df = pd.DataFrame(stats)
        return stats_df