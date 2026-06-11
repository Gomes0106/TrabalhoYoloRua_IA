# Contador de Veículos com YOLO

## Descrição do Problema

Em ruas movimentadas, realizar a contagem manual de veículos é uma tarefa demorada e sujeita a erros. Além disso, coletar dados sobre o fluxo de trânsito exige observação constante, o que dificulta análises rápidas e precisas.

Pensando nisso, este projeto foi desenvolvido para automatizar a contagem de veículos e pessoas utilizando técnicas de Visão Computacional e Inteligência Artificial, permitindo obter informações sobre o tráfego de forma simples e eficiente.

## Descrição da Solução Proposta

O sistema utiliza o modelo YOLOv8 para detectar e rastrear objetos em tempo real a partir de uma câmera IP, webcam ou arquivo de vídeo. Cada objeto recebe um identificador único e é contabilizado apenas uma vez ao cruzar uma linha virtual definida na imagem.

O sistema é capaz de identificar e contar:

* Carros
* Motos
* Pessoas
* Bicicletas
* Ônibus
* Caminhões

Ao final da execução, são gerados relatórios contendo os dados coletados durante o monitoramento.

## Funcionalidades

* Detecção de objetos em tempo real com YOLOv8
* Rastreamento de objetos por ID
* Contagem automática ao cruzar uma linha virtual
* Exibição de estatísticas durante a execução
* Geração de relatórios em CSV e TXT
* Opção de salvar o vídeo processado

## Tecnologias e Bibliotecas Utilizadas

* Python 3.9+
* OpenCV
* Ultralytics YOLOv8
* NumPy
* IP Webcam (captura de vídeo via celular)

## Requisitos de Ambiente

* Python 3.9 ou superior
* Pip instalado
* Celular Android com IP Webcam ou webcam do computador
* Conexão de rede para utilização da câmera IP
* Dependências listadas no arquivo `requirements.txt`

## Instalação

Clone o repositório:

```bash
git clone https://github.com/Gomes0106/TrabalhoYoloRua_IA.git
cd TrabalhoYoloRua_IA
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração da Câmera

### Android (IP Webcam)

1. Instale o aplicativo IP Webcam.
2. Inicie o servidor pelo aplicativo.
3. Anote o endereço IP exibido.

Exemplo:

```text
http://192.168.0.105:8080
```

URL utilizada pelo sistema:

```text
http://192.168.0.105:8080/video
```

## Como Executar

### Utilizando a câmera do celular

```bash
python contador_veiculos.py --fonte http://192.168.0.105:8080/video
```

### Utilizando a webcam do computador

```bash
python contador_veiculos.py --fonte 0
```

### Utilizando um arquivo de vídeo

```bash
python contador_veiculos.py --fonte video.mp4
```

### Exemplo completo

```bash
python contador_veiculos.py --fonte http://192.168.0.105:8080/video --duracao 20 --modelo yolov8n.pt --confianca 0.40 --salvar-video
```

## Parâmetros

| Parâmetro      | Descrição                    |
| -------------- | ---------------------------- |
| --fonte        | Webcam, câmera IP ou vídeo   |
| --duracao      | Tempo de execução em minutos |
| --modelo       | Modelo YOLO utilizado        |
| --confianca    | Confiança mínima da detecção |
| --salvar-video | Salva o vídeo processado     |

## Estrutura do Projeto

```text
TrabalhoYoloRua_IA/
├── contador_veiculos.py
├── requirements.txt
├── README.md
└── resultados/
```

## Resultados

Ao finalizar a execução, os arquivos serão salvos automaticamente na pasta:

```text
resultados/
```

Arquivos gerados:

```text
contagem_DATA.csv
resumo_DATA.txt
video_DATA.mp4 (opcional)
```

## Resultado do Teste

Para realizar esta análise do tráfego em Ituiutaba, foi utilizada uma solução simples e prática. A gravação foi feita com um celular fixado em um tripé, posicionado sobre o telhado da residência para obter uma visão ampla da via.

Durante os 20 minutos de monitoramento, o sistema registrou um total de 109 elementos. A maior parte do fluxo foi composta por carros, com 97 registros, o que representa uma média de aproximadamente 5 veículos por minuto. Também foram identificados 6 caminhões, além da passagem de 1 bicicleta e 1 pedestre.

Em relação às motocicletas, o relatório contabilizou oficialmente 4 ocorrências. No entanto, observou-se que esse número foi um pouco maior na prática. Algumas motos trafegavam em velocidade elevada e, em determinados momentos, não permaneceram tempo suficiente na área de detecção para que o sistema conseguisse rastreá-las e registrar o cruzamento da linha de contagem. Por esse motivo, houve uma pequena diferença entre a quantidade registrada e a quantidade real de motocicletas que passaram pelo local.

De forma geral, o teste demonstrou que o sistema foi capaz de identificar e contabilizar os veículos com boa precisão, mostrando potencial para aplicações de monitoramento e análise de fluxo de trânsito.
