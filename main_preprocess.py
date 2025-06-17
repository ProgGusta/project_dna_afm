# main_preprocess.py
# Este script utiliza as classes do pacote dna_analyzer para executar uma tarefa de PRÉ-PROCESSAMENTO.
import os
from src.dna_analyzer import (
    Loader,
    Saver,
    ImagePreprocessor
)

def run_preprocessing_task():
    # --- Configuração ---
    INPUT_DIR = './data/raw'
    OUTPUT_DIR = './data/processed/extended_images'
    TARGET_SIZE = 512

    # --- Inicialização dos Objetos ---
    loader = Loader()
    preprocessor = ImagePreprocessor(target_size=TARGET_SIZE)
    saver = Saver(output_directory=OUTPUT_DIR)

    # --- Processamento ---
    image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for filename in image_files:
        print(f"Processando: {filename}")
        image_path = os.path.join(INPUT_DIR, filename)

        # 1. Carrega a imagem colorida
        original_image = loader.load_color(image_path)
        if original_image is None:
            continue

        # 2. Usa o preprocessor para normalizar a imagem
        processed_image = preprocessor.normalize_size_with_blur_padding(original_image)
        
        # 3. Salva a imagem resultante
        saver.save_image(processed_image, filename)
        
        print(f'Tamanho final da imagem {filename}: {processed_image.shape[1]}x{processed_image.shape[0]}')

    print("\nPré-processamento de imagens concluído.")

if __name__ == "__main__":
    run_preprocessing_task()