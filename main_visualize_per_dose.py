# main_visualize_per_dose.py
# Este script executa a análise e visualiza os contornos classificados para cada dose.
import os
from src.dna_analyzer import (
    Loader,
    Visualizer,
    Analyzer
)

def run_visualization_per_dose():
    # --- Configuração ---
    IMAGE_PATHS = {
        'Sem Irradiar': './data/processed/extended_images/sample_segmentation_17.png',
        '0.4 Gy': './data/processed/extended_images/Amostra 1_0,4 Gy 2023-10-18 15h17m27_3x3 (1).png',
        '0.7 Gy': './data/processed/extended_images/Amostrairradiada_03_0,7Gy_3x3.png',
        '1.0 Gy': './data/processed/extended_images/Amostrairradiada_02_1Gy_3x3.png'
    }

    ANALYZER_CONFIG = {
        'segmenter': {'canny_threshold1': 100, 'canny_threshold2': 200},
        'extractor': {'circularity_threshold': 0.8}
    }

    # --- Inicialização dos Objetos ---
    loader = Loader()
    analyzer = Analyzer(config=ANALYZER_CONFIG)
    visualizer = Visualizer()
    
    # --- Processamento e Visualização ---
    all_results = []

    for dose, image_path in IMAGE_PATHS.items():
        print(f"Processando amostra da dose: {dose}...")
        
        if not os.path.exists(image_path):
            print(f"  AVISO: Arquivo não encontrado em '{image_path}'. Pulando esta dose.")
            continue

        image = loader.load_grayscale(image_path)
        if image is None:
            continue

        # A classe Analyzer já faz todo o processamento e retorna tudo o que precisamos
        results = analyzer.process(image)
        
        # Adiciona a informação da dose e armazena
        current_stats = results["statistics"]
        current_stats['Dose'] = dose
        all_results.append(current_stats)

        # Usa o novo método do Visualizer para exibir o par de imagens (DNA/RNA)
        visualizer.plot_classified_image_pair(
            dna_image=results["dna_image"], 
            rna_image=results["rna_image"],
            title_prefix=dose
        )

    # --- Relatório Final no Console ---
    if not all_results:
        print("\nNenhuma imagem foi processada com sucesso.")
        return

    print("\n--- Resultados Numéricos Finais ---")
    for result in all_results:
        print(f"Dose: {result['Dose']}")
        print(f"  Número de fragmentos de DNA detectados: {result['Num DNA']}")
        print(f"  Soma total dos perímetros de DNA: {result['Perímetro DNA']:.2f}")
        print(f"  Número de fragmentos de RNA detectados: {result['Num RNA']}")
        print(f"  Soma total dos perímetros de RNA: {result['Perímetro RNA']:.2f}\n")

if __name__ == "__main__":
    run_visualization_per_dose()