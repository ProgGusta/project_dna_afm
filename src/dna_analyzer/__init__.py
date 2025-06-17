# src/dna_analyzer/__init__.py

# Importa as classes principais de cada módulo para o nível do pacote.
# Isso permite que os usuários importem diretamente do pacote 'dna_analyzer'
# em vez de precisar saber a estrutura interna dos arquivos.

from .loader import Loader
from .saver import Saver
from .preprocessor import ImagePreprocessor
from .segmenter import Segmenter
from .feature_extractor import FeatureExtractor
from .stats_calculator import StatsCalculator
from .visualizer import Visualizer
from .analyzer import Analyzer

# Definir a variável __all__ para controlar 'from dna_analyzer import *'
__all__ = [
    'Loader',
    'Saver',
    'ImagePreprocessor',
    'Segmenter',
    'FeatureExtractor',
    'StatsCalculator',
    'Visualizer',
    'Analyzer',
]

# Definir a versão do pacote
__version__ = "1.0.0"