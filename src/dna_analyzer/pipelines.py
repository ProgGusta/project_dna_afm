# src/dna_analyzer/pipelines.py
import os
import glob
import pandas as pd
from .io import Loader, Saver
from .analyzer import Analyzer
from .visualizer import Visualizer
from .segmenter import Segmenter
from .preprocessor import ImagePreprocessor
from .stats_calculator import StatsCalculator


def run_dose_response_pipeline():
    """Executa a análise de dose-resposta e gera os gráficos."""
    print("Executando a pipeline de Análise de Dose-Resposta...")

    # --- Configuração ---
    INPUT_DIR = './data/processed/extended_images'  # Diretório principal com todas as imagens
    OUTPUT_DIR = './results/dose_response'

    # Dicionário mapeando a dose para um padrão de nome de arquivo
    DOSE_PATTERNS = {
        'Sem Irradiar': '*sample_segmentation*.png',
        '0.4 Gy': '*0,4 Gy*.png',
        '0.7 Gy': '*0,7Gy*.png',
        '1.0 Gy': '*1Gy*.png'
    }

    ANALYZER_CONFIG = {
        'segmenter': {'canny_threshold1': 100, 'canny_threshold2': 200},
        'extractor': {'circularity_threshold': 0.8}
    }

    # --- Lógica ---
    loader, analyzer, visualizer, saver = Loader(), Analyzer(config=ANALYZER_CONFIG), Visualizer(), Saver(OUTPUT_DIR)

    # --- Processamento ---
    all_individual_results = []

    # Itera sobre cada dose e seu padrão
    for dose, pattern in DOSE_PATTERNS.items():
        # Usa glob para encontrar todos os arquivos que correspondem ao padrão no diretório de entrada
        image_paths = glob.glob(os.path.join(INPUT_DIR, pattern))
        
        if not image_paths:
            print(f"  Aviso: Nenhuma imagem encontrada para a dose '{dose}' com o padrão '{pattern}'")
            continue
            
        print(f"  Encontradas {len(image_paths)} imagens para a dose: {dose}")

        # Itera sobre cada imagem encontrada para a dose atual
        for image_path in image_paths:
            image = loader.load_grayscale(image_path)
            if image is None: continue
            
            results = analyzer.process(image)
            current_result = results["statistics"]
            current_result['Dose'] = dose
            current_result['Arquivo'] = os.path.basename(image_path) # Adiciona o nome do arquivo para rastreabilidade
            all_individual_results.append(current_result)

    if not all_individual_results:
        print("Nenhuma imagem foi processada. Encerrando pipeline.")
        return

    # --- Agregação e Salvamento dos Resultados ---
    # Converte a lista de resultados individuais em um DataFrame do Pandas
    df_individual = pd.DataFrame(all_individual_results)
    saver.save_dataframe(df_individual, "resultados_individuais_por_arquivo.csv")

    # Usa groupby para agregar os resultados por dose (calculando média e desvio padrão)
    # Seleciona apenas colunas numéricas para as operações de agregação
    numeric_cols = df_individual.select_dtypes(include=['number']).columns
    df_aggregated = df_individual.groupby('Dose')[numeric_cols].agg(['mean', 'std']).round(2)
    saver.save_dataframe(df_aggregated, "resultados_agregados_por_dose.csv")

    print("\n--- Resultados Agregados por Dose (Média) ---")
    print(df_aggregated)
    
    # --- Visualização dos Resultados Agregados ---
    # Prepara os dados para o visualizer, usando a média dos resultados
    df_mean = df_aggregated.xs('mean', axis=1, level=1).reset_index()
    results_for_plot = df_mean.to_dict('records')
    
    visualizer = Visualizer()
    visualizer.plot_dose_response(results_for_plot, output_dir=OUTPUT_DIR)
    
    print("Pipeline de Análise de Dose-Resposta concluída.")

def run_skeleton_analysis_pipeline():
    """Executa a análise de esqueletização e visualiza os resultados."""
    print("Executando a pipeline de Visualização de Esqueleto...")

    # --- Configuração ---
    INPUT_DIR = './data/processed/extended_images'  # Diretório principal com todas as imagens

    # Dicionário mapeando a dose para um padrão de nome de arquivo
    DOSE_PATTERNS = {
        'Sem Irradiar': '*sample_segmentation*.png',
        '0.4 Gy': '*0,4 Gy*.png',
        '0.7 Gy': '*0,7Gy*.png',
        '1.0 Gy': '*1Gy*.png'
    }

    # --- Lógica ---
    loader, analyzer, visualizer = Loader(), Analyzer(), Visualizer()

    for dose, pattern in DOSE_PATTERNS.items():
        # Usa glob para encontrar todos os arquivos que correspondem ao padrão no diretório de entrada
        image_paths = glob.glob(os.path.join(INPUT_DIR, pattern))
        print(f"  Analisando {len(image_paths)} imagens para a dose: {dose}")

        for image_path in image_paths:
            # Carrega a imagem em escala de cinza
            image = loader.load_grayscale(image_path)
            if image is None: continue

            # Executa a análise de esqueleto
            results = analyzer.run_skeleton_pipeline(image)

            visualizer.plot_skeleton_overlay(
                original_image=results['original'],
                skeleton_image=results['skeleton'],
                dose_label=f"{dose} - {os.path.basename(image_path)}"
            )

    print("Pipeline de Visualização de Esqueleto concluída.")

def run_comparison_pipeline():
    """Executa a comparação de algoritmos de detecção de borda."""
    print("Executando a pipeline de Comparação de Algoritmos...")

    # --- Configuração ---
    INPUT_DIR = './data/processed/extended_images'  # Diretório de entrada
    OUTPUT_DIR = './results/figures/compare_methods'  # Nome da pasta de saída

    # --- Lógica ---
    loader, segmenter, visualizer, saver = Loader(), Segmenter(canny_threshold1=50, canny_threshold2=150), Visualizer(), Saver(OUTPUT_DIR)

    image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]


    for filename in image_files:
        image_path = os.path.join(INPUT_DIR, filename)

        original_image = loader.load_grayscale(image_path)
        if original_image is None: continue

        # 1. Obter todos os resultados de detecção de borda
        edge_results = segmenter.detect_all_edges(original_image)

        # 2. Salvar cada imagem de resultado separadamente
        base_name = os.path.splitext(filename)[0]
        for algo_name, result_image in edge_results.items():
            # A classe Saver já adiciona o OUTPUT_DIR, então passamos apenas o nome do arquivo
            saver.save_image(result_image, f"{base_name}_{algo_name}.png")

        # 3. Salvar e exibir a imagem de comparação completa
        # Salva e exibe a imagem de comparação completa
        comparison_save_path = os.path.join(OUTPUT_DIR, f"{base_name}_comparison.png")

        # Chama o método do Visualizer para criar, salvar e exibir o gráfico
        visualizer.plot_edge_comparison(
            original_image, 
            edge_results, 
            save_path=comparison_save_path, 
            show_plot=True
        )

        # Opcional: break para rodar para apenas uma imagem
        # break

    print("Pipeline de Comparação de Algoritmos concluída.")

def run_preprocessing_task_pipeline():
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

def run_skeleton_length_analysis_pipeline():
    # --- Configuração ---
    INPUT_DIR = './data/processed/extended_images'  # Diretório principal com todas as imagens
    OUTPUT_DIR = './results/figures/skeleton_length/'  # Nome da pasta de saída para os gráficos

    # Dicionário mapeando a dose para um padrão de nome de arquivo
    DOSE_PATTERNS = {
        'Sem Irradiar': '*sample_segmentation*.png',
        '0.4 Gy': '*0,4 Gy*.png',
        '0.7 Gy': '*0,7Gy*.png',
        '1.0 Gy': '*1Gy*.png'
    }

    # Metadados: Fator de conversão (nm por pixel) baseado na largura da imagem
    CONVERSION_FACTORS = {
        256: 11.72,
        258: 11.63,
        512: 5.86,
        514: 5.79,
        1024: 2.93
    }
    
    # --- Inicialização dos Objetos ---
    loader = Loader()
    analyzer = Analyzer()
    visualizer = Visualizer()
    
    # --- Processamento ---
    all_results = []

    for dose, pattern in DOSE_PATTERNS.items():
        # Usa glob para encontrar todos os arquivos que correspondem ao padrão no diretório de entrada
        image_paths = glob.glob(os.path.join(INPUT_DIR, pattern))
        print(f"Processando amostra da dose: {dose}...")

        for image_path in image_paths:
            image = loader.load_grayscale(image_path)
            if image is None: continue

            # Determina o fator de conversão a partir da largura da imagem
            width = image.shape[1]
            conversion_factor = CONVERSION_FACTORS.get(width)
            if conversion_factor is None:
                print(f"  ERRO: Fator de conversão não encontrado para a resolução {width}px. Pulando dose.")
                continue

            # Executa a nova pipeline de quantificação, passando o fator de conversão
            results = analyzer.run_skeleton_quantification_pipeline(image, conversion_factor)
            
            all_results.append({
                'Dose': dose,
                'Comprimento Esquelético': results['comprimento_esqueletico_nm']
            })
    
    # --- Relatório Final ---
    if not all_results:
        print("\nNenhuma imagem foi processada com sucesso.")
        return

    print("\n--- Resultados Numéricos Finais ---")
    for r in all_results:
        print(f"Dose: {r['Dose']}, Comprimento Esquelético: {r['Comprimento Esquelético']:.2f} nm")

    # Gera o gráfico final
    visualizer.plot_skeleton_length_vs_dose(all_results, output_dir=OUTPUT_DIR)

def run_visualization_per_dose_pipeline():
    # --- Configuração ---
    INPUT_DIR = './data/processed/extended_images'  # Diretório principal com todas as imagens

    # Dicionário mapeando a dose para um padrão de nome de arquivo
    DOSE_PATTERNS = {
        'Sem Irradiar': '*sample_segmentation*.png',
        '0.4 Gy': '*0,4 Gy*.png',
        '0.7 Gy': '*0,7Gy*.png',
        '1.0 Gy': '*1Gy*.png'
    }

    ANALYZER_CONFIG = {
        'segmenter': {'canny_threshold1': 100, 'canny_threshold2': 200},
        'extractor': {'circularity_threshold': 0.8}
    }

    # --- Inicialização dos Objetos ---
    loader = Loader()
    analyzer = Analyzer(config=ANALYZER_CONFIG)
    visualizer = Visualizer()
    
    # --- Processamento e Visualização ---
    all_results = []

    # Itera sobre cada dose e seu padrão
    for dose, pattern in DOSE_PATTERNS.items():
        # Usa glob para encontrar todos os arquivos que correspondem ao padrão no diretório de entrada
        image_paths = glob.glob(os.path.join(INPUT_DIR, pattern))
        
        if not image_paths:
            print(f"  Aviso: Nenhuma imagem encontrada para a dose '{dose}' com o padrão '{pattern}'")
            continue
            
        print(f"  Encontradas {len(image_paths)} imagens para a dose: {dose}")

        # Itera sobre cada imagem encontrada para a dose atual
        for image_path in image_paths:

            image = loader.load_grayscale(image_path)
            if image is None:
                continue

            # A classe Analyzer já faz todo o processamento e retorna tudo o que precisamos
            results = analyzer.process(image)
            
            # Adiciona a informação da dose e armazena
            current_stats = results["statistics"]
            current_stats['Dose'] = dose
            all_results.append(current_stats)

            # Usa o novo método do Visualizer para exibir o par de imagens (DNA/RNA)
            visualizer.plot_classified_image_pair(
                dna_image=results["dna_image"], 
                rna_image=results["rna_image"],
                title_prefix=dose
            )

    # --- Relatório Final no Console ---
    if not all_results:
        print("\nNenhuma imagem foi processada com sucesso.")
        return

    print("\n--- Resultados Numéricos Finais ---")
    for result in all_results:
        print(f"Dose: {result['Dose']}")
        print(f"  Número de fragmentos de DNA detectados: {result['Num DNA']}")
        print(f"  Soma total dos perímetros de DNA: {result['Perímetro DNA']:.2f}")
        print(f"  Número de fragmentos de RNA detectados: {result['Num RNA']}")
        print(f"  Soma total dos perímetros de RNA: {result['Perímetro RNA']:.2f}\n")

def run_analysis_pipeline():
    # --- Configuração ---
    INPUT_DIR = './data/processed/extended_images'  # Diretório de entrada
    OUTPUT_DIR = './results/statistics/perimeters'  # Nome da pasta de saída

    ANALYZER_CONFIG = {
        'segmenter': {'canny_threshold1': 100, 'canny_threshold2': 200},
        'extractor': {'circularity_threshold': 0.8}
    }

    # --- Inicialização dos Objetos ---
    loader = Loader()
    analyzer = Analyzer(config=ANALYZER_CONFIG)
    saver = Saver(output_directory=OUTPUT_DIR)
    stats_calculator = StatsCalculator()

    # --- Processamento ---
    image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    all_stats = []

    for filename in image_files:
        print(f"Processando {filename}...")
        image_path = os.path.join(INPUT_DIR, filename)

        image = loader.load_grayscale(image_path)
        if image is None:
            continue

        results = analyzer.process(image)
        
        stats = results["statistics"]
        stats['Imagem'] = filename
        all_stats.append(stats)
        
        # Opcional: Salvar imagens individuais de DNA/RNA pode ser feito aqui se necessário
        # base_name = os.path.splitext(filename)[0]
        # saver.save_image(results["dna_image"], f"{base_name}_dna.png")
        # saver.save_image(results["rna_image"], f"{base_name}_rna.png")

    # --- Finalização e Geração de Relatórios ---
    if not all_stats:
        print("Nenhuma imagem processada. Encerrando.")
        return

    # 1. Criar e salvar o DataFrame de resultados por imagem (como antes)
    df_results = pd.DataFrame(all_stats)
    df_results = df_results[['Imagem', 'Num DNA', 'Perímetro DNA', 'Num RNA', 'Perímetro RNA']]
    saver.save_dataframe(df_results, "resultados_perimetros.csv")

    # 2. Calcular e salvar as estatísticas descritivas gerais
    print("\nCalculando estatísticas descritivas gerais...")
    df_descriptive_stats = stats_calculator.calculate_descriptive_stats(df_results)
    saver.save_dataframe(df_descriptive_stats, "estatisticas_descritivas_gerais.csv")
    
    print("\nAnálise e geração de estatísticas concluídas com sucesso.")