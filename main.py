
import numpy as np

# Globale Variablen
# Dimension der Zielfunktion
dimension = 3

# Zielfunktion, 
# xVec: ein N-Dimensionaler Vector der Eingangsgrößen
def zf(xVec): 

    return 0.0

# Nebenbedingungen
# XVec: ein N-Dimensionaler Vector der Eingangsgrößen
# return: Boolean: Wahr wenn keine Verletzt, falsch otherwise
def checkNB(xVec):
    return True

# Generiert normalverteilte Punkte im Suchraum
# minAbstand Double
# maxAbstand Double
# dimension Integer
# return n x dimension Numpy Array
def randomPointsInBox(minAbstand, maxAbstand, dimension):
    return np.zeros(2,dimension)

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

zfOpt = optimize()