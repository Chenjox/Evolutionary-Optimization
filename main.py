import math
from math import sin
import numpy as np
import scipy as sci
from scipy.stats import truncnorm
import random
import matplotlib
from matplotlib import pyplot as plt

# Globale Variablen
# Dimension der Zielfunktion
dimension = 3
# Arrays zur Visualiserung:
rectangelXYZ = np.zeros([1,3])
rectangelHeight = np.zeros(1)
rectangleWidth = np.zeros(1)

# Zielfunktion, 
# xVec: ein N-Dimensionaler Vector der Eingangsgrößen
def zf(xVec): 
    return sin(xVec[0]) + 7.0 * sin(xVec[1])**2 + 0.1 * xVec[2]**4 * sin(xVec[0])

def zfMax(xVec):
    return -zf(xVec)

# Nebenbedingungen
# XVec: ein N-Dimensionaler Vector der Eingangsgrößen
# return: Boolean: Wahr wenn keine Verletzt, falsch otherwise

def forceBoundaries(punkte,minBereich,maxBereich):
    for i in range(len(punkte)):
        for j in range(len(punkte[0])):
            if punkte[i,j] < minBereich:
                punkte[i,j] = minBereich
            if punkte[i,j] > maxBereich:
                punkte[i,j] = maxBereich

    return  punkte




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

# mittelpunkt: n array
# maxAbstand: double
# anzahlPunkte: Integer
def getStartpunkte(mittelpunkt,maxAbstand,anzahlPunkte):
    p = randomPointsInBox(0,maxAbstand,anzahlPunkte)
    for i in range(0,anzahlPunkte):
        p[i] = mittelpunkt + p[i]
    return p


def dataToVisualize(XYZ, Height, Width):
    # Arrays zur Visualiserung:
    global rectangleWidth, rectangelXYZ
    rectangelXYZ = np.vstack((rectangelXYZ, XYZ))
    rectangleWidth = np.append(rectangleWidth, Width)

# startPoint: N-Dimensionaler Vector
# minMax: Boolean ob minimum oder Maximum gesucht ist

def optimize(isMaximumsuche,anzahlStartPunkte, minBereich,maxBereich,minSuchbereich,maxSuchbereich,verkleinerungsfaktor):

    minSB = minSuchbereich
    maxSB = maxSuchbereich
    momentanePunkte = getStartpunkte((minBereich+maxBereich)/2, (maxBereich-minBereich)/2, anzahlStartPunkte)
    vergleichswert = -math.inf
    maxIter = 1000
    itere = 0
    while itere < maxIter:
        #Selektion
        anzahlPunkte = momentanePunkte.shape[0]
        fitness = np.zeros((anzahlPunkte,1))
        for i in range(0,anzahlPunkte):
            if isMaximumsuche:
                fitness[i] = zf(momentanePunkte[i])
            else:
                fitness[i] = zfMax(momentanePunkte[i])
        # https://stackoverflow.com/a/19932054 FIXME do not sort if all are equal
        fitness, punkte = map(list, zip(*sorted(zip(fitness, momentanePunkte), reverse=True)))
    
        # War der Jahrgang gut?
        bestOf = 0
        for i in range(0,anzahlPunkte):
            if fitness[i] > vergleichswert:
                bestOf = bestOf + 1
        print(bestOf, bestOf/anzahlPunkte)
        # Erfolgsregel
        if bestOf/anzahlPunkte >= 0.2:
            if abs(fitness[0] - vergleichswert) < 1e-10:
                momentanePunkte = punkte
                break
            elternpunkt = punkte[0]
            vergleichswert = fitness[0]
            #Mutation
            #print(elternpunkt)
            suchpunkte = randomPointsInBox(minSB,maxSB,anzahlStartPunkte)
            momentanePunkte = elternpunkt + suchpunkte

            print(momentanePunkte)
        else:
            minSB, maxSB = modifySuchbox(minSB, maxSB, verkleinerungsfaktor)
            suchpunkte = randomPointsInBox(minSB,maxSB,anzahlStartPunkte)
            momentanePunkte = elternpunkt + suchpunkte
            print("Ich verkleinere mich!")


            #Speichern der relevanten Daten zur Visualiserung
            dataToVisualize(punkte[0], maxSuchbereich, maxSuchbereich)

        momentanePunkte = forceBoundaries(momentanePunkte,minBereich,maxBereich)
        itere = itere + 1
        

    return momentanePunkte[0]

## Erster Suchbereich ist abhängig von dem Eingangsraum.

## Hauptprogramm

#zfOpt = optimize()

p = optimize(True,5,-math.pi,math.pi, 0.1,0.8 ,0.3)
print(p)



#Visualisierung
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
plt.xlim([-1, 3])
plt.ylim([-1, 3])
n = 10
#(np.size(rectangleWidth))
for i in range(1, n):
    x = rectangelXYZ[i, 0]
    y = rectangelXYZ[i, 1]
    w = rectangleWidth[i]
    ax.add_patch(matplotlib.patches.Rectangle((x, y), w, w, fill=None, alpha=1))
plt.show()