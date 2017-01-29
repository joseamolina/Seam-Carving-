'''
Created on Dec 1, 2015

@author: Jose Angel Molina
'''

import tkinter
from copy import deepcopy
from algoritmia.utils import argmin

class PixelColor:
    __slots__ = ("r", "g", "b")
    def __init__(self, r, g ,b):
        self.r, self.g, self.b = r, g, b

class GrayImage:
    __slots__ = ("m", "cols", "rows")
    
    def __init__(self, m):
        if type(m) == type([]):
            self.rows = len(m)
            self.cols = len(m[0])
            self.m = deepcopy(m)
        else:
            raise Exception("BAD PARAMETER")

    def PhotoImage(self, veta=None):
        imageSC = tkinter.PhotoImage(width=self.cols, height=self.rows)
        
        for r in range(self.rows):
            im_row = self.m[r]
            for c in range(self.cols):  
                v = im_row[c]
                imageSC.put("#%02x%02x%02x" % (v,v,v), (c, r))
            if veta != None:
                imageSC.put("#%02x%02x%02x" % (0,255,0), (veta[r], r))
        return imageSC

    def EnergyAsGrayImage(self): 
        minV = 10e100
        maxV = -10e100
        mat=[[0]*self.cols for r in range(self.rows)]
        m = self.m # para escribir menos
        for r in range(1,self.rows-1):
            for c  in range(1,self.cols-1):
                sx = m[r - 1][c -1] + 2 * m[r - 1][c ] + m[r - 1][c +1] - m[r + 1][c -1] - 2 * m[r + 1][c ] - m[r + 1][c +1]
                sy = m[r - 1][c -1] + 2 * m[r][c -1] + m[r + 1][c -1] - m[r - 1][c +1] - 2 * m[r][c +1] - m[r + 1][c +1]
                v = (sx * sx + sy * sy)**0.5
                if v<minV: minV=v
                if v>maxV: maxV=v
                mat[r][c ] = v
            mat[r][0] = mat[r][2]
            mat[r][self.cols-1] = mat[r][self.cols-3]
    
        for c in range(self.cols):
            mat[0][c] = mat[2][c];
            mat[self.rows-1][c] = mat[self.rows - 3][c];
                    
        for r in range(self.rows):
            for c in range(self.cols):
                mat[r][c] = int(255*(mat[r][c]-minV)/maxV)
        return GrayImage(mat)
    
    def QuitarVeta(self, veta):
        if self.cols>1:
            for r in range(self.rows):
                del self.m[r][veta[r]]
            self.cols -= 1
                   
class ColorImage:
    __slots__ = ("m", "cols", "rows", "imageOrig")
    
    def __init__(self, obj):
        if type(obj) == type(""): #carga de fichero
            filename = obj
            self.imageOrig = tkinter.PhotoImage(file = filename)
            self.cols = self.imageOrig.width()
            self.rows = self.imageOrig.height()
            self.m=[[0]*self.cols for r in range(self.rows)]
            for r in range(self.rows):
                for c in range(self.cols):
                    cr,cg,cb = [int(v) for v in self.imageOrig.get(c,r).split()]
                    self.m[r][c] = PixelColor(cr,cg,cb)  
        elif type(obj) == type([]): # carga a partir de una matriz de pixels (p.e. colorImage.m)
            m = obj
            self.rows = len(m)
            self.cols = len(m[0])
            self.m = deepcopy(m)
        else:
            raise Exception("BAD PARAMETER")
        
    def PhotoImage(self):
        imageSC = tkinter.PhotoImage(width=self.cols, height=self.rows)
        
        for r in range(self.rows):
            im_row = self.m[r]
            for c in range(self.cols):
                pc = im_row[c]
                imageSC.put("#%02x%02x%02x" % (pc.r,pc.g,pc.b), (c, r))

        return imageSC

    def ToGrayImage(self):
        grayMat=[[0]*self.cols for r in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                p = self.m[r][c]
                grayMat[r][c] = int(p.r*0.3 + p.g*0.56 + p.b*0.11)
        return GrayImage(grayMat)

    def QuitarVeta(self, veta):
        if self.cols>1:
            for r in range(self.rows):
                del self.m[r][veta[r]]
            self.cols -= 1 
            
# No es necesario modificar el código encima de esta línea:
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

###############
# IMPLEMENT #
###############

def EncontrarVetaDeMenorEnergia(m : "int[rows][cols]") -> "List<int>":
    rows = len(m)
    cols = len(m[0])
    infinity = float('infinity')
    #-encuentra la veta de menor energia y la devuelve como una lista de enteros: el entero en 
    # la posición k, contiene el índice de la columna en la que se encuentra la veta en 
    # la fila k.
    #implementaremos la version iterativa
    #Empezamos de abajo a arriba rellenando la matriz:
    #creamos una matriz
    mat= []
    for i in range (rows): mat.append([(0,infinity,infinity)]*cols)
    
    #Empezamos de abajo a arriba--> de izq a derecha
    for i in range(rows-1,-1,-1):
        for j in range(cols):
            #Para cada posicion, depende donde esta, nos preocupamos de sus 3 colindantes anteriores
            if i == rows-1:
                mat[i][j]=(m[i][j],infinity,infinity)
            else:
                if j == 0:
                    valor1 = mat[i+1][j]
                    valor2 = mat[i+1][j+1]
                    mat[i][j] = min([(valor1[0]+m[i][j],i+1,j), (valor2[0]+m[i][j],i+1,j+1)], key=lambda tupla: tupla[0] )
                elif j == cols-1:
                    valor1 = mat[i+1][j]
                    valor3 = mat[i+1][j-1]
                    mat[i][j] = min([(valor3[0]+m[i][j],i+1, j-1),(valor1[0]+m[i][j],i+1,j)], key=lambda tupla: tupla[0]  )
                else:
                    valor1 = mat[i+1][j]
                    valor2 = mat[i+1][j+1]
                    valor3 = mat[i+1][j-1]
                    mat[i][j] = min([(valor3[0]+m[i][j],i+1,j-1),(valor1[0]+m[i][j],i+1,j), (valor2[0]+m[i][j],i+1 ,j+1)],  key=lambda tupla: tupla[0]    )
    
    #Como es prog dinamica de muchos a muchos, debemos obtener el minimo de todos ellos
    #localizado en la fila 0
    veta = []
    minimo,_,col = mat[0][0]
    
    
    #Obtener el minimo
    for i in range(1,cols):
        peso,_,c = mat[0][i]
        if peso < minimo:
            minimo = peso
            col = c

    veta.append(col)
    _, f, c = mat[0][col]
    
    #Meter indice columna
    for _ in range(1,rows):
        veta.append(c)
        _, f, c = mat[f][c]
        
    return veta

# No es necesario modificar el código debajo de esta línea:
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

def ReducirAnchuraImagen(imagen: "ColorImage", imagenEnergia: "GrayImage", nuevaAnchura: "int") -> "ColorImage":
    width = imagen.cols
    n = width - nuevaAnchura
    primeraveta = None
    for i in range(n):
        veta = EncontrarVetaDeMenorEnergia(imagenEnergia.m)
        if i==0:
           primeraveta = veta 
        imagen.QuitarVeta(veta)
        imagenEnergia.QuitarVeta(veta)
        print("Removed seam {}/{}".format(i+1, n))
    print("Done: {0} pixels width -> {1} pixels width.".format(width, imagen.cols))
    return imagen.PhotoImage(), primeraveta

# PROGRAMA PRINCIAPL --------------------------------------------------------------------------------

# Parámetros principales:
ficheroGIFimagen = 'Castillo400.gif'         
scaleWidth = 0.6

# Crea la ventana gráfica
root = tkinter.Tk()
root.title("Seam Carving")
root.resizable(width=False, height=False)

# Lee la imagen original
cm = ColorImage(ficheroGIFimagen)
imageOrig = cm.PhotoImage()

# Ajusta el tamaño de la ventana gráfica según el tamalo de la imagen original
canvas = tkinter.Canvas(root,borderwidth=0, highlightthickness=0, height=imageOrig.height()*2, 
                        width=imageOrig.width()*2, background="WHITE")
canvas.pack(padx=0,pady=0)

# Muestra la imagen original
canvas.create_image(0, 0, image=imageOrig, anchor="nw")

# Calcula la energia de la imagen
im_energy_original = cm.ToGrayImage().EnergyAsGrayImage()
im_energy = deepcopy(im_energy_original)

# Crea la imagen final resescalada a la nueva anchura
finalWidth = int(imageOrig.width()*scaleWidth)
imageSC, primeraveta = ReducirAnchuraImagen(cm, im_energy, finalWidth)

# Muestra la imagen de la energía (y, en verde, la primera veta eliminada)
# print(primeraveta)
energyImage = im_energy_original.PhotoImage(primeraveta)
canvas.create_image(imageOrig.width(), 0, image=energyImage, anchor="nw")

# Muestra la nueva imagen reescalada
canvas.create_image((imageOrig.width()-finalWidth)/2, imageOrig.height(), image=imageSC, anchor="nw")

root.mainloop()