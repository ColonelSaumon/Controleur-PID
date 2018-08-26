# -*- coding: utf-8 -*-
"""
    CorrecteurPID.py
    ================
    
    Auteur : Godefroy Borduas
    Email : godefroy.borduas@umontreal.ca
    Date : 26 août 2018
"""

import numpy as np
import matplotlib.pyplot as plt

def pid(x, Kp, Ki, Kd) :
    """
        Calcul la correction du contrôleur en fonction
        de la variable d'environnement x (qui peut être la possition,
        le temps, la température, la lumière, etc.)
            x = variable d'environnement
            Kp = Constante du correcteur proportionnel
            Ki = Constante du correcteur intégrale
            Kd = Constante du correcteur dérivé
    """
    return Kp + Ki/x + Kd*x

def correction(err, x, Kp, Ki, Kd):
    """
        Calcul la fonction de commende du correcteur (u(t)) en fonction
        de la variablew d'environnement x (qui peut être la possition,
        le temps, la température, la lumière, etc.)
            err = erreur entre la commande d'environnement et la consigne
            x = variable d'environnement
            Kp = Constante du correcteur proportionnel
            Ki = Constante du correcteur intégrale
            Kd = Constante du correcteur dérivé
    """
    return err*pid(x, Kp, Ki, Kd)

def Correcteur(cons, x, fct_transf, Kp, Ki, Kd):
    """
        Calcule l'effet du correcteur sur l'environnement à partir de la
        consigne, de la variable d'environnement et de la fonction de
        transfère propre au correcteur.
            cons = Consigne apporter à l'environnement
            x = variable d'environnement
            fct_transf = fonction python représentant l'actionneur du système
                doit accepter en paramètre la variable d'environnement
                uniquement
            Kp = Constante du correcteur proportionnel
            Ki = Constante du correcteur intégrale
            Kd = Constante du correcteur dérivé
    """
    return correction(cons - x, x, Kp, Ki, Kd)*fct_transf(x)

########################################
#    fonction de la simulation main
########################################
    
def Trans_unique(x) :
    print(x)
    return x

def Transfere(x) :
    """
        Fonction de transfère selon la méthode de Strejc
            G0 = gain de vitesse
            tau et n = paramètres
    """
    return G0/(x*(1+tau*x)**n)

def Linear(p1, p2) :
    """
        Calcul la fonction linéaire représenter par les points désirée
        p1 = point 1 (x, y)
        p2 = point 2 (x, y)
    """
    pente = (p2[1] - p1[1])/(p2[0] - p1[0])
    return pente, (p2[1] - pente*p2[0])

def CalculFonction(Delta, p1, p2) :
    """
        Calcul les points y de la fonction linéaire désirer selon le pas
        de calcul (Delta) et les points p1 et p2.
    """
    y = []
    m, b = Linear(p1, p2)
    x = p1[0]
    if (m*x + b) != p1[1] :
        raise "Il semblerait que la fonction linéaire n'est pas bien calculée."
    while x <= p2[0] :
        y.append(m*x + b)
        x += Delta
        
    return y

def AddToListFromList(l1, l2) :
    """
        Ajoute les éléments de la liste l2 à la liste l1
    """
    return np.append(np.array(l1), np.array(l2))

if __name__ == '__main__' :
    G0 = 1
    tau = 1/1000
    n = 2
    
    # Pas de calcul de la simulation
    pas = 1
    
    # Couple de point de température désirée (temps en minute)
    target = [(0, 22),
               (45, 150),
               (100, 150)]
    # Calul de la fonction de consigne
    consigne = []
    consigne = AddToListFromList(consigne, CalculFonction(pas, target[0], target[1]))
    consigne = AddToListFromList(consigne, CalculFonction(pas, target[1], target[2]))
    temps = np.arange(target[0][0], target[2][0] + 2)
    
    # Température en fonction du temps
    y = [float(target[0][1]) - 2]
    # Erreur en fonction du temps
    erreur = []
    # Évolution de la consigne
    for i in range(0, len(consigne)) :
        erreur.append(consigne[i] - y[-1])
        y.append(Correcteur(consigne[i], y[-1], Transfere, 1, 0, 0))
    
    
    y = np.array(y)
    erreur = np.array(y)
    
    # Graphique de la simulation
    #temps /= 60     # Pour l'avoir en minute    
    # Affichage de la consigne
    plt.figure()
    plt.title('Simulation de la correction PID')
    plt.plot(temps[:2], consigne[:2], 'b-', label='consigne')
    plt.plot(temps[:2], y[:2], 'k--', label='Temperature')
    plt.xlabel('temps (minutes)')
    plt.ylabel('température (celsius)')
    plt.legend(loc='best')
    
    # Affichage de l'erreur
    plt.figure()
    plt.title('Simulation erreur de la correction PID')
    plt.plot(temps[:2], erreur[:2], 'b-')
    plt.xlabel('temps (minutes)')
    plt.ylabel('température (celsius)')
    
    plt.show()