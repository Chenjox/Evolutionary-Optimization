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
samplePoints = np.zeros([1,3])
bestChain = np.zeros([1,3])
# Zielfunktion, 
# xVec: ein N-Dimensionaler Vector der Eingangsgrößen
def zf(xVec): 
    global samplePoints
    samplePoints = np.vstack((samplePoints,xVec))
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
        # Zufälliger Punkt im Einheitswürfel
        punkt = np.zeros((dimension))
        for j in range(0,dimension):
            punkt[j] = random.uniform(-1.0,1.0)
        # Zufällige Projection in eine Richtung
        richtung = random.randint(0,dimension-1)
        vorzeichen = random.randint(1,2)
        punkt[richtung] = (-1)**(vorzeichen)
        normalDist = get_truncated_normal((minAbstand + maxAbstand)/2, 1, minAbstand, maxAbstand)
        w = normalDist.rvs(1)

        #print(w)
        result[i] = w*punkt
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

# startPoint: N-Dimensionaler Vector
# minMax: Boolean ob minimum oder Maximum gesucht ist

def optimize(isMaximumsuche,anzahlStartPunkte, anzahlKetten,minBereich,maxBereich,minSuchbereich,maxSuchbereich,verkleinerungsfaktor):
    global bestChain
    bestPoint = np.zeros(3)
    bestFitness = -math.inf
    for k in range(0,anzahlKetten):
        minSB = minSuchbereich
        maxSB = maxSuchbereich
        momentanePunkte = getStartpunkte((minBereich+maxBereich)/2, (maxBereich-minBereich)/2, anzahlStartPunkte)
        vergleichswert = -math.inf
        chain = np.zeros([1,3])
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
            # Fix with help of ChatGPT....
            sortIndices = np.argsort(fitness)
            fitness = fitness[sortIndices]
            punkte = momentanePunkte[sortIndices]
            # fitness, punkte = map(list, zip(*sorted(zip(fitness, momentanePunkte), reverse=True)))

            # War der Jahrgang gut?
            bestOf = 0
            for i in range(0,anzahlPunkte):
                if fitness[i] > vergleichswert:
                    bestOf = bestOf + 1
            #print(bestOf, bestOf/anzahlPunkte)
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

                #print(momentanePunkte)
            else:
                minSB, maxSB = modifySuchbox(minSB, maxSB, verkleinerungsfaktor)
                suchpunkte = randomPointsInBox(minSB,maxSB,anzahlStartPunkte)
                momentanePunkte = elternpunkt + suchpunkte
                #print("Ich verkleinere mich!")


            #Speichern der relevanten Daten zur Visualiserung
            chain = np.vstack((chain,punkte[0]))

            momentanePunkte = forceBoundaries(momentanePunkte,minBereich,maxBereich)
            itere = itere + 1
        if vergleichswert > bestFitness:
            bestPoint = momentanePunkte[0]
            bestChain = chain
            bestFitness = vergleichswert
    print(bestFitness)
    return bestPoint

## Erster Suchbereich ist abhängig von dem Eingangsraum.

## Hauptprogramm

#zfOpt = optimize()

p = optimize(True,20,30,-math.pi,math.pi, 1,3 ,0.6)
print(p)

#Visualisierung
fig = plt.figure()
#122
bs = fig.add_subplot(122, projection='3d')

x = samplePoints[:,0]
y = samplePoints[:,1]
z = samplePoints[:,2]

bs.scatter(x,y,z)
bs.set_xlim3d(-math.pi, math.pi)  # Set x-axis range
bs.set_ylim3d(-math.pi, math.pi)  # Set y-axis range
bs.set_zlim3d(-math.pi, math.pi)

print(len(samplePoints))
# Beste Linie an Punkten
ax = fig.add_subplot(121, projection='3d')

fx = bestChain[:,0]
fy = bestChain[:,1]
fz = bestChain[:,2]
ax.plot(fx,fy,fz,c='red')

ax.set_xlim3d(-math.pi, math.pi)  # Set x-axis range
ax.set_ylim3d(-math.pi, math.pi)  # Set y-axis range
ax.set_zlim3d(-math.pi, math.pi)

plt.show()