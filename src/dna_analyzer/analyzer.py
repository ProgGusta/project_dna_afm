# src/dna_analyzer/analyzer.py
from .segmenter import Segmenter
from .feature_extractor import FeatureExtractor
from .visualizer import Visualizer
from .preprocessor import ImagePreprocessor

class Analyzer:
    """
    Classe orquestradora que executa o pipeline de análise de imagem.
    """
    def __init__(self, config: dict = None):
        if config is None:
            config = {}
        
        # Instancia as classes de componentes, passando configurações se existirem
        self.preprocessor = ImagePreprocessor(**config.get('preprocessor', {}))
        self.segmenter = Segmenter(**config.get('segmenter', {}))
        self.extractor = FeatureExtractor(**config.get('extractor', {}))
        self.visualizer = Visualizer(**config.get('visualizer', {}))

    def process(self, image):
        """
        Processa uma única imagem através de todas as etapas.

        Args:
            image (numpy.ndarray): A imagem de entrada.

        Returns:
            dict: Um dicionário com os resultados, incluindo estatísticas e imagens.
        """
        # Etapa 1: Segmentação
        contours, edges = self.segmenter.segment(image)

        # Etapa 2: Extração de Características
        features = self.extractor.extract_features(contours)
        
        # Etapa 3: Visualização
        dna_image, rna_image = self.visualizer.draw_classified_contours(
            edges, 
            features["dna_contours"], 
            features["rna_contours"]
        )

        return {
            "statistics": features["statistics"],
            "dna_image": dna_image,
            "rna_image": rna_image
        }

    def run_skeleton_pipeline(self, image):
        """
        Executa a pipeline de pré-processamento, segmentação e esqueletização.
        """
        # 1. Pré-processamento
        blurred_image = self.preprocessor.apply_gaussian_blur(image)
        
        # 2. Segmentação
        binary_image = self.segmenter.segment_with_adaptive_threshold(blurred_image)
        
        # 3. Extração de Característica (Esqueleto)
        skeleton = self.extractor.extract_skeleton(binary_image)
        
        return {
            'original': image,
            'skeleton': skeleton
        }

    def run_skeleton_quantification_pipeline(self, image, conversion_factor=1.0):
        """
        Executa a pipeline completa para QUANTIFICAR o comprimento do esqueleto.
        """
        # 1. Pré-processamento
        blurred_image = self.preprocessor.apply_gaussian_blur(image)
        
        # 2. Segmentação
        # Usamos um kernel menor para limpeza, conforme o script original
        binary_image = self.segmenter.segment_with_adaptive_threshold(
            blurred_image, cleanup_kernel_size=(1, 1)
        )
        
        # 3. Extração do Esqueleto
        skeleton = self.extractor.extract_skeleton(binary_image)
        
        # 4. Cálculo da Característica (Comprimento)
        length = self.extractor.calculate_skeleton_length(skeleton, conversion_factor)
        
        return {
            'comprimento_esqueletico_nm': length
        }