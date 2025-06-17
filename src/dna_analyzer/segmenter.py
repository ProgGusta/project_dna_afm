# src/dna_analyzer/segmenter.py
import cv2
import numpy as np

class Segmenter:
    """Classe para segmentar moléculas em uma imagem usando detecção de bordas."""

    def __init__(self, canny_threshold1: int = 100, canny_threshold2: int = 200):
        """
        Inicializa o segmentador com os limiares do Canny.
        """
        self.canny_threshold1 = canny_threshold1
        self.canny_threshold2 = canny_threshold2

    def segment(self, image):
        """
        Aplica o detector de bordas Canny e encontra os contornos.

        Args:
            image (numpy.ndarray): A imagem de entrada em escala de cinza.

        Returns:
            tuple: Uma tupla contendo a lista de contornos e a imagem de bordas.
        """
        edges = cv2.Canny(image, self.canny_threshold1, self.canny_threshold2)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours, edges

    def detect_canny_edges(self, image):
        """Aplica o detector de bordas Canny e retorna apenas a imagem de bordas."""
        return cv2.Canny(image, self.canny_threshold1, self.canny_threshold2)

    def detect_sobel(self, image, ksize=3):
        """Aplica o operador Sobel."""
        sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
        sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)
        return cv2.magnitude(sobelx, sobely).astype(np.uint8)

    def detect_laplacian(self, image, ksize=3):
        """Aplica o operador Laplaciano."""
        laplacian = cv2.Laplacian(image, cv2.CV_64F, ksize=ksize)
        return cv2.convertScaleAbs(laplacian)

    def detect_prewitt(self, image):
        """Aplica o operador Prewitt."""
        kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
        kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
        prewittx = cv2.filter2D(image, -1, kernelx)
        prewitty = cv2.filter2D(image, -1, kernely)
        return cv2.magnitude(prewittx.astype(np.float32), prewitty.astype(np.float32)).astype(np.uint8)

    def detect_all_edges(self, image):
        """
        Executa todos os detectores de borda e retorna um dicionário com os resultados.
        """
        return {
            "canny": self.detect_canny_edges(image),
            "sobel": self.detect_sobel(image),
            "laplacian": self.detect_laplacian(image),
            "prewitt": self.detect_prewitt(image)
        }
    
    def segment_with_adaptive_threshold(self, image, block_size=11, C=2, cleanup_kernel_size=(2, 2)):
        """
        Segmenta a imagem usando limiar adaptativo e faz uma limpeza morfológica.
        Retorna uma imagem binária.
        """
        # Aplica limiar adaptativo para binarizar a imagem
        binary_image = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, block_size, C
        )

        # Remove pequenos ruídos com uma operação de abertura morfológica
        if cleanup_kernel_size:
            kernel = np.ones(cleanup_kernel_size, np.uint8)
            clean_binary = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
            return clean_binary
        
        return binary_image