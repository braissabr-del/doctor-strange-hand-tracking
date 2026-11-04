
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# ==========================================
# 1. CAMERA
# ==========================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("Erro ao abrir a camera!")
    exit()

# ==========================================
# 2. DETECTOR DE MAOS
# ==========================================

detector = HandDetector(
    maxHands=2,
    modelComplexity=0,
    detectionCon=0.55,
    minTrackCon=0.45
)

# ==========================================
# 3. VIDEO DO ESCUDO
# ==========================================

shield = cv2.VideoCapture("dr_1.mp4")

if not shield.isOpened():
    print("Erro ao abrir o video do escudo!")
    cap.release()
    exit()

# ==========================================
# 4. REMOVER FUNDO BRANCO
# ==========================================


def prepararEscudo(frame):

    # Reduzir resolucao
    frame = cv2.resize(frame, (960, 540))

    # Converter de BGR para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Identificar o fundo verde
    verde_baixo = np.array([35, 40, 40])
    verde_alto = np.array([90, 255, 255])

    mascara_verde = cv2.inRange(
        hsv,
        verde_baixo,
        verde_alto
    )

    # Suavizar a mascara
    mascara_verde = cv2.morphologyEx(
        mascara_verde,
        cv2.MORPH_OPEN,
        np.ones((3, 3), np.uint8)
    )

    mascara_verde = cv2.GaussianBlur(
        mascara_verde,
        (5, 5),
        0
    )

    # Criar transparencia
    alpha = 255 - mascara_verde

    # Remover pequenos residuos
    pontos = cv2.findNonZero(
        (alpha > 15).astype(np.uint8) * 255
    )

    if pontos is None:
        return None

    # Recortar o escudo
    x, y, w, h = cv2.boundingRect(pontos)

    margem = 15

    x1 = max(0, x - margem)
    y1 = max(0, y - margem)
    x2 = min(frame.shape[1], x + w + margem)
    y2 = min(frame.shape[0], y + h + margem)

    imagem = frame[y1:y2, x1:x2]
    alpha = alpha[y1:y2, x1:x2]

    # Criar imagem com transparencia
    resultado = cv2.merge([
        imagem[:, :, 0],
        imagem[:, :, 1],
        imagem[:, :, 2],
        alpha
    ])

    return resultado


# ==========================================
# 5. SOBREPOR ESCUDO NA CAMERA
# ==========================================

def Overlay(background, overlay, x, y, handSize):

    if overlay is None:
        return background

    # Tamanho do escudo proporcional a mao
    largura = int(handSize * 2.0)

    if largura < 1:
        return background

    proporcao = largura / overlay.shape[1]

    altura = int(overlay.shape[0] * proporcao)

    overlay = cv2.resize(
        overlay,
        (largura, altura),
        interpolation=cv2.INTER_AREA
    )

    # Coordenadas do escudo
    x1 = int(x - largura / 2)
    y1 = int(y - altura / 2)

    x2 = x1 + largura
    y2 = y1 + altura

    # Limitar a area a tela
    bg_h, bg_w = background.shape[:2]

    bx1 = max(0, x1)
    by1 = max(0, y1)
    bx2 = min(bg_w, x2)
    by2 = min(bg_h, y2)

    if bx1 >= bx2 or by1 >= by2:
        return background

    # Recortar a parte visivel do escudo
    ox1 = bx1 - x1
    oy1 = by1 - y1
    ox2 = ox1 + (bx2 - bx1)
    oy2 = oy1 + (by2 - by1)

    parte = overlay[oy1:oy2, ox1:ox2]

    # Separar imagem e transparencia
    imagem = parte[:, :, :3].astype(np.float32)

    alpha = parte[:, :, 3].astype(np.float32) / 255.0
    alpha = alpha[:, :, np.newaxis]

    # Misturar com a imagem da camera
    roi = background[by1:by2, bx1:bx2].astype(np.float32)

    resultado = (imagem * alpha) + (roi * (1 - alpha))

    background[by1:by2, bx1:bx2] = resultado.astype(np.uint8)

    return background


# ==========================================
# 6. CONTROLE DO ESCUDO
# ==========================================

showShield = False
changeTimer = 0

print("Doctor Strange iniciado!")
print("Pressione Q para sair.")

# ==========================================
# 7. LOOP PRINCIPAL
# ==========================================

while True:

    success, img = cap.read()

    if not success:
        print("Erro na captura da camera!")
        break

    # Detectar maos
    hands, img = detector.findHands(img, draw=False)

    final = img.copy()

    # Alternar escudo quando duas maos permanecem visiveis
    if len(hands) == 2:

        changeTimer += 1

        if changeTimer > 100:
            showShield = not showShield
            changeTimer = 0

    else:
        changeTimer = 0

    # Uma mao ativa o escudo diretamente
    # Duas maos dependem do estado showShield
    applyShield = (
        (showShield and len(hands) == 2)
        or len(hands) == 1
    )

    
    # Aplicar escudo em todas as maos detectadas
    if len(hands) > 0:

        shieldSuccess, shieldImg = shield.read()

        # Reiniciar video quando chegar ao final
        if not shieldSuccess:
            shield.set(cv2.CAP_PROP_POS_FRAMES, 0)
            shieldSuccess, shieldImg = shield.read()

        if shieldSuccess:

            escudo = prepararEscudo(shieldImg)

            if escudo is not None:

                # Aplicar um escudo em cada mao
                for hand in hands:

                    bbox = hand["bbox"]
                    handSize = bbox[2]

                    cx, cy = hand["center"]

                    final = Overlay(
                        final,
                        escudo,
                        cx,
                        cy,
                        handSize
                    )

    # Espelhar imagem para acompanhar movimentos
    cv2.imshow(
        "Doctor Strange",
        cv2.flip(final, 1)
    )

    # Tecla Q encerra o programa
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# 8. FINALIZACAO
# ==========================================

cap.release()
shield.release()

cv2.destroyAllWindows()

print("Programa encerrado!")