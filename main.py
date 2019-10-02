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

# CONSTANTES
DISTANCIA_INICIAL_REAL = 49 # distancia em milimetros

# inicializa variaveis de processamento
imagem_inicial = []
distancia_inicial = 0
distancia_atual = 0
distancia_anterior = 0

# overlay sobre o video para desenho da reta
overlay = np.zeros((768, 1024, 3), dtype=np.uint8) 
o = camera.add_overlay(overlay, layer=3, alpha=64)

while True:
    try:
        # obtem imagem do frame
        imagem_atual = np.empty((768 * 1024 * 3,), dtype=np.uint8)
        camera.capture(imagem_atual, 'bgr')
        imagem_atual = imagem_atual.reshape((768, 1024, 3))
        
        # inicializa imagem_inicial na primeira vez que entra no loop e calcula a distancia entre os dois pontos
        if (imagem_inicial == []):
            imagem_inicial = imagem_atual
            distancia_inicial = ai.distancia_pontos(imagem_inicial)[0] # otem a distancia ente os pontos (pos 0)
        
        # verifica se conseguiu calcular a distancia senao tentar obter a imagem inicial novamente na proxima iteracao
        if distancia_inicial == 0:
            print("nao foi possivel identificar os pontos da imagem inicial")
            imagem_inicial = []
        else:
            print("distancia incial:{}".format(distancia_inicial))
            # obtem a distancia atual, os dois pontos e os pixels centrais de cada um deles
            distancia_atual, p1, p2, p1c, p2c = ai.distancia_pontos(imagem_atual)
        
            if (distancia_atual == 0):
                print("nao foi possivel identificar os pontos da imagem atual")
                continue
        
            # calcula a variacao entre as imagens
            variacao_pixels = distancia_atual - distancia_inicial
            variacao_mm = variacao_pixels * DISTANCIA_INICIAL_REAL / distancia_inicial
            print("distancia:{}".format(variacao_pixels))
            
            # desenha uma reta entre os pontos e mostra informacoes sobre a variacao na tela
            if abs(distancia_atual - distancia_anterior) > 0: # ajusta sensibilidade para 1 pixels
         
                # cria overlay sobre o video com imagem da reta
                overlay = np.zeros((768, 1024, 3), dtype=np.uint8)        
                # desenha a reta
                
                
                
                # for px in p1: overlay[px[0], px[1]] = (0, 255, 0)
                # for px in p2: overlay[px[0], px[1]] = (0, 255, 0)
                cv2.circle(overlay, p1c,10, (255,0,255), thickness=2)
                cv2.circle(overlay, p2c,10, (0,255,0), thickness=2)
                cv2.line(overlay, p1c, p2c, (255, 255, 255), thickness=2)


                # desenha ROI
                # cv2.line(overlay, (ai.ROI_X1, ai.ROI_Y1), (ai.ROI_X1, ai.ROI_Y2), (255, 0, 255), thickness=2)
                # cv2.line(overlay, (ai.ROI_X1, ai.ROI_Y2), (ai.ROI_X2, ai.ROI_Y2), (255, 0, 255), thickness=2)
                # cv2.line(overlay, (ai.ROI_X2, ai.ROI_Y2), (ai.ROI_X2, ai.ROI_Y1), (255, 0, 255), thickness=2)
                # cv2.line(overlay, (ai.ROI_X2, ai.ROI_Y1), (ai.ROI_X1, ai.ROI_Y1), (255, 0, 255), thickness=2)
                
                variacao_mm = round(variacao_mm, 1)
            
                # mostra texto com ainformacoes sobre a variação 
                camera.annotate_text = "\n Variacao em Pixels: {} \n Variacao em mm: {}".format(variacao_pixels, variacao_mm)
 
                camera.remove_overlay(o)
                o = camera.add_overlay(overlay, layer=3, alpha=64)            

            distancia_anterior = distancia_atual # controle para atualizar imagem na tela
        print("capturou")
        time.sleep(1)         
                               
    except KeyboardInterrupt:
        break
