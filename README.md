# Análise Computacional de Danos no DNA por Radiação Ionizante

## 📖 Sobre o Projeto

Este projeto desenvolve e implementa uma suíte de ferramentas computacionais em Python para analisar imagens de DNA plasmidial obtidas por Microscopia de Força Atômica (AFM). O objetivo principal é quantificar os danos estruturais no DNA após a exposição a diferentes doses de radiação ionizante, um problema de grande relevância na área de biofísica e medicina, especialmente em contextos de diagnóstico e tratamento de câncer.

A radiação ionizante, embora fundamental em terapias médicas, afeta tanto células cancerígenas quanto sadias. Compreender a correlação entre a dose de radiação e o nível de dano ao DNA é crucial. Utilizando técnicas de processamento de imagem e segmentação, como detecção de bordas, esqueletização e classificação de contornos, este projeto visa automatizar a análise e fornecer dados quantitativos sobre a fragmentação e as alterações morfológicas do DNA.

### Objetivos Principais

* **Desenvolver rotinas computacionais** para pré-processar e segmentar imagens de AFM de DNA.
* **Implementar diferentes técnicas de análise**, como classificação de fragmentos (DNA/RNA) e extração de esqueleto molecular.
* **Quantificar os danos no DNA**, medindo características como número de fragmentos e comprimento total das moléculas.
* **Correlacionar os danos quantificados com a dose de radiação** recebida, gerando gráficos e relatórios estatísticos.

---

## 📂 Estrutura de Arquivos

O projeto é organizado de forma modular para garantir manutenibilidade, escalabilidade e clareza.

```
projeto_dna_afm/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── skeleton.ipynb
├── results/
│   ├── figures/
│   └── statistics/
├── src/
│   └── dna_analyzer/
│       ├── __init__.py
│       ├── io/
│       │   ├── __init__.py
│       │   ├── loader.py
│       │   └── saver.py
│       ├── pipelines.py
│       ├── analyzer.py
│       ├── preprocessor.py
│       ├── segmenter.py
│       ├── feature_extractor.py
│       ├── stats_calculator.py
│       └── visualizer.py
├── main.py
├── .gitignore
├── pyproject.toml
└── README.md
```

* **`src/dna_analyzer/`**: Contém todo o código-fonte do pacote Python. Cada módulo encapsula uma parte da lógica (pré-processamento, segmentação, visualização, etc.).
* **`data/`**: Pasta para armazenar as imagens de AFM. **Esta pasta é ignorada pelo Git** (via `.gitignore`) e deve ser criada manualmente.
    * `raw/`: Para as imagens originais, intocadas.
    * `processed/`: Para imagens após etapas de pré-processamento.
* **`results/`**: Armazena todas as saídas geradas pelos scripts, como imagens processadas, gráficos e arquivos CSV com estatísticas. **Também ignorada pelo Git**.
* **`notebooks/`**: Para Jupyter Notebooks utilizados em análises exploratórias e testes de algoritmos.
* **`main_*.py`**:  Ponto de entrada único e centralizado para executar todas as análises disponíveis no projeto.
* **`pyproject.toml`**: Arquivo de configuração do projeto que define metadados e, mais importante, as dependências necessárias para executá-lo.
* **`.gitignore`**: Especifica quais arquivos e pastas devem ser ignorados pelo Git.
* **`README.md`**: Este arquivo de documentação.

---

## Instalação e Configuração

Siga os passos abaixo para configurar o ambiente e executar o projeto.

### Pré-requisitos
* Python 3.8 ou superior
* Git

### 1. Clonar o Repositório
Abra um terminal e clone o projeto para a sua máquina local:
```bash
git clone https://github.com/ProgGusta/project_dna_afm.git
cd projeto_dna_afm
```

### 2. Criar e Ativar um Ambiente Virtual
É uma prática altamente recomendada usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual (uma pasta chamada 'venv' será criada)
python -m venv venv
```

Agora, ative o ambiente. O comando varia conforme o seu sistema operacional:

* **No Windows (PowerShell/CMD):**
    ```bash
    .\venv\Scripts\activate
    ```

* **No macOS ou Linux:**
    ```bash
    source venv/bin/activate
    ```
Após a ativação, você verá `(venv)` no início do seu prompt de comando.

### 3. Instalar as Dependências
Todas as bibliotecas necessárias estão listadas no arquivo `pyproject.toml`. Instale-as com um único comando do Pip:

```bash
pip install -e .
```
* **Nota**: A flag `-e` instala o projeto em "modo editável", o que significa que as alterações que você fizer nos arquivos `.py` em `src/` serão refletidas imediatamente, sem a necessidade de reinstalar.

* **Dependência Especial**: Algumas análises (como a de esqueletização) requerem o pacote `opencv-contrib-python`. Garanta que ele esteja instalado:
    ```bash
    pip install opencv-contrib-python
    ```

---

## Como Executar

Todas as análises foram centralizadas em um único ponto de entrada, o script `main.py`. Para executar uma tarefa específica, você deve passar o nome da "pipeline" desejada como um argumento na linha de comando.

### Descobrindo as Pipelines Disponíveis

Para ver todas as pipelines disponíveis e uma breve descrição do programa, use a flag `-h` ou `--help`:

```bash
python main.py --help
```

A saída mostrará todas as `choices` (escolhas) disponíveis para a execução:
```
usage: main.py [-h] {dose-response,skeleton-viz,compare-edges,preprocess,skeleton-length,visualization-per-dose,analysis}

DNA Analyzer: Ferramenta para análise de imagens de AFM de DNA.

positional arguments:
  {dose-response,skeleton-viz,compare-edges,preprocess,skeleton-length,visualization-per-dose,analysis}
                        O nome da pipeline de análise a ser executada.

options:
  -h, --help            show this help message and exit
```

### Pipelines Disponíveis

* **`analysis`**: Executa a análise padrão em um diretório de imagens, gerando um CSV com as estatísticas de DNA/RNA por imagem e outro CSV com as estatísticas descritivas (média, mediana, etc.) do conjunto completo.

* **`preprocess`**: Pré-processa um diretório de imagens, normalizando seus tamanhos para um padrão (ex: 512x512) com preenchimento de borda suavizado. Ideal para preparar os dados para outras análises.

* **`compare-edges`**: Compara diferentes algoritmos de detecção de borda (Canny, Sobel, etc.) em uma imagem de amostra e salva os resultados visuais na pasta de resultados.

* **`dose-response`**: Executa a análise de dose-resposta em um conjunto pré-definido de imagens e gera gráficos de "Fragmentos vs. Dose" e "Perímetro vs. Dose".

* **`visualization-per-dose`**: Para cada imagem de um conjunto de doses, exibe na tela um gráfico comparativo com os contornos classificados como DNA e RNA.

* **`skeleton-viz`**: Executa a análise de esqueletização, gerando e exibindo uma visualização do esqueleto sobreposto em cada imagem para um conjunto de doses.

* **`skeleton-length`**: Executa a análise quantitativa de esqueletização, calculando o comprimento total das moléculas (em nm) e gerando um gráfico final de "Comprimento vs. Dose".

* **`full-skeleton-analysis`**: Esta é a pipeline de análise mais completa do projeto, projetada para realizar uma investigação quantitativa e estatística detalhada sobre o comprimento das moléculas de DNA.
    - Encontra automaticamente todas as imagens relevantes para cada dose usando padrões de nome de arquivo.
    - Processa cada imagem para extrair o esqueleto de **cada molécula individualmente**.
    - Calcula o comprimento (em nanômetros) de cada esqueleto molecular.
    - Gera um relatório completo de **estatística descritiva** (média, mediana, desvio padrão, quartis, etc.) para os comprimentos em cada grupo de dose.
    - Realiza testes de **estatística inferencial** (ANOVA/Kruskal-Wallis, testes par a par e correlação com a dose) para verificar a significância estatística das diferenças.
    - Cria e salva múltiplas **visualizações** para análise da distribuição dos dados, incluindo histogramas, boxplots e um gráfico de dispersão do comprimento médio versus a dose.
    - **Saída**: Gera uma pasta completa de resultados em `./results/full_skeleton_analysis/` com arquivos `.csv` para as estatísticas, `.txt` para o relatório inferencial e `.png` para os gráficos.

### Exemplos de Uso

Para executar uma análise, certifique-se de que seu ambiente virtual esteja ativado e rode o `main.py` a partir da pasta raiz do projeto, seguido pelo nome da pipeline.

**Exemplo 1: Executar a Análise Estatística Padrão**
```bash
python main.py analysis
```
> Gera os arquivos CSV com os resultados na pasta `./results/`.

**Exemplo 2: Pré-processar as Imagens**
```bash
python main.py preprocess
```
> Salva as imagens normalizadas na pasta de resultados correspondente.

**Exemplo 3: Executar a Análise Quantitativa de Esqueletos**
```bash
python main.py skeleton-length
```
> Exibe os resultados numéricos no terminal e salva o gráfico final na pasta de resultados.