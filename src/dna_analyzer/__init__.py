# src/dna_analyzer/__init__.py

# Importa as classes dos módulos principais
from .preprocessor import ImagePreprocessor
from .segmenter import Segmenter
from .feature_extractor import FeatureExtractor
from .stats_calculator import StatsCalculator
from .visualizer import Visualizer
from .analyzer import Analyzer

# Importa as classes do submódulo de IO
from .io import Loader, Saver

# Importa as funções de pipeline para serem usadas pelo main.py
from .pipelines import (
    run_dose_response_pipeline,
    run_skeleton_analysis_pipeline,
    run_comparison_pipeline,
    run_preprocessing_task_pipeline,
    run_skeleton_length_analysis_pipeline,
    run_visualization_per_dose_pipeline,
    run_analysis_pipeline,
    run_full_skeleton_analysis_pipeline
)

__all__ = [
    'Loader', 'Saver', 'ImagePreprocessor', 'Segmenter', 'FeatureExtractor',
    'StatsCalculator', 'Visualizer', 'Analyzer', 'run_dose_response_pipeline',
    'run_skeleton_analysis_pipeline', 'run_comparison_pipeline',
    'run_preprocessing_task_pipeline', 'run_skeleton_length_analysis_pipeline',
    'run_visualization_per_dose_pipeline', 'run_analysis_pipeline',
    'run_full_skeleton_analysis_pipeline'
]

__version__ = "2.0.0" # Versão atualizada