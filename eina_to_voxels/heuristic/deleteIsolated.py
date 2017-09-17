from heuristic import heuristic
from copy import deepcopy

class DeleteIsolated(heuristic.Heuristic):
    
    def __init__(self, param):
        super(DeleteIsolated,self).__init__(param)
        
    """
    if a block does not have any block in his 26 block neighborhood, delete that block
    """
    def apply(self,world):
        # Al pasar a Python 3 esto ya no funciona, se queja de que un diccionario
        # no puede cambiar durante una iteración, lo reescribo (rápidamente, requiere revisarlo más tranquilamente
        # y algún test)
        # matrix = world.matrix
        #
        # cells = matrix.values.keys()
        # for (i,j,k) in cells:
        #     if matrix.neighbor_26((i,j,k)) == None:
        #         del matrix.values[(i,j,k)]
        #
        #
        # return world
        matrix = world.matrix
        newmatrix = deepcopy(world.matrix)
        cells = matrix.values.keys()
        for (i,j,k) in cells:
            if matrix.neighbor_26((i,j,k)) == None:
                del newmatrix.values[(i, j, k)]
        world.matrix = newmatrix
        return world
