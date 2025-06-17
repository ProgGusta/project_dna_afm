# src/dna_analyzer/saver.py
import cv2
import pandas as pd
import os

class Saver:
    """Classe para salvar os resultados da análise (imagens e CSV)."""

    def __init__(self, output_directory: str):
        self.output_dir = output_directory
        os.makedirs(self.output_dir, exist_ok=True)

    def save_image(self, image, filename: str):
        """Salva uma imagem no diretório de saída."""
        path = os.path.join(self.output_dir, filename)
        cv2.imwrite(path, image)

    def save_dataframe(self, dataframe, filename: str):
        """Salva um DataFrame pandas como CSV no diretório de saída."""
        path = os.path.join(self.output_dir, filename)
        dataframe.to_csv(path, index=False)
        print(f"Resultados salvos em: {path}")