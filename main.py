import math
import numpy as np
import scipy as sci
from scipy.stats import truncnorm
import random

# Globale Variablen
# Dimension der Zielfunktion
dimension = 3

# Zielfunktion, 
# xVec: ein N-Dimensionaler Vector der Eingangsgrößen
def zf(xVec): 
    return sin(xVec[0]) + 7.0 * sin(xVec[1])**2 + 0.1 * xVec[2]**4 * sin(xVec[0])

# Nebenbedingungen
# XVec: ein N-Dimensionaler Vector der Eingangsgrößen
# return: Boolean: Wahr wenn keine Verletzt, falsch otherwise
def checkNB(xVec):
    isinrangeNB = True
    for i in range(xVec.size()):
        if xVec[i] < -math.pi or xVec[i] > math.pi:
            isinrangeNB = False

    return isinrangeNB

# https://stackoverflow.com/a/44308018
def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

# Generiert normalverteilte Punkte im Suchraum
# minAbstand Double
# maxAbstand Double
# anzahl: Anzahl Kindpunkte
# dimension Integer
# return n x dimension Numpy Array
def randomPointsInBox(minAbstand, maxAbstand, anzahl):
    result = np.zeros((anzahl,dimension))
    for i in range(0,anzahl):
        normalDist = get_truncated_normal((minAbstand + maxAbstand)/2, 1, minAbstand, maxAbstand)
        w = normalDist.rvs(dimension)
        for j in range(0,dimension):
            vorzeichen = random.randint(1,2)
            w[j] = (-1)**(vorzeichen) * w[j]
        #print(w)
        result[i] = w
    return result

# Modifiziert die Suchbox
# minAbstand Double
# maxAbstand Double
# factor: Verkleinerungsfaktor
# return Tuple mit minAbstand, maxAbstand
def modifySuchbox(minAbstand, maxAbstand, factor):
    return (minAbstand * factor, maxAbstand * factor)

# startPoint: N-Dimensionaler Vector
# minMax: Boolean ob minimum oder Maximum gesucht ist
def optimize(startPoint, minMax): 
    return 0.0

## Erster Suchbereich ist abhängig von dem Eingangsraum.


## Hauptprogramm

#zfOpt = optimize()

print(randomPointsInBox(1.0,10.0,10))