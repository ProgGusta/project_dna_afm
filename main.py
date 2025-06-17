# main.py
import os
import pandas as pd
from src.dna_analyzer import (
    Loader,
    Saver,
    StatsCalculator,
    Analyzer
)

def run_analysis():
    # --- Configuração ---
    INPUT_DIR = './data/processed/extended_images'  # Diretório de entrada
    OUTPUT_DIR = './results/statistics/perimeters'  # Nome da pasta de saída

    ANALYZER_CONFIG = {
        'segmenter': {'canny_threshold1': 100, 'canny_threshold2': 200},
        'extractor': {'circularity_threshold': 0.8}
    }

    # --- Inicialização dos Objetos ---
    loader = Loader()
    analyzer = Analyzer(config=ANALYZER_CONFIG)
    saver = Saver(output_directory=OUTPUT_DIR)
    stats_calculator = StatsCalculator()

    # --- Processamento ---
    image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    all_stats = []

    for filename in image_files:
        print(f"Processando {filename}...")
        image_path = os.path.join(INPUT_DIR, filename)

        image = loader.load_grayscale(image_path)
        if image is None:
            continue

        results = analyzer.process(image)
        
        stats = results["statistics"]
        stats['Imagem'] = filename
        all_stats.append(stats)
        
        # Opcional: Salvar imagens individuais de DNA/RNA pode ser feito aqui se necessário
        # base_name = os.path.splitext(filename)[0]
        # saver.save_image(results["dna_image"], f"{base_name}_dna.png")
        # saver.save_image(results["rna_image"], f"{base_name}_rna.png")

    # --- Finalização e Geração de Relatórios ---
    if not all_stats:
        print("Nenhuma imagem processada. Encerrando.")
        return

    # 1. Criar e salvar o DataFrame de resultados por imagem (como antes)
    df_results = pd.DataFrame(all_stats)
    df_results = df_results[['Imagem', 'Num DNA', 'Perímetro DNA', 'Num RNA', 'Perímetro RNA']]
    saver.save_dataframe(df_results, "resultados_perimetros.csv")

    # 2. Calcular e salvar as estatísticas descritivas gerais
    print("\nCalculando estatísticas descritivas gerais...")
    df_descriptive_stats = stats_calculator.calculate_descriptive_stats(df_results)
    saver.save_dataframe(df_descriptive_stats, "estatisticas_descritivas_gerais.csv")
    
    print("\nAnálise e geração de estatísticas concluídas com sucesso.")

if __name__ == "__main__":
    run_analysis()