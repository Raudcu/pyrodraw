from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from matplotlib import colors as mcolors

import numpy as np

from itertools import product, combinations


'''
:class: 'Paralelepipedo'. Clase para el dibujo de Paralelepipedos a partir de sus lados ('L') y la posición de uno de sus vértices ('vert'). Lo armo dibujando las seis caras. Además se puede pasar como parámetro el valor de alpha para las caras ('face_alpha'), el color de los bordes de las caras ('edge_color') y el grosor de los bordes de las caras ('line_width').
'''

class Paralelepipedo:

    # Inicializo
    def __init__(self, L=[1,1,1], vert=[0,0,0], face_alpha=0, edge_color='black', line_width=1.5):
        self.L = L
        self.vert = vert

        self.calcula_vertices()
        self.calcula_caras()

        self.dibuja_caras(face_alpha, edge_color, line_width)
    
    
    # Método para el cálculo de los vértices. Se corresponde a trasladar el vértice en [0,0,0] en 'vert'.
    def calcula_vertices(self):
        self.vertices = self.vert + np.array(list(product([0, self.L[0]], [0, self.L[1]], [0, self.L[2]])))
   

    # Método para encontrar los vértices de cada cara del Paralelepipedo.
    def calcula_caras(self):
        
        self.vert_caras = [] # Vértices de las caras del Paralelepipedo.
        
        
        # Con este loop se consideran las seis maneras que corresponden de tomar de a cuatos puntos entre los ocho vértices del Paralelepipedo.
        faces = [(2,0,1,3), (0,4,5,1), (0,4,6,2), (1,5,7,3), (6,2,3,7), (4,6,7,5)]
        
        for cara in faces:
            vert_x = list(self.vertices[list(cara),0]) # Las cuatos posiciones x de cada vértice de la cara.
            vert_y = list(self.vertices[list(cara),1]) # Las cuatos posiciones y de cada vértice de la cara.
            vert_z = list(self.vertices[list(cara),2]) # Las cuatos posiciones z de cada vértice de la cara.
        
            self.vert_caras.append( [list(zip(vert_x, vert_y, vert_z))] )
                        
                
    # Método par dibujar las caras del Paralelepipedo a partir de los vértices de sus caras. 
    def dibuja_caras(self, face_alpha, edge_color, line_width):
        
        self.caras = []
            
        for cara in self.vert_caras:
            self.caras.append(Poly3DCollection(cara, facecolors = mcolors.to_rgba('gray', alpha=face_alpha), edgecolors=edge_color, lw=line_width))


            
if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from copy import deepcopy


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    c = Paralelepipedo(np.array([1,2,3])*np.sqrt(2)*2, [1,1,1], 0.2, 'red', 2)

    for cara in c.caras:
        ax.add_collection3d(deepcopy(cara), zs='z')

    ax.scatter3D(*np.hsplit(c.vertices,3), s=60)

    
    ax.set_aspect('equal')
    ax.view_init(20,-75)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.show()
