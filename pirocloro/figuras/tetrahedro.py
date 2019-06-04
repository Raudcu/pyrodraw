from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from matplotlib import colors as mcolors

import numpy as np

from itertools import combinations


'''
:class: 'Tetrahedro'. Clase para el dibujo de Tetrahedros de a pares (uno 'Up' y uno 'Down') en la dirección [111], a partir del centro del 'Up' y el lado 'L' del cubo en el que se inscribe. Lo armo dibujando las cuatro caras triangulares de cada Tetrahedro. Además se puede pasar como parámetro el valor de alpha para los bordes ('edge_alpha').
'''

class Tetrahedro:     
    
    # Inicializo
    def __init__(self, centro, L, edge_alpha=0.1):
        self.centro = centro
        self.L = L

        self.edge_alpha = edge_alpha
        
        self.calcula_vertices()
        self.calcula_caras()
        self.dibuja_caras()
    
    
    # Método para el cálulo de los vértices. Se corresponde a sumarle a 'centro' las posiciones de los vértices del Tetrahedro 'Up' respecto a su centro.
    def calcula_vertices(self):
        self.vertices = self.centro + self.L/2 * np.array([[1, 1, 1], [1, -1, -1], [-1, -1, 1], [-1, 1, -1]]) 
   

    # Método para encontrar los vértices de cada cara triangular del Tetrahedro.
    def calcula_caras(self):
        
        self.vert_up = [] # Vértices de las caras del Tetrahedro Up.
        self.vert_down = [] # Vértices de las caras del Tetrahedro Down.
        
        
        # Con este loop se consideran todas las maneras de tomar de a tres puntos entre los cuatro vértices del Tetrahedro, o sea, los vértices de cada cara triangular.
        for cara in combinations(range(4), 3):
            vert_x = list(self.vertices[list(cara),0]) # Las tres posiciones x de cada vértice de la cara triangular.
            vert_y = list(self.vertices[list(cara),1]) # Las tres posiciones y de cada vértice de la cara triangular.
            vert_z = list(self.vertices[list(cara),2]) # Las tres posiciones z de cada vértice de la cara triangular.
        
            self.vert_up.append( [list(zip(vert_x, vert_y, vert_z))] )
            
            # Las caras del Tetrahedro down se arman invirtiendo los valores de los vértices y trasladándolos.
            self.vert_down.append( [list(zip(list( -np.array(vert_x) + 2*self.vertices[0,0] ),
                                list( -np.array(vert_y) + 2*self.vertices[0,1] ),
                                list( -np.array(vert_z)) + 2*self.vertices[0,2] ))] )
                        
                
    # Método par dibujar las caras de ambos Tetrahedros a partir de los vértices de sus caras. 
    def dibuja_caras(self):
        
        self.caras = []
            
        for i, cara_up, cara_down in zip(range(4), self.vert_up, self.vert_down):
            self.caras.append(Poly3DCollection(cara_up, 
                                               facecolors = mcolors.to_rgba('mediumpurple', alpha=0.1 + i*0.1),
                                               edgecolors = mcolors.to_rgba('gray', alpha=self.edge_alpha)))
            
            self.caras.append(Poly3DCollection(cara_down, 
                                               facecolors = mcolors.to_rgba('lightskyblue', alpha=0.1 + i*0.1),
                                               edgecolors = mcolors.to_rgba('gray', alpha=self.edge_alpha)))

            

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from copy import deepcopy

    from cubo import Cubo

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    t = Tetrahedro([0,0,0], 0.5)

    for cara in t.caras:
        ax.add_collection3d(deepcopy(cara), zs='z')

    ax.scatter(*np.hsplit(t.vertices,3), s=0)

    
    ax.set_aspect('equal')
    ax.view_init(20,-75)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.show()
