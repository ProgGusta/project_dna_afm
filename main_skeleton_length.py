# main_skeleton_length.py
# Este script executa a análise de quantificação de comprimento esquelético.
# Lembre-se de instalar: pip install opencv-contrib-python
import os
from src.dna_analyzer import (
    Loader,
    Visualizer,
    Analyzer
)

def run_skeleton_length_analysis():
    # --- Configuração ---
    OUTPUT_DIR = './results/figures/skeleton_length/'  # Nome da pasta de saída para os gráficos

    # Dicionário mapeando a dose para o caminho da imagem
    IMAGE_PATHS = {
        'Sem Irradiar': './data/processed/extended_images/sample_segmentation_17.png',
        '0.4 Gy': './data/processed/extended_images/Amostra 1_0,4 Gy 2023-10-18 15h17m27_3x3 (1).png',
        '0.7 Gy': './data/processed/extended_images/Amostrairradiada_03_0,7Gy_3x3.png',
        '1.0 Gy': './data/processed/extended_images/Amostrairradiada_02_1Gy_3x3.png'
    }

    # Metadados: Fator de conversão (nm por pixel) baseado na largura da imagem
    CONVERSION_FACTORS = {
        256: 11.72,
        258: 11.63,
        512: 5.86,
        514: 5.79,
        1024: 2.93
    }
    
    # --- Inicialização dos Objetos ---
    loader = Loader()
    analyzer = Analyzer()
    visualizer = Visualizer()
    
    # --- Processamento ---
    all_results = []

    for dose, image_path in IMAGE_PATHS.items():
        print(f"Processando amostra da dose: {dose}...")
        
        if not os.path.exists(image_path):
            print(f"  AVISO: Arquivo não encontrado em '{image_path}'. Pulando esta dose.")
            continue

        image = loader.load_grayscale(image_path)
        if image is None: continue

        # Determina o fator de conversão a partir da largura da imagem
        width = image.shape[1]
        conversion_factor = CONVERSION_FACTORS.get(width)
        if conversion_factor is None:
            print(f"  ERRO: Fator de conversão não encontrado para a resolução {width}px. Pulando dose.")
            continue

        # Executa a nova pipeline de quantificação, passando o fator de conversão
        results = analyzer.run_skeleton_quantification_pipeline(image, conversion_factor)
        
        all_results.append({
            'Dose': dose,
            'Comprimento Esquelético': results['comprimento_esqueletico_nm']
        })
    
    # --- Relatório Final ---
    if not all_results:
        print("\nNenhuma imagem foi processada com sucesso.")
        return

    print("\n--- Resultados Numéricos Finais ---")
    for r in all_results:
        print(f"Dose: {r['Dose']}, Comprimento Esquelético: {r['Comprimento Esquelético']:.2f} nm")

    # Gera o gráfico final
    visualizer.plot_skeleton_length_vs_dose(all_results, output_dir=OUTPUT_DIR)

if __name__ == "__main__":
    run_skeleton_length_analysis()