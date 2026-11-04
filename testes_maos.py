
import cv2
from cvzone.HandTrackingModule import HandDetector
import time

# Detector
detector = HandDetector(
    maxHands=2,
    detectionCon=0.5,
    minTrackCon=0.5,
    modelComplexity=0
)

# Câmera
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Não foi possível abrir a câmera.")
    exit()

previousTime = 0

while True:

    success, img = cap.read()

    if not success:
        print("Falha na captura.")
        break

    # Detecta e DESENHA as mãos
    hands, img = detector.findHands(img, draw=True)

    # Mostra quantidade de mãos
    cv2.putText(
        img,
        f"Maos detectadas: {len(hands)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # Calcula FPS
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime) if previousTime else 0
    previousTime = currentTime

    cv2.putText(
        img,
        f"FPS: {int(fps)}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow("Teste de reconhecimento", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
