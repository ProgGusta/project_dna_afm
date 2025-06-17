# src/dna_analyzer/preprocessor.py
import cv2
import numpy as np

class ImagePreprocessor:
    """
    Realiza tarefas de pré-processamento, como normalização de tamanho e preenchimento.
    """

    def __init__(self, target_size: int = 512, blur_ksize: int = 5):
        """
        Inicializa o pré-processador.

        Args:
            target_size (int): O tamanho alvo (altura e largura) para a imagem final.
            blur_ksize (int): O tamanho do kernel para o desfoque gaussiano (deve ser ímpar).
        """
        self.target_size = target_size
        if blur_ksize % 2 == 0:
            blur_ksize += 1 # Garante que o tamanho do kernel seja ímpar
        self.blur_ksize = blur_ksize

    def normalize_size_with_blur_padding(self, image):
        """
        Redimensiona uma imagem proporcionalmente e preenche as bordas para atingir
        o tamanho alvo. As bordas adicionadas são suavizadas.

        Args:
            image (numpy.ndarray): A imagem de entrada (colorida).

        Returns:
            numpy.ndarray: A imagem processada com o tamanho alvo.
        """
        h, w = image.shape[:2]

        # 1. Redimensiona proporcionalmente
        scale = min(self.target_size / h, self.target_size / w)
        new_width = int(w * scale)
        new_height = int(h * scale)
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

        # 2. Calcula o preenchimento (padding)
        top = (self.target_size - new_height) // 2
        bottom = self.target_size - new_height - top
        left = (self.target_size - new_width) // 2
        right = self.target_size - new_width - left

        # 3. Expande as bordas usando replicação
        extended_image = cv2.copyMakeBorder(
            resized_image, top, bottom, left, right, cv2.BORDER_REPLICATE
        )

        # 4. Aplica desfoque na imagem com bordas
        blur_image = cv2.GaussianBlur(
            extended_image, (self.blur_ksize, self.blur_ksize), sigmaX=0, sigmaY=0
        )

        # 5. Cria uma máscara para misturar a imagem original com a borrada
        mask = np.zeros_like(extended_image, dtype=np.float32)
        # A máscara é 1 na área da imagem original e 0 nas bordas
        cv2.rectangle(mask, (left, top), (left + new_width, top + new_height), (1, 1, 1), thickness=-1)

        # 6. Mistura a imagem nítida (centro) com a borrada (bordas)
        final_image = (
            extended_image.astype(np.float32) * mask + 
            blur_image.astype(np.float32) * (1 - mask)
        ).astype(np.uint8)

        return final_image
    
    def apply_gaussian_blur(self, image, ksize=(5, 5)):
        """
        Aplica um filtro GaussianBlur para suavizar a imagem e reduzir ruído.
        """
        return cv2.GaussianBlur(image, ksize, 0)