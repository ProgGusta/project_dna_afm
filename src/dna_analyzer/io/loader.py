# src/dna_analyzer/io/loader.py
import cv2

class Loader:
    """Classe responsável por carregar imagens do disco."""
    
    def load_grayscale(self, image_path: str):
        """
        Carrega uma imagem em escala de cinza a partir de um caminho.

        Args:
            image_path (str): O caminho para o arquivo de imagem.

        Returns:
            numpy.ndarray: A imagem carregada ou None se ocorrer um erro.
        """
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Erro: Não foi possível carregar a imagem em {image_path}")
        return image

    def load_color(self, image_path: str):
        """
        Carrega uma imagem colorida (BGR) a partir de um caminho.
        """
        image = cv2.imread(image_path)
        if image is None:
            print(f"Erro: Não foi possível carregar a imagem em {image_path}")
        return image