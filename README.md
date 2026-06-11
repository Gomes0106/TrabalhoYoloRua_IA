# Contador de Veículos com YOLO

Sistema de contagem automática de veículos e pessoas utilizando YOLOv8 e OpenCV. O programa detecta e contabiliza carros, motos, pessoas, bicicletas, ônibus e caminhões a partir de uma câmera IP, webcam ou arquivo de vídeo.

## Funcionalidades

* Detecção em tempo real com YOLOv8
* Rastreamento de objetos por ID
* Contagem automática ao cruzar uma linha virtual
* Exibição de estatísticas durante a execução
* Geração de relatórios em CSV e TXT
* Opção de salvar o vídeo processado

## Requisitos

* Python 3.9 ou superior
* Celular com IP Webcam (Android) ou DroidCam (iOS) (opcional)

## Instalação

Clone o projeto e instale as dependências:

```bash
git clone <https://github.com/Gomes0106/TrabalhoYoloRua_IA >
cd vehicle_counter

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

## Configuração da câmera

### Android (IP Webcam)

1. Instale o aplicativo IP Webcam.
2. Inicie o servidor no aplicativo.
3. Anote o endereço exibido.

Exemplo:

```text
http://192.168.0.105:8080
```

URL do vídeo:

```text
http://192.168.0.105:8080/video
```

## Como executar

### Câmera do celular

```bash
python contador_veiculos.py --fonte http://192.168.0.105:8080/video
```

### Webcam do computador

```bash
python contador_veiculos.py --fonte 0
```

### Arquivo de vídeo

```bash
python contador_veiculos.py --fonte video.mp4
```

### Exemplo completo

```bash
python contador_veiculos.py \
--fonte http://192.168.0.105:8080/video \
--duracao 20 \
--modelo yolov8n.pt \
--confianca 0.40 \
--salvar-video
```

## Parâmetros

| Parâmetro      | Descrição                    |
| -------------- | ---------------------------- |
| --fonte        | Webcam, câmera IP ou vídeo   |
| --duracao      | Tempo de execução em minutos |
| --modelo       | Modelo YOLO utilizado        |
| --confianca    | Confiança mínima da detecção |
| --salvar-video | Salva o vídeo processado     |

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

## Estrutura do Projeto

```text
vehicle_counter/
├── contador_veiculos.py
├── requirements.txt
├── README.md
└── resultados/
```

## Dependências Principais

* Ultralytics YOLOv8
* OpenCV


## Resultado final

Para realizar esta análise do tráfego em Ituiutaba, foi utilizada uma solução simples e prática. A gravação foi feita com um celular fixado em um tripé, posicionado sobre o telhado da minha casa.

Durante os 20 minutos de monitoramento, o sistema registrou um total de 109 elementos. A maior parte do fluxo foi composta por carros, com 97 registros, o que representa uma média de aproximadamente 5 veículos por minuto. Também foram identificados 6 caminhões, além da passagem de 1 bicicleta e 1 pedestre.

Em relação às motocicletas, o relatório contabilizou oficialmente 4 ocorrências. No entanto, observou-se que esse número foi um pouco maior na prática. Algumas motos trafegavam em velocidade elevada e, em determinados momentos, não permaneceram tempo suficiente na área de detecção para que o sistema conseguisse rastreá-las e registrar o cruzamento da linha de contagem. Por esse motivo, houve uma pequena diferença entre a quantidade registrada e a quantidade real de motocicletas que passaram pelo local.

De forma geral, o teste demonstrou que o sistema foi capaz de identificar e contabilizar os veículos com boa precisão, mostrando potencial para aplicações de monitoramento e análise de fluxo de trânsito.
