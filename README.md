# 🚗 Contador de Veículos com YOLO

Detecta e contabiliza **carros, motos, pessoas, bicicletas, ônibus e caminhões** em tempo real usando a câmera do celular como fonte de vídeo.

---

## 📋 O que o projeto faz

- Conecta à câmera do celular via rede Wi-Fi (app **IP Webcam**)
- Usa **YOLOv8** para detectar e rastrear objetos frame a frame
- Conta cada objeto **uma única vez** quando ele cruza uma linha virtual na tela
- Exibe estatísticas ao vivo (totais + por minuto)
- Encerra automaticamente após o tempo configurado (padrão: 20 min)
- Salva os resultados em **CSV** e **TXT** na pasta `resultados/`

---

## 🗂 Estrutura do projeto

```
vehicle_counter/
├── contador_veiculos.py   # Script principal
├── requirements.txt       # Dependências Python
├── README.md              # Este arquivo
└── resultados/            # Criado automaticamente ao rodar
    ├── contagem_YYYYMMDD_HHMMSS.csv
    ├── resumo_YYYYMMDD_HHMMSS.txt
    └── video_YYYYMMDD_HHMMSS.mp4   # Somente com --salvar-video
```

---

## ⚙️ Pré-requisitos

| Requisito | Versão mínima |
|-----------|---------------|
| Python    | 3.9+          |
| pip       | qualquer      |
| Celular   | Android (IP Webcam) ou iOS (DroidCam) |

---

## 🚀 Instalação passo a passo

### 1. Clone ou baixe o projeto

```bash
# Se tiver Git:
[git clone <url-do-repo>](https://github.com/Gomes0106/TrabalhoYoloRua_IA)
cd vehicle_counter

# Ou baixe o ZIP e extraia
```

### 2. (Recomendado) Crie um ambiente virtual

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

> Na primeira execução, o YOLOv8 baixará automaticamente o modelo `yolov8n.pt` (~6 MB).

---

## 📱 Configurar a câmera do celular

### Android — IP Webcam (gratuito, recomendado)

1. Instale o app **IP Webcam** (Play Store)
2. Abra o app → role até o final → toque em **"Iniciar servidor"**
3. Anote o endereço exibido na tela, ex: `http://192.168.0.105:8080`
4. No navegador do PC, acesse esse endereço para confirmar que funciona
5. A URL do vídeo será: `http://192.168.0.105:8080/video`

### iOS — DroidCam (gratuito)

1. Instale **DroidCam** no iPhone e no PC
2. Conecte usando o IP exibido no app
3. Use a URL: `http://192.168.0.XXX:4747/video`

> ⚠️ **Celular e PC precisam estar na mesma rede Wi-Fi.**

---

## ▶️ Como executar

### Uso básico

```bash
python contador_veiculos.py --fonte http://192.168.0.105:8080/video
```

### Todos os parâmetros

```bash
python contador_veiculos.py \
  --fonte http://192.168.0.105:8080/video \
  --duracao 20 \
  --modelo yolov8n.pt \
  --confianca 0.40 \
  --salvar-video
```

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| `--fonte` | `http://192.168.0.100:8080/video` | URL da câmera IP, `0` para webcam local ou caminho de um `.mp4` |
| `--duracao` | `20` | Duração da sessão em minutos |
| `--modelo` | `yolov8n.pt` | Modelo YOLO a usar (ver tabela abaixo) |
| `--confianca` | `0.40` | Confiança mínima (0.0–1.0) |
| `--salvar-video` | desativado | Salva o vídeo processado |

### Testar com webcam do notebook

```bash
python contador_veiculos.py --fonte 0 --duracao 5
```

### Testar com um vídeo gravado

```bash
python contador_veiculos.py --fonte meu_video.mp4 --duracao 999
```

---

## 🎯 Escolhendo o modelo YOLO

| Modelo | Tamanho | Velocidade | Precisão | Indicado para |
|--------|---------|------------|----------|---------------|
| `yolov8n.pt` | ~6 MB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | PC sem GPU, tempo real |
| `yolov8s.pt` | ~22 MB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Equilíbrio (recomendado) |
| `yolov8m.pt` | ~52 MB | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | PC com GPU dedicada |
| `yolov8l.pt` | ~87 MB | ⚡⚡ | ⭐⭐⭐⭐⭐ | GPU potente |

> **Sem GPU?** Use `yolov8n.pt` (padrão). Com GPU NVIDIA, pode usar `yolov8s.pt` ou maior.

---

## 🖥 Interface durante a execução

```
┌─────────────────────────────────────────┐
│ CONTADOR DE TRAFEGO                      │
│ ─────────────────────────────────────── │
│ Pessoa        :   47                     │
│ Carro         :  123                     │
│ Moto          :   38                     │
│ Ônibus        :    5                     │
│ Caminhão      :    9                     │
│                                          │
│ Tempo restante: 14:32                    │
│ FPS: 18.4                                │
├─────────────────────────────────────────┤
│                                          │
│  ════ LINHA DE CONTAGEM ════             │  ← linha amarela
│                                          │
│  [bbox vermelho] carro #12 92%           │
│  [bbox verde]    pessoa #7 88%           │
└─────────────────────────────────────────┘
```

- **Linha amarela**: objetos são contados ao cruzá-la (nos dois sentidos)
- **Bbox colorido**: cada classe tem uma cor diferente
- **`#ID`**: identificador único de rastreamento por objeto

**Tecla `Q`** → encerra a sessão e salva os resultados.

---

## 📊 Exemplo de saída (resultados/)

**resumo_20250611_143022.txt**
```
=============================================
   RELATÓRIO DE CONTAGEM DE TRÁFEGO
=============================================
Data/hora: 11/06/2025 14:30:22
Duração  : 20.0 minutos

Categoria       Total   Por minuto
-----------------------------------
Bicicleta           8         0.40
Caminhão           11         0.55
Carro             187         9.35
Moto               64         3.20
Ônibus              6         0.30
Pessoa             93         4.65
-----------------------------------
TOTAL GERAL       369
=============================================
```

---

## 🔧 Ajustes finos

### Mover a linha de contagem

No arquivo `contador_veiculos.py`, linha 160:

```python
y_linha = int(altura * 0.60)   # 60% da altura — mude para 0.5, 0.7, etc.
```

### Adicionar ou remover classes detectadas

```python
CLASSES_DE_INTERESSE = {
    0:  "pessoa",
    2:  "carro",
    3:  "moto",
    # Comente as linhas que não quer detectar
    # 1:  "bicicleta",
    # 5:  "ônibus",
    # 7:  "caminhão",
}
```

### Reduzir uso de CPU (frames por segundo)

No `contador_veiculos.py`, após `cap.read()`, adicione:

```python
time.sleep(0.05)   # processa ~20 frames/s no máximo
```

---

## ❓ Resolução de problemas

| Problema | Solução |
|----------|---------|
| `Não foi possível abrir a fonte` | Verifique se celular e PC estão na mesma rede Wi-Fi e o app está rodando |
| FPS muito baixo (<5) | Use `yolov8n.pt` ou reduza a resolução no app IP Webcam |
| Objetos contados múltiplas vezes | Aumente `--confianca` para 0.50 ou 0.60 |
| Objetos não detectados | Diminua `--confianca` para 0.30; melhore a iluminação |
| Janela não abre (servidor remoto) | Execute localmente ou use `--salvar-video` e visualize depois |
| `ModuleNotFoundError: ultralytics` | Execute `pip install ultralytics` com o venv ativado |

---

## 💡 Dicas para uma boa coleta

1. **Posicione o celular** perpendicular à rua (visão de cima ou lateral), não diagonal
2. **Fixe o celular** para evitar trepidação — use um tripé ou apoio firme
3. **Boa iluminação** melhora muito a detecção; evite contraluz
4. **Resolução**: no IP Webcam, use 640×480 para velocidade ou 1280×720 para precisão
5. **Carregador**: mantenha o celular na tomada durante os 20 minutos

---

## 🧠 Como funciona (técnico)

```
Câmera (celular) → Frame JPEG via HTTP
        ↓
  OpenCV captura o frame
        ↓
  YOLOv8 detecta objetos (bbox + classe + confiança)
        ↓
  ByteTrack atribui ID único por objeto entre frames
        ↓
  Verifica se centróide cruzou a linha virtual
        ↓
  Incrementa contador (cada ID contado 1 única vez)
        ↓
  Desenha HUD + bboxes na tela
        ↓
  Salva CSV/TXT ao encerrar
```

---

## 📦 Dependências

- **[Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)** — detecção e rastreamento
- **[OpenCV](https://opencv.org/)** — captura de vídeo e renderização

---

## 📄 Licença

Uso livre para fins educacionais e acadêmicos.
