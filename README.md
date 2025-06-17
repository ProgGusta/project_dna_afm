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
│       ├── preprocessor.py
│       ├── segmenter.py
│       ├── feature_extractor.py
│       ├── stats_calculator.py
│       ├── visualizer.py
│       └── analyzer.py
├── .gitignore
├── main_dose_response.py
├── main_skeleton_analysis.py
├── main_compare.py
├── pyproject.toml
└── README.md
```

* **`src/dna_analyzer/`**: Contém todo o código-fonte do pacote Python. Cada módulo encapsula uma parte da lógica (pré-processamento, segmentação, visualização, etc.).
* **`data/`**: Pasta para armazenar as imagens de AFM. **Esta pasta é ignorada pelo Git** (via `.gitignore`) e deve ser criada manualmente.
    * `raw/`: Para as imagens originais, intocadas.
    * `processed/`: Para imagens após etapas de pré-processamento.
* **`results/`**: Armazena todas as saídas geradas pelos scripts, como imagens processadas, gráficos e arquivos CSV com estatísticas. **Também ignorada pelo Git**.
* **`notebooks/`**: Para Jupyter Notebooks utilizados em análises exploratórias e testes de algoritmos.
* **`main_*.py`**: Scripts de ponto de entrada, cada um projetado para executar uma tarefa ou experimento específico (ex: `main_dose_response.py` para gerar gráficos de dose-resposta).
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

Cada script `main_*.py` na raiz do projeto foi projetado para executar uma análise específica.

### Exemplo: Análise de Dose-Resposta

Este script processa um conjunto pré-definido de imagens, cada uma associada a uma dose de radiação, e gera gráficos mostrando o impacto da dose no DNA.

1.  **Verifique os Caminhos**: Antes de executar, abra o arquivo `main_dose_response.py` e garanta que os caminhos no dicionário `IMAGE_PATHS` apontem para a localização correta das suas imagens na pasta `data/`.

2.  **Execute o Script**: No terminal (com o ambiente virtual ativado), execute o seguinte comando a partir da pasta raiz do projeto:
    ```bash
    python main_dose_response.py
    ```

### O que Esperar
* O terminal exibirá o progresso do processamento para cada dose.
* Ao final, os resultados numéricos serão impressos no console.
* Uma nova pasta será criada em `results/resultados_dose_resposta/`, contendo os gráficos salvos em formato `.png` (ex: `grafico_fragmentos_vs_dose.png`).

Para executar outras análises, utilize o script correspondente, como `python main_skeleton_analysis.py` para a análise de esqueletos.