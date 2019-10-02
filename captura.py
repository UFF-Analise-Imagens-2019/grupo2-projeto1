import time
import picamera
import numpy as np
import ai
import cv2

camera = picamera.PiCamera()
camera.resolution = (1024, 768)
camera.framerate = 24
camera.start_preview()

# um segundo para inicializar a camera
time.sleep(1)

nome_diretorio = '/home/pi/placerda'
capturou = 0

while True:
    try:
        # obtem imagem do frame
        time.sleep(1)
        # exit                                       
    except KeyboardInterrupt:
        print("capturou!")
        capturou+=1
        imagem_atual = np.empty((768 * 1024 * 3,), dtype=np.uint8)
        camera.capture(imagem_atual, 'bgr')
        imagem_atual = imagem_atual.reshape((768, 1024, 3))
        cv2.imwrite("{}/imagem_{}.png".format(nome_diretorio, capturou), imagem_atual)
        if (capturou == 3):
            break