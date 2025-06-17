# main_dose_response.py
# Este script executa uma análise de dose-resposta usando o pacote dna_analyzer.
import os
from src.dna_analyzer import (
    Loader,
    Visualizer,
    Analyzer
)

def run_dose_response_analysis():
    # --- Configuração ---
    OUTPUT_DIR = './results/figures/dose_response'  # Nome da pasta de saída para os gráficos

    # Dicionário mapeando a dose para o caminho da imagem correspondente
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
    
    # --- Processamento ---
    all_results = []

    for dose, image_path in IMAGE_PATHS.items():
        print(f"Processando amostra da dose: {dose}...")
        
        if not os.path.exists(image_path):
            print(f"  AVISO: Arquivo não encontrado em '{image_path}'. Pulando esta dose.")
            continue

        image = loader.load_grayscale(image_path)
        if image is None:
            continue

        # Reutiliza o Analyzer para processar a imagem
        results = analyzer.process(image)
        
        # Adiciona a informação da dose ao dicionário de resultados
        current_result = results["statistics"]
        current_result['Dose'] = dose
        all_results.append(current_result)

    # --- Apresentação e Visualização dos Resultados ---
    if not all_results:
        print("\nNenhuma imagem foi processada com sucesso. Análise encerrada.")
        return

    print("\n--- Resultados da Análise de Dose-Resposta ---")
    for r in all_results:
        print(f"Dose: {r['Dose']}")
        print(f"  Fragmentos de DNA: {r['Num DNA']}, Perímetro Total: {r['Perímetro DNA']:.2f}")
        print(f"  Fragmentos de RNA: {r['Num RNA']}, Perímetro Total: {r['Perímetro RNA']:.2f}\n")
    
    # Gera e salva os gráficos de dose-resposta
    visualizer.plot_dose_response(all_results, output_dir=OUTPUT_DIR)
    
if __name__ == "__main__":
    run_dose_response_analysis()