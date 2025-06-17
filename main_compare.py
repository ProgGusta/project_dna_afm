# main_compare.py
# Este script utiliza as classes do pacote dna_analyzer para executar uma tarefa de COMPARAÇÃO.
import os
from src.dna_analyzer import (
    Loader,
    Saver,
    Segmenter,
    Visualizer
)

def run_comparison_task():
    # --- Configuração ---
    INPUT_DIR = './data/processed/extended_images'  # Diretório de entrada
    OUTPUT_DIR = './results/figures/compare_methods'  # Nome da pasta de saída
    
    # --- Inicialização dos Objetos ---
    loader = Loader()
    segmenter = Segmenter(canny_threshold1=50, canny_threshold2=150)
    visualizer = Visualizer()
    saver = Saver(output_directory=OUTPUT_DIR)

    # --- Processamento ---
    image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for filename in image_files:
        print(f"Processando: {filename}")
        image_path = os.path.join(INPUT_DIR, filename)
        
        original_image = loader.load_grayscale(image_path)
        if original_image is None:
            continue

        # 1. Obter todos os resultados de detecção de borda
        edge_results = segmenter.detect_all_edges(original_image)

        # 2. Salvar cada imagem de resultado separadamente
        base_name = os.path.splitext(filename)[0]
        for algo_name, result_image in edge_results.items():
            # A classe Saver já adiciona o OUTPUT_DIR, então passamos apenas o nome do arquivo
            saver.save_image(result_image, f"{base_name}_{algo_name}.png")

        # 3. Salvar e exibir a imagem de comparação completa
        # Define o caminho completo para o arquivo de comparação
        comparison_save_path = os.path.join(OUTPUT_DIR, f"{base_name}_comparison.png")

        # Chama o método do Visualizer para criar, salvar e exibir o gráfico
        visualizer.plot_edge_comparison(
            original_image,
            edge_results,
            save_path=comparison_save_path,
            show_plot=True  # Mude para False se quiser apenas salvar os arquivos sem exibi-los
        )
        
        # Opcional: break para rodar para apenas uma imagem
        break
        
    print("\nProcesso de comparação concluído.")

if __name__ == "__main__":
    run_comparison_task()