import numpy as np
from scipy.linalg import norm

from ..figuras.tetrahedro import Tetrahedro
from ..figuras.cubo import Cubo

from ..piezas.spines import Spines
from ..piezas.monopolo import Monopolo


'''
:class: 'CeldaUnidad'. Clase para construir todos los elementos de una celda unidad a partir de su posición particular 'ijk', las posiciones de los spines en 'posiciones' y sus valores de spin en 'spin_values'.
'''

class CeldaUnidad:

    # Base de la red FCC
    base_fcc = 0.5 * np.array([[0, 0, 0], [1, 1, 0], [0, 1, 1], [1, 0, 1]])
    

    #Inicializo
    def __init__(self, ijk, posiciones, spin_values):
        self.i = ijk[0]
        self.j = ijk[1]
        self.k = ijk[2]
        
        self.centros_up = (CeldaUnidad.base_fcc + ijk)  / (np.sqrt(2)/4)
        self.centros_down = self.centros_up + np.array([1,1,1])/np.sqrt(2)

        _L = round((len(spin_values)/16)**(1/3))
        self.spin_inicial = ( self.i + self.j*_L + self.k*_L*_L ) * 16


        # Cubo
        self.cubo = Cubo(np.sqrt(8), np.array(ijk)*np.sqrt(8))
        

        # Tetrahedros
        self.tetrahedros = [ Tetrahedro(centro, np.sqrt(0.5)) for centro in self.centros_up ]
        

        # Spines 
        self.spines = [ Spines(posiciones[i:i+4], spin_values[i:i+4])
                        for i in range(self.spin_inicial, self.spin_inicial+16, 4) ]


        # Monopolos
        ## Tetrahedros Up
        self.monopolos = [ Monopolo(centro, -int(sum( spin_values[i:i+4] )))
                          for centro, i in zip(self.centros_up, range(self.spin_inicial, self.spin_inicial+16, 4)) ]

        ## Tetrahedros Down
        for centro, i in zip(self.centros_down, range(self.spin_inicial, self.spin_inicial + 16, 4)):
            _spines_down = CeldaUnidad.tetra_down(i, posiciones, _L)
            
            self.monopolos.append( Monopolo(centro, int(sum( spin_values[_spines_down] ))) )


    @staticmethod
    # Método para dado un spin apical de un Tetrahedro Up, determinar los vecinos con los que conforma el Down.
    def tetra_down(i, posiciones, L):

        # Caja
        box = L * np.sqrt(8)
      

        # Calculo r_ij para todos los spines respescto del spin i considerando condiciones de contorno periódicas.
        r_ij = []
    
        for pos in posiciones:
            aux = pos - posiciones[i]
            r_ij.append( aux - np.around(aux/box)*box )
        
        r_ij = np.array(r_ij)
        

        # Calculo las distancias entre el spin i y el resto.
        distancias = np.apply_along_axis(lambda x: norm(x), 1, r_ij)


        # Determino quienes son los primeros vecinos del spin i ordenando las distancias y quedándome con los seis siguientes.
        vecinos = np.argsort(distancias)[1:7]


        # Los vecinos con los que el spin i forma el Tetrahedro Down son los tres que tienen todas las componentes de r_ij al menos más grande que -np.sqrt(2)/4: dos vecinos, en posición fija, siempre tienen una de las tres componentes de rij igual a 0 y las otras dos con módulo igual a raíz de dos sobre dos (lo cual me asegura una distancia entre primeros vecinos igual a 1). Para ser conservativo, ya que los spines se pueden mover de su posición de equilibrio, pido que las componentes sean mayor a raíz de dos sobre cuatro en lugar de pedir que sean mayor a cero (porque de hecho a veces, debido a las distorsiones, no lo son).
        vecinos_down = vecinos[ np.apply_along_axis(lambda x: np.all(x>=-np.sqrt(2)/4), 1, r_ij[vecinos]) ]


        # Retorno el array de vecinos_down con el spin i insertado al principio.                       
        return np.insert(vecinos_down, 0, i)



if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from copy import deepcopy

    import sys

    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    filename = sys.argv[1]
    c = CeldaUnidad(filename, [0,0,0])

    
    # Cubo
    for cara in c.cubo.caras:
        ax.add_collection3d(deepcopy(cara), zs='z')


    for edge in deepcopy(c.cubo.bordes):
        ax.plot3D(*edge, color='black', lw=2)      

    
    # Tetrahedros
    for tetrahedro in c.tetrahedros:

        for cara in tetrahedro.caras:
            ax.add_collection3d(deepcopy(cara), zs='z')


    # Spines
    for spines in c.spines:
        ax.quiver(*np.hsplit(tetrahedro.vertices,3), *np.hsplit(spines.vectores,3), 
                  length=0.2, arrow_length_ratio=0.5, pivot='middle', normalize=True,            
                  capstyle='round', colors=spines.colores, lw=2)
    

    # Monopolos
    for monopolo in deepcopy(c.monopolos):

        if monopolo.radio!=0:
            x, y, z = zip(*monopolo.coordenadas)
            ax.plot_surface(np.array(x), np.array(y), np.array(z), color=monopolo.color)


    ax.set_aspect('equal')
    ax.view_init(20,-75)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.show()            
