# -*- coding: utf-8 -*-
# FUNCOES PARA ANALISE DE IMAGENS
import cv2

#cv2.circle(imagem, (pt1pxc_y, pt1pxc_x),10, (255,255,255))
#cv2.circle(imagem, (pt2pxc_y, pt2pxc_x),10, (255,255,255))
#cv2.line(imagem,(pt1pxc_y, pt1pxc_x),(pt2pxc_y, pt2pxc_x),(255,255,255))

# CONSTANTES (PARAMETROS)
ROI_X1 = 490 #400#472
ROI_Y1 = 160  #20#183
ROI_X2 = 540 # 655#602
ROI_Y2 = 590 #498

THRESHOLD_PRETO  = 140
DISTANCIA_MINIMA = 20

#cor da marca 1 (verde)
VHueMin1 = 56 # 66 #58
VHueMax1 = 89 # 79 #72
VSMin1 = 8 #18 #13
VSMax1 = 45 #35 # 24

#cor da marca 2 (rosa)
VHueMin2 = 139 #149
VHueMax2 = 169 #159
VSMin2 = 31 #41
VSMax2 = 68 #58

#cor da marca 3 (azul)
VHueMin3 = 102
VHueMax3 = 110
VSMin3 = 29
VSMax3 = 53


# funcao utilitaria para mostrar a imagem
def show(imagem):
    cv2.imshow("show", imagem)
    cv2.waitKey(0)
    
# funcao que calcula a distancia vetorial entre dois pixels
def distancia_pixels(px1, px2):
    a = (px2[0]-px1[0])**2
    b = (px2[1]-px1[1])**2
    c = (a + b)**0.5
    return int(c)

# calcula a distancia entre dois pontos na imagem
def distancia_pontos(imagem):
    
    # recorta regiao de interesse definida empiricamente
    img = imagem[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]
    
    #img = img[248:273, 57:200]
    #img = img[459:495, 48:199]
    #cv2.imwrite("/home/pi/placerda/roi fita rosa.png", img)
    #calcula(img)
    #exit
    
    #cv2.imwrite("/home/pi/placerda/roi.png", img)
    
    # trabalha em HSV para futuramente melhorar o histograma
    roi = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #aumentar contraste equalizando histograma: aumentar a intensidade
    #
    #pelo teste, não vale a pena
    #
    #

    # define os dois pontos utilizados para calcular a distância na imagem
    (h,w) = roi.shape[:2] # obtem altura e largura
    pt1 = [] # cada ponto e' uma lista de pixels na imagem
    pt2 = []
 
    pixels_area1 = 0
    pixels_area2 = 0
    # varre a area de interesse para encontrar os pixels dos pontos 1 e 2
    for y in range(h):
        for x in range(w):
            (H, S, V) = roi[y, x]
            if ((H >= VHueMin1) and (H <= VHueMax1) and (S >= VSMin1) and (S <= VSMax1)):
                x_i = ROI_X1 + x
                y_i = ROI_Y1 + y
                pt1.append((y_i, x_i))
                pixels_area1 += 1
            if ((H >= VHueMin2) and (H <= VHueMax2) and (S >= VSMin2) and (S <= VSMax2)):
                x_i = ROI_X1 + x
                y_i = ROI_Y1 + y
                pt2.append((y_i, x_i))
                pixels_area2 += 1
    # print("pixels_area1={}".format(pixels_area1))                
    # print("pixels area2={}".format(pixels_area2))   
# testa se encontrou os pontos
    if (len(pt1) == 0) or (len(pt2) == 0):
        return 0, [], [], (0,0), (0,0)
    
    # identifica o pixel central de pt1 e pt2

    # ponto central de pt1
    pt1pxc_x = sum(px[0] for px in pt1) // len(pt1)
    pt1pxc_y = sum(px[1] for px in pt1) // len(pt1)
    pt1pxc = (pt1pxc_y, pt1pxc_x)

    # ponto central de pt2
    pt2pxc_x = sum(px[0] for px in pt2) // len(pt2)
    pt2pxc_y = sum(px[1] for px in pt2) // len(pt2)
    pt2pxc = (pt2pxc_y, pt2pxc_x)
    
     # calcula a distancia entre os dois pontos
    distancia_pontos = distancia_pixels(pt1pxc, pt2pxc)  

    return distancia_pontos, pt1, pt2, pt1pxc, pt2pxc




# calcula a distancia entre dois pontos na imagem
def distancia_pontos_original(imagem):
    # trabalha em grayscale para simplificar a identificacao dos pontos
    gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # recorta regiao de interesse definida empiricamente
    roi = gray[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]

    # define os dois pontos utilizados para calcular a distância na imagem
    (h,w) = roi.shape[:2] # obtem altura e largura
    pt1 = [] # cada ponto e' uma lista de pixels na imagem
    pt2 = []
        
    # varre a area de interesse para encontrar os pixels dos pontos 1 e 2
    for y in range(h):
        for x in range(w):
            if roi[y,x] < THRESHOLD_PRETO:
                print("{},{}:{}".format(y,x,roi[y,x])) # debug
                x_i = ROI_X1 + x  # x_i representa o x do pixel nas coordenadas da imagem inteira
                y_i = ROI_Y1 + y  # y_i representa o y do pixel nas coordenadas da imagem inteira
                if len(pt1) == 0: # encontramos o primeiro pixel de p1
                    pt1.append((x_i, y_i))
                elif distancia_pixels(pt1[0], (x_i, y_i)) < DISTANCIA_MINIMA: # novo pixel esta na abrangencia de p1
                    pt1.append((x_i, y_i))
                else:
                    pt2.append((x_i, y_i))
    
    # testa se encontrou os pontos
    if (len(pt1) == 0) or (len(pt2) == 0):
        return 0, [], [], (0,0), (0,0)
    
    # identifica o pixel central de pt1 e pt2

    # ponto central de pt1
    pt1pxc_x = sum(px[0] for px in pt1) // len(pt1)
    pt1pxc_y = sum(px[1] for px in pt1) // len(pt1)
    pt1pxc = (pt1pxc_x, pt1pxc_y)

    # ponto central de pt2
    pt2pxc_x = sum(px[0] for px in pt2) // len(pt2)
    pt2pxc_y = sum(px[1] for px in pt2) // len(pt2)
    pt2pxc = (pt2pxc_x, pt2pxc_y)

    # calcula a distancia entre os dois pontos
    distancia_pontos = distancia_pixels(pt1pxc, pt2pxc)  

    return distancia_pontos, pt1, pt2, pt1pxc, pt2pxc

def calcula(imagem):
    
    
    imagemHSV = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
    
    LargImg = imagem.shape[1]
    AltImg = imagem.shape[0]

    """Verificações na Img PB, mas saida na imagem colorida"""
    # VAI SO ATE O MEIO DA IMAGEM, na vertical
    ContPontos = 1
    vHSV = []  # acumula os valores de H da imagem
    
    for y in range(0, LargImg):
        for x in range(0, AltImg):
            (H, S, V) = imagemHSV[x, y]
            # print("Valor do S")
            # print(S)
            vHSV.append((H, S, V))
            ContPontos = ContPontos + 1


    VHueMedia = sum(vv[0] for vv in vHSV) // len(vHSV)
    VHueMin = min(vv[0] for vv in vHSV)
    VHueMax = max(vv[0] for vv in vHSV)

    VSMedia = sum(vv1[1] for vv1 in vHSV) // len(vHSV)
    VSMin = min(vv[1] for vv in vHSV)
    VSMax = max(vv[1] for vv in vHSV)

    VVaMedia = sum(vv1[2] for vv1 in vHSV) // len(vHSV)
    VVaMin = min(vv[2] for vv in vHSV)
    VVaMax = max(vv[2] for vv in vHSV)

    print("Hue = Media: ", VHueMedia, "Min: ", VHueMin, "Max: ", VHueMax)
    print("Sat = Media: ", VSMedia, "Min: ", VSMin, "Max: ", VSMax)
    print("Vib = Media: ", VVaMedia, "Min: ", VVaMin, "Max: ", VVaMax)
