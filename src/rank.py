__author__ = 'Lorenzo de la Paz'


from math import log

#Parametros constantes
N = 50000
k1 = 1.2
k2 = 100
b = 0.0
R = 0.0
r = 0.0

#Funcion que calcula la puntuación en base a la función de ranking BM25
def score_BM25(n, f, qf, dl, avdl):
    K = compute_K(dl, avdl)
    #print('valor de K:', str(K))
    first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
    #print('first referencia: ', first)
    
    second = ((k1 + 1) * f) / (K + f)
    #print('second referencia: ', second)
    
    third = ((k2+1) * qf) / (k2 + qf)
    #print('third referencia: ', third)
    return first * second * third

#Funcion que calcula el valor del parametros K
def compute_K(dl, avdl):
    return k1 * ((1-b) + b * (float(dl)/float(avdl)) )