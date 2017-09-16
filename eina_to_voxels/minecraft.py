#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pcloudproc.pcloudproc import *

"""
Some Minecraft specific functions
"""

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