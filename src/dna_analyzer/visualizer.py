# src/dna_analyzer/visualizer.py
import cv2
import matplotlib.pyplot as plt
import os
import numpy as np

class Visualizer:
    """Classe para criar visualizações dos resultados da análise."""

    def __init__(self, dna_color_cv=(255, 0, 0), rna_color_cv=(0, 255, 0), thickness=1):
        """
        Define atributos de cor separados para OpenCV e Matplotlib.
        """
        # Cores para OpenCV (formato BGR, 0-255)
        self.cv2_dna_color = dna_color_cv # Azul para DNA
        self.cv2_rna_color = rna_color_cv # Verde para RNA

        # Cores para Matplotlib (nomes em texto)
        self.plt_dna_color = 'blue'
        self.plt_rna_color = 'green'
        
        self.thickness = thickness

    def draw_classified_contours(self, base_image, dna_contours, rna_contours):
        """
        Desenha os contornos classificados em imagens separadas.

        Returns:
            tuple: Uma tupla contendo a imagem com contornos de DNA e a com de RNA.
        """
        dna_image = cv2.cvtColor(base_image, cv2.COLOR_GRAY2BGR)
        rna_image = dna_image.copy() # Usamos a mesma base para a imagem de RNA

        cv2.drawContours(dna_image, dna_contours, -1, self.cv2_dna_color, self.thickness)
        cv2.drawContours(rna_image, rna_contours, -1, self.cv2_rna_color, self.thickness)
        
        return dna_image, rna_image
    

    def plot_edge_comparison(self, original_image, edge_results: dict, save_path: str = None, show_plot: bool = True):
        """
        Mostra uma figura com a imagem original e os resultados dos algoritmos de borda.

        Args:
            original_image (numpy.ndarray): A imagem original.
            edge_results (dict): Dicionário com os nomes dos algoritmos e suas imagens de resultado.
        """
        num_plots = len(edge_results) + 1
        plt.figure(figsize=(12, 8))

        # Plot da imagem original
        plt.subplot(2, 3, 1)
        plt.imshow(original_image, cmap='gray')
        plt.title('Original')
        plt.axis('off')

        # Plot dos resultados
        for i, (name, image) in enumerate(edge_results.items()):
            plt.subplot(2, 3, i + 2)
            plt.imshow(image, cmap='gray')
            plt.title(name.capitalize())
            plt.axis('off')

        plt.tight_layout()
        
        # Se um caminho de salvamento for fornecido, salva o gráfico
        if save_path:
            # Garante que o diretório de destino exista
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            # Salva a figura com boa resolução
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico de comparação salvo em: {save_path}")

        # Exibe o gráfico se solicitado
        if show_plot:
            plt.show()
        
        # Fecha a figura para liberar memória
        plt.close()

    def plot_dose_response(self, results: list, output_dir: str):
        """
        Gera e salva gráficos de dose-resposta para fragmentos e perímetros.

        Args:
            results (list): Uma lista de dicionários, cada um contendo os resultados e a 'Dose'.
            output_dir (str): O diretório onde os gráficos serão salvos.
        """
        if not results:
            print("Atenção: Lista de resultados vazia. Nenhum gráfico gerado.")
            return

        os.makedirs(output_dir, exist_ok=True)

        doses = [r['Dose'] for r in results]
        rna_fragments = [r['Num RNA'] for r in results]
        dna_fragments = [r['Num DNA'] for r in results]
        rna_perimeters = [r['Perímetro RNA'] for r in results]
        dna_perimeters = [r['Perímetro DNA'] for r in results]

        # Gráfico 1: Número de Fragmentos
        plt.figure(figsize=(12, 6))
        plt.plot(doses, rna_fragments, 'o-', label='Fragmentos de RNA', color=self.plt_rna_color)
        plt.plot(doses, dna_fragments, 'o-', label='Fragmentos de DNA', color=self.plt_dna_color)
        plt.title('Número de Fragmentos Detectados por Dose')
        plt.xlabel('Dose (Gy)')
        plt.ylabel('Número de Fragmentos')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'grafico_fragmentos_vs_dose.png'))
        plt.close()

        # Gráfico 2: Soma dos Perímetros
        plt.figure(figsize=(12, 6))
        plt.plot(doses, rna_perimeters, 'o-', label='Perímetro Total de RNA', color=self.plt_rna_color)
        plt.plot(doses, dna_perimeters, 'o-', label='Perímetro Total de DNA', color=self.plt_dna_color)
        plt.title('Soma dos Perímetros Detectados por Dose')
        plt.xlabel('Dose (Gy)')
        plt.ylabel('Soma dos Perímetros')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'grafico_perimetro_vs_dose.png'))
        plt.close()

        print(f"Gráficos de dose-resposta salvos em: {output_dir}")

    def plot_classified_image_pair(self, dna_image, rna_image, title_prefix=""):
        """
        Exibe um gráfico com duas imagens lado a lado (DNA e RNA).

        Args:
            dna_image (np.ndarray): Imagem com contornos de DNA.
            rna_image (np.ndarray): Imagem com contornos de RNA.
            title_prefix (str): Um prefixo para os títulos dos subplots.
        """
        plt.figure(figsize=(12, 6))
        
        # Subplot para DNA
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.cvtColor(dna_image, cv2.COLOR_BGR2RGB))
        plt.title(f'DNA - {title_prefix}')
        plt.axis('off')

        # Subplot para RNA
        plt.subplot(1, 2, 2)
        plt.imshow(cv2.cvtColor(rna_image, cv2.COLOR_BGR2RGB))
        plt.title(f'RNA - {title_prefix}')
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()

    def plot_skeleton_overlay(self, original_image, skeleton_image, dose_label="", thicken_kernel_size=(2, 2)):
        """
        Cria uma sobreposição do esqueleto na imagem original e exibe um gráfico comparativo.
        """
        # Engrossa o esqueleto para melhor visualização
        if thicken_kernel_size:
            kernel = np.ones(thicken_kernel_size, np.uint8)
            skeleton_image = cv2.dilate(skeleton_image, kernel, iterations=1)

        # Cria uma imagem colorida e sobrepõe o esqueleto em vermelho
        overlay = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
        overlay[skeleton_image > 0] = [0, 0, 255]  # Esqueleto em Vermelho (BGR)

        # Exibe os resultados
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(original_image, cmap='gray')
        plt.title(f'Imagem Original - {dose_label}')
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)) # Converte para RGB para Matplotlib
        plt.title(f'Esqueleto Sobreposto - {dose_label}')
        plt.axis('off')

        plt.tight_layout()
        plt.show()

    def plot_skeleton_length_vs_dose(self, results: list, output_dir: str):
        """
        Plota o gráfico de Comprimento Esquelético por Dose e o salva em arquivo.

        Args:
            results (list): Lista de dicionários com 'Dose' e 'Comprimento Esquelético'.
            output_dir (str): Diretório para salvar o gráfico.
        """
        if not results:
            print("Atenção: Lista de resultados vazia. Nenhum gráfico gerado.")
            return

        os.makedirs(output_dir, exist_ok=True)
        
        doses = [r['Dose'] for r in results]
        skeleton_lengths = [r['Comprimento Esquelético'] for r in results]

        plt.figure(figsize=(12, 6))
        plt.plot(doses, skeleton_lengths, 'o-', label='Comprimento Esquelético', color='red', markersize=8)
        plt.title('Comprimento Esquelético por Dose')
        plt.xlabel('Dose (Gy)')
        plt.ylabel('Comprimento Esquelético (nm)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'grafico_comprimento_vs_dose.png'))
        plt.close()

        print(f"Gráfico de comprimento vs. dose salvo em: {output_dir}")