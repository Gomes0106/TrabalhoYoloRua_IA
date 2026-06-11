"""
Contador de Veículos com YOLO
Detecta e contabiliza carros, motos e pessoas em tempo real.
Usa a webcam do PC por padrão (índice 0).
"""

import cv2
import time
import csv
import os
import argparse
from datetime import datetime
from collections import defaultdict

try:
    from ultralytics import YOLO
except ImportError:
    print("[ERRO] ultralytics não instalado. Execute: pip install ultralytics")
    exit(1)


# ─── Configurações ────────────────────────────────────────────────────────────

# Classes do YOLO que nos interessam (COCO dataset)
CLASSES_DE_INTERESSE = {
    0:  "pessoa",
    1:  "bicicleta",
    2:  "carro",
    3:  "moto",
    5:  "ônibus",
    7:  "caminhão",
}

# Cores por classe (BGR)
CORES = {
    "pessoa":     (0,   255, 0),    # verde
    "bicicleta":  (255, 165, 0),    # azul claro
    "carro":      (0,   0,   255),  # vermelho
    "moto":       (0,   255, 255),  # amarelo
    "ônibus":     (255, 0,   0),    # azul
    "caminhão":   (128, 0,   128),  # roxo
}

# Duração padrão da sessão em minutos
DURACAO_PADRAO_MIN = 20


# ─── Linha de contagem ────────────────────────────────────────────────────────

def desenhar_linha(frame, x_linha, altura):
    """Desenha a linha de contagem vertical na tela."""
    cv2.line(frame, (x_linha, 0), (x_linha, altura), (0, 255, 255), 2)
    cv2.putText(frame, "LINHA DE CONTAGEM", (x_linha + 8, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

def cruzou_linha(cx_atual, cx_anterior, x_linha):
    """Retorna True se o centróide cruzou a linha vertical."""
    if cx_anterior is None:
        return False
    return (cx_anterior < x_linha <= cx_atual) or (cx_anterior > x_linha >= cx_atual)


# ─── HUD (informações na tela) ────────────────────────────────────────────────

def desenhar_hud(frame, contagens, tempo_restante_s, fps_real):
    """Desenha o painel de estatísticas no canto superior esquerdo."""
    painel_h = 30 + len(contagens) * 28 + 50
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (280, painel_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    y = 35
    cv2.putText(frame, "CONTADOR DE TRAFEGO", (18, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    y += 8
    cv2.line(frame, (15, y), (275, y), (100, 100, 100), 1)
    y += 18

    for classe, total in sorted(contagens.items()):
        cor = CORES.get(classe, (200, 200, 200))
        cv2.putText(frame, f"{classe.capitalize():12s}: {total:4d}", (18, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, cor, 1)
        y += 28

    y += 4
    mins = int(tempo_restante_s // 60)
    secs = int(tempo_restante_s % 60)
    cv2.putText(frame, f"Tempo restante: {mins:02d}:{secs:02d}", (18, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, (180, 180, 180), 1)
    y += 22
    cv2.putText(frame, f"FPS: {fps_real:.1f}", (18, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, (180, 180, 180), 1)


# ─── Salvamento de resultados ─────────────────────────────────────────────────

def salvar_resultados(contagens, duracao_real_s, output_dir="resultados"):
    """Salva contagens em CSV e gera um resumo em TXT."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # CSV com série temporal
    csv_path = os.path.join(output_dir, f"contagem_{timestamp}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["categoria", "total", "por_minuto"])
        for classe, total in sorted(contagens.items()):
            por_min = total / (duracao_real_s / 60) if duracao_real_s > 0 else 0
            writer.writerow([classe, total, f"{por_min:.2f}"])
        writer.writerow(["TOTAL", sum(contagens.values()), ""])

    # Resumo legível
    txt_path = os.path.join(output_dir, f"resumo_{timestamp}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("=" * 45 + "\n")
        f.write("   RELATÓRIO DE CONTAGEM DE TRÁFEGO\n")
        f.write("=" * 45 + "\n")
        f.write(f"Data/hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Duração  : {duracao_real_s/60:.1f} minutos\n\n")
        f.write(f"{'Categoria':<15} {'Total':>6}  {'Por minuto':>10}\n")
        f.write("-" * 35 + "\n")
        for classe, total in sorted(contagens.items()):
            por_min = total / (duracao_real_s / 60) if duracao_real_s > 0 else 0
            f.write(f"{classe.capitalize():<15} {total:>6}  {por_min:>10.2f}\n")
        f.write("-" * 35 + "\n")
        total_geral = sum(contagens.values())
        f.write(f"{'TOTAL GERAL':<15} {total_geral:>6}\n")
        f.write("=" * 45 + "\n")

    print(f"\n✅  Resultados salvos em '{output_dir}/'")
    print(f"   📄 {csv_path}")
    print(f"   📄 {txt_path}")
    return csv_path, txt_path


# ─── Loop principal ───────────────────────────────────────────────────────────

def rodar(fonte, duracao_min, modelo_path, confianca, salvar_video):
    """Função principal: abre a fonte de vídeo e executa a detecção."""

    print(f"\n{'='*50}")
    print("  CONTADOR DE VEÍCULOS — YOLO v8")
    print(f"{'='*50}")
    print(f"  Fonte    : {fonte}")
    print(f"  Modelo   : {modelo_path}")
    print(f"  Duração  : {duracao_min} minutos")
    print(f"  Confiança: {confianca}")
    print(f"{'='*50}\n")

    # Carrega modelo
    print("[...] Carregando modelo YOLO...")
    modelo = YOLO(modelo_path)
    print("[OK]  Modelo carregado!\n")

    # Abre fonte de vídeo
    print(f"[...] Conectando à fonte: {fonte}")
    cap = cv2.VideoCapture(fonte)
    if not cap.isOpened():
        print(f"[ERRO] Não foi possível abrir a fonte: {fonte}")
        print("       Verifique se o endereço IP está correto e o app está rodando.")
        return

    largura  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_src  = cap.get(cv2.CAP_PROP_FPS) or 25
    print(f"[OK]  Fonte aberta: {largura}x{altura} @ {fps_src:.1f} FPS\n")

    # Linha de contagem (60% da altura)
    x_linha = int(largura * 0.50) 

    # Writer de vídeo (opcional)
    writer = None
    if salvar_video:
        os.makedirs("resultados", exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = os.path.join("resultados", f"video_{ts}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(video_path, fourcc, fps_src, (largura, altura))
        print(f"[OK]  Gravando vídeo em: {video_path}\n")

    # Estado de rastreamento
    contagens        = defaultdict(int)   # total por classe
    tracks_anteriores = {}                 # id_track -> cy no frame anterior
    ids_contados     = set()               # ids que já foram contabilizados

    duracao_s  = duracao_min * 60
    inicio     = time.time()
    frames_fps = 0
    t_fps      = time.time()
    fps_real   = 0.0

    print("[RUN] Iniciando captura. Pressione 'q' para encerrar.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame não recebido. Tentando reconectar...")
            time.sleep(0.5)
            cap.release()
            cap = cv2.VideoCapture(fonte)
            continue

        elapsed    = time.time() - inicio
        restante   = max(0, duracao_s - elapsed)

        # FPS real
        frames_fps += 1
        if time.time() - t_fps >= 1.0:
            fps_real   = frames_fps / (time.time() - t_fps)
            frames_fps = 0
            t_fps      = time.time()

        # ── Inferência YOLO com rastreamento ──────────────────────────────────
        resultados = modelo.track(
            frame,
            persist=True,
            conf=confianca,
            classes=list(CLASSES_DE_INTERESSE.keys()),
            verbose=False,
        )

        # ── Processa detecções ────────────────────────────────────────────────
        if resultados[0].boxes is not None:
            boxes = resultados[0].boxes
            for box in boxes:
                # Pula detecções sem ID de rastreamento
                if box.id is None:
                    continue

                track_id   = int(box.id.item())
                classe_idx = int(box.cls.item())
                classe     = CLASSES_DE_INTERESSE.get(classe_idx, "desconhecido")
                conf       = float(box.conf.item())

                # Coordenadas
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                # Verifica cruzamento da linha
                cx_ant = tracks_anteriores.get(track_id)
                if cruzou_linha(cx, cx_ant, x_linha) and track_id not in ids_contados:
                    contagens[classe] += 1
                    ids_contados.add(track_id)

                tracks_anteriores[track_id] = cx

                # Desenha bbox
                cor = CORES.get(classe, (200, 200, 200))
                cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)
                label = f"{classe} #{track_id} {conf:.0%}"
                cv2.putText(frame, label, (x1, y1 - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, cor, 1)
                # Centróide
                cv2.circle(frame, (cx, cy), 4, cor, -1)

        # ── Desenha UI ────────────────────────────────────────────────────────
        desenhar_linha(frame, x_linha, largura)
        desenhar_hud(frame, contagens, restante, fps_real)

        if salvar_video and writer:
            writer.write(frame)

        cv2.imshow("Contador de Trafego — pressione Q para sair", frame)

        # ── Saída ─────────────────────────────────────────────────────────────
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or restante <= 0:
            break

    # ── Finaliza ──────────────────────────────────────────────────────────────
    duracao_real = time.time() - inicio
    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()

    # Resumo no terminal
    print(f"\n{'='*45}")
    print("  RESULTADO FINAL")
    print(f"{'='*45}")
    for classe, total in sorted(contagens.items()):
        por_min = total / (duracao_real / 60)
        print(f"  {classe.capitalize():<15} {total:>5}   ({por_min:.1f}/min)")
    print(f"  {'TOTAL':<15} {sum(contagens.values()):>5}")
    print(f"{'='*45}")
    print(f"  Duração real: {duracao_real/60:.1f} min")

    salvar_resultados(contagens, duracao_real)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Contador de veículos com YOLO — câmera IP ou webcam local"
    )
    parser.add_argument(
        "--fonte",
        default="0",
        help=(
            "Fonte de vídeo. Exemplos:\n"
            "  Webcam do PC (padrão): 0\n"
            "  Segunda câmera:        1\n"
            "  Câmera IP (IP Webcam): http://192.168.0.XXX:8080/video\n"
            "  Arquivo de vídeo:      video.mp4"
        ),
    )
    parser.add_argument(
        "--duracao",
        type=int,
        default=DURACAO_PADRAO_MIN,
        help=f"Duração da sessão em minutos (padrão: {DURACAO_PADRAO_MIN})",
    )
    parser.add_argument(
        "--modelo",
        default="yolov8n.pt",
        help="Modelo YOLO (yolov8n.pt, yolov8s.pt, yolov8m.pt, ...)",
    )
    parser.add_argument(
        "--confianca",
        type=float,
        default=0.40,
        help="Confiança mínima para detecção (0.0–1.0, padrão: 0.40)",
    )
    parser.add_argument(
        "--salvar-video",
        action="store_true",
        help="Salva o vídeo processado em resultados/",
    )
    args = parser.parse_args()

    # Converte "0" para inteiro se for webcam local
    fonte = args.fonte
    if fonte.strip().isdigit():
        fonte = int(fonte)

    rodar(
        fonte=fonte,
        duracao_min=args.duracao,
        modelo_path=args.modelo,
        confianca=args.confianca,
        salvar_video=args.salvar_video,
    )


if __name__ == "__main__":
    main()
