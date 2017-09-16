import numpy as np
from laspy.file import File
from eina_to_voxels.openStreetMap import openStreetMap
import colorsys
import worldDTO
from pcloudproc.pcloudproc import *
from PIL import Image



class World:
    
    def __init__(self, src, src2, x1, y1, x2, y2):
        
        self.osm = openStreetMap.OpenStreetMap()
        self.heuristics = []
        
        # Lee fichero .las cuya ruta está en src
        inFile = File(src, mode = "r")
        
        xMin = min(inFile.x)
        yMin = min(inFile.y)
        zMin = min(inFile.z)
        
        xMax = max(inFile.x)
        yMax = max(inFile.y)
        zMax = max(inFile.z)
        
        

        if src2 != None:
            print("hola")
            coords = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()

            img = Image.open(src2)


            pixelX_size = (x2 - x1)/img.size[0]
            pixelY_size = (y2 - y1)/img.size[1]


            rgb_img = img.convert('RGB')

            red = []
            green = []
            blue = []

            for coord in coords:

                x = (coord[0]-x1)/pixelX_size
                y = (coord[1]-y1)/pixelY_size
                rgb = rgb_img.getpixel((int(x), int(y)))

                red.append(rgb[0]*255)
                green.append(rgb[1]*255)
                blue.append(rgb[2]*255)

            rgb = (red, green, blue)
            print("adios")

        # Modificar el brillo de los colores
        rgb = changeBrightness(inFile.Red,inFile.Green,inFile.Blue)
        
        # Se guardan las coordenadas en la variable coord como una unica lista de coordenadas (x, y, z)
        coords = np.vstack((inFile.x, inFile.y, inFile.z, rgb[0],rgb[1],rgb[2])).transpose()
        
        
        # Numero de celdas para x, y, z
        # La cuenta solo funciona porque se asume que las coordenadas están en metros y que
        # queremos 1 metro por celda. Al menos la segunda debería ser un parámetro
        resolution = (int(round(xMax - xMin)), int(round(yMax - yMin)), int(round(zMax - zMin)))
    
        # Esquinas max y min de la estructura
        bcube = {'min': (xMin, yMin, zMin),'max': (xMax, yMax, zMax)}
        
        
        print("Creando matriz")
    
        
        self.matrix = sparse_matrix_from_pointcolors(coords, resolution, bcube)



    def add(self, heuristic):
        self.heuristics.append(heuristic)   
        
        
    def start(self):
        w = worldDTO.WorldDTO(self.matrix)
        
        for h in self.heuristics:
            w = h.apply(w)
        self.matrix = w.matrix
                
    """
    dest is the path of the file where the program exports the world 
    """
    def exportWorld(self,dest):
        f = open(dest, 'w')
        
        
        resolution = self.matrix.resolution
        for x in range (0,resolution[0],30):
            for y in range (0,resolution[1],30):
                for z in range (0,resolution[2],30):
                    for i in range(0,30):
                        for j in range(0,30):
                            for k in range(0,30):
                                #print (x+i,y+j,z+k)
                                if (x+i,y+j,z+k) in self.matrix.values:
                                    cell = (x+i,y+j,z+k)
                                    #print cell
                                    f.write("%d %d %d %d\n" % (resolution[0]-cell[0],cell[1],cell[2],self.matrix.values[cell][1]))
                       
        
        f.close()
        
        
"""
Change color brightness for a rgb tuple
red, green and blue are nunpy arrays (CREO) 
"""
def changeBrightness(red,green,blue):
    rgb = np.vstack((red, green, blue)).transpose()
    hsv = [ colorsys.rgb_to_hsv(h[0]/65025., h[1]/65025., h[2]/65025.) for h in rgb]
    
    rgb = [ colorsys.hsv_to_rgb(h[0], h[1], h[2] + 0.2*((1-h[2])**2)) for h in hsv]
    
    red = [ int(h[0]*255) for h in rgb]
    green = [ int(h[1]*255) for h in rgb]
    blue = [ int(h[2]*255) for h in rgb]
    
    return (red, green, blue)


def sparse_matrix_from_pointcolors(pointcolors_iterator, resolution, bcube):
    """
    Deduzco que:
    - crea una SparseMatrix vacía de la resolución y bounding cube que le decimos
    - coge un iterador de tuplas (x,y,z,r,g,b) (sacado de un LAS p.ej.)
    - calcula la celda de cada x,y,z (ncell)
    - si esta celda no la tenemos ya en matrix , calcula un color cercano para ella (el cómo
      exactamente me cuesta seguirlo, es a base de números mágicos, el color es entre 1 y 16)
      y guarda en su value una tupla (1, el color mejor (salvo si sale 13 o 5 que guarda 16), scores)
       (y no sé por qué guarda scores, que parece
      ser la distancia entre el color del punto que está considerado y todos los que tiene
      en el vector mágico colors
    - devuelve el matrix así calculado
    """
    colors = [(221, 221, 221, 1), (219, 125, 62, 1.2), (179, 80, 188, 1.4),
              (107, 138, 201, 4), (177, 166, 39, 1), (65, 174, 56, 1.1),
              (208, 132, 153, 1.1), (64, 64, 64, 4), (154, 161, 161, 1.4),
              (46, 110, 137, 1.4), (126, 61, 181, 4), (46, 56, 141, 4),
              (79, 50, 31, 1.1), (53, 70, 27, 1.1), (150, 52, 48, 1.4), (25, 22, 22, 2)]

    scores = []
    matrix = SparseMatrix({}, resolution, bcube)
    for pc in pointcolors_iterator:
        ncell = coords_to_cell(pc[0:3], resolution, bcube)
        if ncell not in matrix.values:

            for color in colors:
                scores.append(math.sqrt(
                    math.pow(color[0] - pc[3], 2) + math.pow(color[1] - pc[4], 2) + math.pow(
                        color[2] - pc[5], 2)) * color[3])

                # scores.append((abs((color[0]-coords[3]))+abs((color[1]-coords[4]))+abs((color[2]-coords[5])))*color[3])
            if ncell[2] > 6:
                scores[5] = scores[5] * 4
                scores[4] = scores[4] * 4
                scores[12] = scores[12] * 4
                scores[14] = scores[14] * 4
                scores[9] = scores[9] * 1.1
                # scores[12] = scores[12]*4
                scores[13] = scores[13] * 4
            else:
                scores[9] = scores[9] * 4
                scores[11] = scores[11] * 4

            min = scores[0]
            best = 0
            for i in range(0, 16):
                if (scores[i] < min):
                    min = scores[i]
                    best = i

            if ((best == 13) | (best == 5)):
                matrix.values[ncell] = (1, 16, scores)
            else:
                matrix.values[ncell] = (1, best, scores)
            scores = []
    return matrix