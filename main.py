# main.py
import argparse
from dna_analyzer import (
    run_dose_response_pipeline,
    run_skeleton_analysis_pipeline,
    run_comparison_pipeline,
    run_preprocessing_task_pipeline,
    run_skeleton_length_analysis_pipeline,
    run_visualization_per_dose_pipeline,
    run_analysis_pipeline,
    run_full_skeleton_analysis_pipeline
)

# Mapeia os nomes amigáveis das pipelines para as funções que as executam
PIPELINES = {
    "dose-response": run_dose_response_pipeline,
    "skeleton-viz": run_skeleton_analysis_pipeline,
    "compare-edges": run_comparison_pipeline,
    "preprocess": run_preprocessing_task_pipeline,
    "skeleton-length": run_skeleton_length_analysis_pipeline,
    "visualization-per-dose": run_visualization_per_dose_pipeline,
    "analysis": run_analysis_pipeline,
    "full-skeleton-analysis": run_full_skeleton_analysis_pipeline
}

def main():
    # --- Configuração do argparse ---
    parser = argparse.ArgumentParser(
        description="DNA Analyzer: Ferramenta para análise de imagens de AFM de DNA.",
        formatter_class=argparse.RawTextHelpFormatter # Melhora a formatação da ajuda
    )
    
    parser.add_argument(
        "pipeline",
        help="O nome da pipeline de análise a ser executada.",
        choices=PIPELINES.keys() # Restringe as escolhas às chaves do nosso dicionário
    )
    
    args = parser.parse_args()
    
    # --- Execução da pipeline escolhida ---
    selected_pipeline_func = PIPELINES.get(args.pipeline)
    
    if selected_pipeline_func:
        selected_pipeline_func()
    else:
        print(f"Erro: Pipeline '{args.pipeline}' não encontrada.")

if __name__ == "__main__":
    main()