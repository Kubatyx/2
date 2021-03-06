import random
import math
import numpy
import random
import time
import sys
tab = []

    
# czytanie z pliki
def file(filename):
    with open(filename, "r") as file:

        jobs, machines = [int(x) for x in next(file).split()]
        print ("Liczba zadan:", jobs)
        print ("Liczba maszyn:", machines)
        for line in file:
            tab.append([int(x) for x in line.split()])
        o = [list(x) for x in zip(*tab)]
        print ("Czasy wykonywania sie zadan przez poszczegolne maszyny:")
        for i in range(len(o)):
            print("Maszyna:",i+1,o[i])
        print ('\n')
    return machines, jobs, o

# obliczanie cmaxa
def makespan(sequence, tab, machines):
    cmax = numpy.zeros((machines, len(sequence) + 1)) #tworzy tablice
    #print cmax
    for j in range(1, len(sequence) + 1):
        cmax[0][j] = cmax[0][j - 1] + tab[0][sequence[j - 1]]
    for i in range(1, machines):
        for j in range(1, len(sequence) + 1):
            cmax[i][j] = max(cmax[i - 1][j], cmax[i][j - 1]) + tab[i][sequence[j - 1]]
    #=print cmax
    return cmax

# funkcja dopisujaca sekwencje
def insertion(sequence, position, value):
    new = sequence[:] #nowa sekwencja
    new.insert(position, value) #dopisanie nowej sekwencji
    #print new
    return new

# obliczanie czasu 
def jobtime(job_id, data, machines):
    sum_p = 0
    for i in range(machines):
        sum_p += data[i][job_id]
    #print sum_p
    return sum_p

# zwykly neh
def neh(data, machines, jobs):
    sequence = []
    for j in range(jobs):
        sequence.append(j)
    order = sorted(sequence, key=lambda x: jobtime(x, data, machines), reverse=True)
    sequence = [order[0]]
    for i in range(1, jobs):
        min_cmax = 30000000
        for j in range(0, i+1):
            seq = insertion(sequence, j, order[i])
            cmax = makespan(seq, data, machines)[machines - 1][len(seq)]
            #print ("\nKolejnosc:\n",seq, "\nMakespan:",cmax)
            if min_cmax > cmax:
                best_seq = seq
                min_cmax = cmax
        sequence = best_seq
    return sequence, makespan(sequence, data, machines)[machines -1][jobs]

def Swap(sequence): # zmiana kolejnosci dwoch losowo wybranych zadan
    tmp = sequence[:]
    job1 = random.randrange(len(sequence)) # random number z ilosci
    job2 = job1
    if job1 == job2: # warunek kiedy sa te same
        job2 = random.randrange(len(sequence) - 1) # losowanie raz jeszcze

    tmp[job1] = sequence[job2]
    tmp[job2] = sequence[job1]
    return tmp


def simulatedannealing (data, machines, jobs):

    sequence, C = neh(data, machines, jobs)
    temp = 1000 # ustalenie temperatury poczatkowej
    mi = [0.8, 0.9, 0.95, 0.99] # wspolczynnik [0.8 0.9 0.95 0.99]
    mi = 0.8

    while temp > 30:
        seqprim = Swap(sequence)
        Cprim = makespan(sequence, data, machines)[machines -1][jobs]
        if Cprim < C: # nowe rozwiazanie lepsze od obecnego
            P = 1 # prawdopodobienstwo 
        else: # nowe gorsze od obecnego
            P = math.exp((C - Cprim)/temp) # funKCJA

        if P >= random.random(): 
            sequence = seqprim[:]
            C = Cprim
        temp = mi*temp #funkcja schladzania mi(0,1)
        print temp,
    return C, sequence


if __name__ == "__main__":
    jobs, machines, o = file("test/ta000")
    seq, cmax = neh(o, jobs, machines)
    cmaxx, seqq = simulatedannealing(o, jobs, machines)
    print ("NEH:", seq[:], '\nBest makespan:', cmax)
    print ("Wyzarzanie:", seqq[:], '\nMakespan:', cmaxx)