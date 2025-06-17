# src/dna_analyzer/feature_extractor.py
import cv2
import numpy as np

class FeatureExtractor:
    """Classe para extrair características e classificar contornos."""

    def __init__(self, circularity_threshold: float = 0.8):
        """
        Inicializa o extrator com o limiar de circularidade para classificar RNA.
        """
        self.circularity_threshold = circularity_threshold

    def extract_features(self, contours):
        """
        Classifica contornos e calcula estatísticas.

        Args:
            contours (list): A lista de contornos detectados.

        Returns:
            dict: Um dicionário contendo contornos classificados e estatísticas.
        """
        dna_contours = []
        rna_contours = []

        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)

            if perimeter == 0:
                continue

            circularity = 4 * np.pi * (area / (perimeter ** 2))
            if circularity > self.circularity_threshold:
                rna_contours.append(contour)
            else:
                dna_contours.append(contour)
        
        # Calcula as estatísticas
        dna_perimeters = [cv2.arcLength(c, True) for c in dna_contours]
        rna_perimeters = [cv2.arcLength(c, True) for c in rna_contours]

        stats = {
            'Num RNA': len(rna_contours),
            'Perímetro RNA': sum(rna_perimeters),
            'Num DNA': len(dna_contours),
            'Perímetro DNA': sum(dna_perimeters)
        }
        
        return {
            "dna_contours": dna_contours,
            "rna_contours": rna_contours,
            "statistics": stats
        }
    
    def extract_skeleton(self, binary_image):
        """
        Aplica o algoritmo de thinning para extrair o esqueleto de uma imagem binária.
        Requer opencv-contrib-python.
        """
        # O algoritmo de thinning espera pixels brancos (255) em fundo preto (0).
        return cv2.ximgproc.thinning(binary_image)
    
    def calculate_skeleton_length(self, skeleton_image, conversion_factor=1.0):
        """
        Calcula o comprimento de um esqueleto contando seus pixels e aplicando
        um fator de conversão.

        Args:
            skeleton_image (np.ndarray): A imagem binária do esqueleto.
            conversion_factor (float): Fator para converter pixels para uma unidade real (ex: nm).

        Returns:
            float: O comprimento total do esqueleto na unidade desejada.
        """
        pixel_count = np.sum(skeleton_image > 0)
        return pixel_count * conversion_factor