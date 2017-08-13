from random import random, sample
from bisect import bisect
from collections import deque
import csv
import math

class Partida():
    def __init__(self, jugadores, menLen, emparejamientos, senales, s, b, x, m):
        self.emparejamientos = emparejamientos
        self.senales = senales
        self.s = s
        self.b = b
        self.x = x
        self.m = m
        self.jugadores = {nombre: Partida.Jugador(menLen)
                            for pareja in emparejamientos[0]
                                for nombre in pareja}
        self.memoria = list()


    def generar_senales(self):

        def with_b(muestra, observa, s, r):
            if not (muestra == observa == 0):
                result = ((0.98) * (1.0 - self.b) * (1.0 - self.x) * muestra/r) + ((0.98) * (1.0 - self.b) * (self.x) * observa/r) + ((0.98) * self.b * s) + ((self.m / 8))
            else:
                result = ((0.98) * (1.0 - 0) * (1.0 - self.x) * muestra/r) + ((0.98) * (1.0 - 0) * (self.x) * observa/r) + ((0.98) * 0 * s) + ((self.m / 8))
            return result

        def choice(opciones, probs):
            probAcumuladas = list()
            aux = 0
            for p in probs:
                aux += p
                probAcumuladas.append(aux)
            r = random() * probAcumuladas[-1]
            op = bisect(probAcumuladas, r)
            return opciones[op]

        yield dict(zip(self.jugadores.keys(), self.senales))


        r = 1
        while True:
            eleccs = dict.fromkeys(self.jugadores.keys())
            for nombre, inst in self.jugadores.items():
                probs = [with_b(inst.mem_mostradas.count(op), inst.mem_observadas.count(op), self.s[indx], r)
                            for indx, op in enumerate(self.senales)]
                eleccs[nombre] = choice(self.senales, probs)
            r += 1
            yield eleccs


    def jugar(self):
        gen_sens =  self.generar_senales()
        for n, ronda in enumerate(self.emparejamientos):
            senales = next(gen_sens)
            self.memoria.append(senales)

            for jugador1, jugador2 in ronda:
                self.jugadores[jugador1].mem_observadas.append(senales[jugador2])
                self.jugadores[jugador2].mem_observadas.append(senales[jugador1])
                self.jugadores[jugador1].mem_mostradas.append(senales[jugador1])
                self.jugadores[jugador2].mem_mostradas.append(senales[jugador2])


    class Jugador():
        def __init__(self, menLen):
            self.mem_mostradas = deque(maxlen=menLen)
            self.mem_observadas = deque(maxlen=menLen)

def calcular_ent(lista):
    auxstring = "".join(str(i + 1) * x for i, x in enumerate(lista))
    return (-sum(freq*math.log(freq, 2)
                                  for freq in (float(auxstring.count(n))/len(auxstring)
                                      for n in set(auxstring))))

def main():
    jugadores = [1, 2, 3, 4, 5, 6, 7, 8]
    senales = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']
    emparejamientos = [[(1, 2), (3, 4), (5, 6), (7, 8)],
                       [(1, 4), (3, 2), (5, 8), (7, 6)],
                       [(1, 6), (3, 8), (5, 2), (7, 4)],
                       [(1, 8), (3, 6), (5, 4), (7, 2)],
                       [(1, 3), (2, 4), (5, 7), (6, 8)],
                       [(1, 5), (2, 6), (3, 7), (4, 8)],
                       [(1, 7), (2, 8), (3, 5), (4, 6)]]

    # Memory length
    menLen = 7

    patron= 1

    s = [1, 0, 0, 0, 0, 0, 0, 0]

    # Content bias ('b'): no content bias=0.0, absolute preference for content=1.0
    # Coordination bias ('x'): fully egocentric=0.0, fully allocentric=1.0, no bias=0.5
    # mutation rate ('m')
    muestras = [{'b': 0.8, 'x': 0.5, 'm': 0.02} for _ in range(100)]

    simulaciones = 1

    estadisticas = {jugador:{muestra:{senal:[0 for ronda in range(1, len(emparejamientos)+1)]
                        for senal in senales}
                            for muestra in range(len(muestras))}
                                for jugador in jugadores}


    for mu in range(len(muestras)):
        for _ in range(simulaciones):
            juego = Partida(jugadores, menLen, emparejamientos, senales, s, muestras[mu]['b'],muestras[mu]['x'], muestras[mu]['m'])
            juego.jugar()
            for n, ronda in enumerate(juego.memoria):
                for jugador, senal in ronda.items():
                    estadisticas[jugador][mu][senal][n] += 1

        with open('data_entropy.csv', 'wb') as csvfile:
            writer =csv.writer(csvfile, delimiter=';',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Muestra', 'Jugador', 'Memoria', 'Ronda', 'Patron', 'b', 'x', 'm'] + senales + ['senales comunidad'] + ['ent'])

            for jugador in jugadores:
                for mu in range(len(muestras)):
                    for ronda in range(1, len(emparejamientos) + 1):
                        aux = [estadisticas[jugador][mu][senal][ronda - 1] for senal in senales]
                        aux1 = [estadisticas[1][mu][senal][ronda - 1] for senal in senales]
                        aux2 = [estadisticas[2][mu][senal][ronda - 1] for senal in senales]
                        aux3 = [estadisticas[3][mu][senal][ronda - 1] for senal in senales]
                        aux4 = [estadisticas[4][mu][senal][ronda - 1] for senal in senales]
                        aux5 = [estadisticas[5][mu][senal][ronda - 1] for senal in senales]
                        aux6 = [estadisticas[6][mu][senal][ronda - 1] for senal in senales]
                        aux7 = [estadisticas[7][mu][senal][ronda - 1] for senal in senales]
                        aux8 = [estadisticas[8][mu][senal][ronda - 1] for senal in senales]

                        nuevalista = []

                        for i in range(len(aux1)):
                            nuevalista.append(aux1[i] + aux2[i] + aux3[i] + aux4[i] + aux5[i] + aux6[i] + aux7[i] + aux8[i])
                        print nuevalista

                        writer.writerow([mu + 1, jugador, menLen, ronda, patron, muestras[mu]['b'], muestras[mu]['x'],
                                         muestras[mu]['m']] + aux + [nuevalista] + [calcular_ent(nuevalista)])

if __name__ == '__main__':
    main()


