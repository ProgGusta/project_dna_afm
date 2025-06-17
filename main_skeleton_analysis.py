# main_skeleton_analysis.py
# Este script executa a análise de esqueletização usando o pacote dna_analyzer.
# Lembre-se de instalar: pip install opencv-contrib-python
import os
from src.dna_analyzer import (
    Loader,
    Visualizer,
    Analyzer
)

def run_skeleton_analysis():
    # --- Configuração ---
    # ATENÇÃO: Verifique se estes caminhos estão corretos para o seu ambiente.
    IMAGE_PATHS = {
        'Sem Irradiar': './data/processed/extended_images/sample_segmentation_17.png',
        '0.4 Gy': './data/processed/extended_images/Amostra 1_0,4 Gy 2023-10-18 15h17m27_3x3 (1).png',
        '0.7 Gy': './data/processed/extended_images/Amostrairradiada_03_0,7Gy_3x3.png',
        '1.0 Gy': './data/processed/extended_images/Amostrairradiada_02_1Gy_3x3.png'
    }

    # --- Inicialização dos Objetos ---
    loader = Loader()
    analyzer = Analyzer() # Usando configurações padrão
    visualizer = Visualizer()
    
    # --- Processamento e Visualização ---
    for dose, image_path in IMAGE_PATHS.items():
        print(f"Processando: {dose}")
        
        if not os.path.exists(image_path):
            print(f"  AVISO: Arquivo não encontrado em '{image_path}'. Pulando esta dose.")
            continue

        image = loader.load_grayscale(image_path)
        if image is None:
            continue

        # 1. Executa a nova pipeline de esqueletização
        results = analyzer.run_skeleton_pipeline(image)
        
        # 2. Usa o Visualizer para plotar o resultado
        visualizer.plot_skeleton_overlay(
            original_image=results['original'],
            skeleton_image=results['skeleton'],
            dose_label=dose
        )
        
if __name__ == "__main__":
    run_skeleton_analysis()