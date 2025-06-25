# src/dna_analyzer/stats_calculator.py
import pandas as pd
from scipy import stats
from itertools import combinations
import re

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
    
    def calculate_length_descriptive_stats(self, length_df: pd.DataFrame):
        """
        Calcula estatísticas descritivas para uma lista de comprimentos de moléculas,
        agrupados por uma categoria (ex: Dose).

        Args:
            length_df (pd.DataFrame): DataFrame com colunas como 'Dose' e 'Comprimento'.

        Returns:
            pd.DataFrame: DataFrame com as estatísticas calculadas por grupo.
        """
        if length_df.empty:
            print("Atenção: DataFrame de comprimentos vazio.")
            return pd.DataFrame()

        # Agrupa por 'Dose' e calcula as estatísticas para a coluna 'Comprimento'
        stats = length_df.groupby('Dose')['Comprimento'].agg(
            ['mean', 'median', 'std', 'min', 'max']
        )

        # Calcula os quartis separadamente e os adiciona ao DataFrame
        quartiles = length_df.groupby('Dose')['Comprimento'].quantile([0.25, 0.5, 0.75]).unstack()
        quartiles.columns = ['Q1 (25%)', 'Q2 (50%)', 'Q3 (75%)']
        
        # Junta os dois DataFrames
        full_stats = pd.concat([stats, quartiles], axis=1).round(2)
        
        return full_stats
    
    def perform_inferential_analysis(self, length_df: pd.DataFrame):
        """
        Realiza testes de hipótese e correlação nos dados de comprimento.

        Args:
            length_df (pd.DataFrame): DataFrame com colunas 'Dose' e 'Comprimento'.

        Returns:
            str: Uma string formatada com o relatório da análise inferencial.
        """
        if length_df.empty or length_df['Dose'].nunique() < 2:
            return "Análise inferencial não pôde ser realizada (dados insuficientes)."

        report = []
        report.append("--- Análise Estatística Inferencial ---\n")

        # Ordena as doses de forma inteligente (numericamente quando possível)
        def sort_key(dose_str):
            # Tenta extrair um número do início da string da dose
            match = re.match(r"([0-9,.]+)", dose_str)
            return float(match.group(1).replace(',', '.')) if match else -1

        doses = sorted(length_df['Dose'].unique(), key=sort_key)
        groups = [length_df[length_df['Dose'] == dose]['Comprimento'] for dose in doses]

        # 1. Teste de Normalidade (Shapiro-Wilk para cada grupo)
        report.append("1. Teste de Normalidade (Shapiro-Wilk):")
        is_normal = {}
        for i, dose in enumerate(doses):
            if len(groups[i]) > 2:
                stat, p_val = stats.shapiro(groups[i])
                normality = 'Normal' if p_val > 0.05 else 'Não Normal'
                is_normal[dose] = (p_val > 0.05)
                report.append(f"  - Grupo '{dose}': p-valor = {p_val:.4f} ({normality})")
            else:
                is_normal[dose] = False # Não se pode testar normalidade com poucos dados
                report.append(f"  - Grupo '{dose}': Dados insuficientes para teste de normalidade.")
        report.append("-" * 30 + "\n")

        # 2. Teste de Diferença entre Grupos
        report.append("2. Teste de Diferença Estatística entre Grupos:")
        # ANOVA ou Kruskal-Wallis para todos os grupos
        all_normal = all(is_normal.values())
        if all_normal:
            # Assumindo variâncias iguais por simplicidade (poderia adicionar teste de Levene)
            f_val, p_val = stats.f_oneway(*groups)
            report.append(f"  - ANOVA (todos os grupos): F-statistic = {f_val:.4f}, p-valor = {p_val:.4f}")
        else:
            h_val, p_val = stats.kruskal(*groups)
            report.append(f"  - Kruskal-Wallis (todos os grupos): H-statistic = {h_val:.4f}, p-valor = {p_val:.4f}")

        # Comparações par a par (t-test ou Mann-Whitney U)
        report.append("\n  Comparações Par a Par:")
        for (i, j) in combinations(range(len(doses)), 2):
            dose1, dose2 = doses[i], doses[j]
            group1, group2 = groups[i], groups[j]

            if is_normal[dose1] and is_normal[dose2]:
                stat, p_val = stats.ttest_ind(group1, group2, equal_var=True) # Assumindo variâncias iguais
                test_name = "T-test"
            else:
                stat, p_val = stats.mannwhitneyu(group1, group2)
                test_name = "Mann-Whitney U"
            
            report.append(f"    - {dose1} vs {dose2} ({test_name}): p-valor = {p_val:.4f}")
        report.append("-" * 30 + "\n")

        # 3. Análise de Correlação (Dose vs. Comprimento)
        report.append("3. Análise de Correlação (Dose vs. Comprimento):")
        # Criar uma representação numérica das doses para correlação
        dose_map = {dose: i for i, dose in enumerate(doses)}
        numeric_doses = length_df['Dose'].map(dose_map)
        
        # Pearson para dados normais, Spearman para não normais
        if all_normal:
            corr, p_val = stats.pearsonr(numeric_doses, length_df['Comprimento'])
            report.append(f"  - Correlação de Pearson: r = {corr:.4f}, p-valor = {p_val:.4f}")
        else:
            corr, p_val = stats.spearmanr(numeric_doses, length_df['Comprimento'])
            report.append(f"  - Correlação de Spearman: rho = {corr:.4f}, p-valor = {p_val:.4f}")
        
        report.append("-" * 30 + "\n")
        report.append("4. Correlação (Dose Numérica vs. Comprimento MÉDIO):")

        try:
            # Calcula o comprimento médio para cada dose
            mean_lengths_by_dose = length_df.groupby('Dose')['Comprimento'].mean()
            
            # Garante que os dados estejam na mesma ordem
            ordered_means = [mean_lengths_by_dose[dose] for dose in doses]
            numeric_doses_for_corr = [sort_key(dose) for dose in doses]

            # Filtra casos onde a dose não pôde ser convertida para número
            valid_data = [(d, m) for d, m in zip(numeric_doses_for_corr, ordered_means) if d != -1]
            
            if len(valid_data) > 1:
                final_doses, final_means = zip(*valid_data)
                
                # Pearson
                corr_p, p_val_p = stats.pearsonr(final_doses, final_means)
                report.append(f"  - Correlação de Pearson: r = {corr_p:.4f}, p-valor = {p_val_p:.4f}")

                # Spearman
                corr_s, p_val_s = stats.spearmanr(final_doses, final_means)
                report.append(f"  - Correlação de Spearman: rho = {corr_s:.4f}, p-valor = {p_val_s:.4f}")
            else:
                report.append("  - Dados insuficientes para calcular a correlação com o comprimento médio.")
        except Exception as e:
            report.append(f"  - Erro ao calcular correlação com médias: {e}")

        return "\n".join(report)