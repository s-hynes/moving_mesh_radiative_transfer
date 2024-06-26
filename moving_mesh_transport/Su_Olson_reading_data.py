"""This is me messing around trying to remember how to read data from a text file 
    into a Python array to plot it. - Stephen"""

import numpy as np
import matplotlib.pyplot as plt
import time

def su_olson(tfinal):

    radius = 50

    #t1 = time.perf_counter()

    with open("Su-Olson_rad_en_dens.txt") as rad:
        linesrad = rad.read().splitlines()  

    #Nlines = len(linesrad) - 1

    with open("Su-Olson_mat_en_dens.txt") as mat:
        linesmat = mat.read().splitlines()  

    #x  = np.zeros(Nlines)
    #rad = np.zeros(Nlines)
    #mat = np.zeros(Nlines)

    x  = []
    rad = []
    mat = []

    # I feel like this sequence of if statements could be more concise and/or elegant.

    if tfinal == 0.1:
        for line in linesrad:
            columns1 = line.split(",")
            x.append(columns1[0])   # Appends the 0th element of the list 'columns' to the list 'x', because the x values are found in the 1st column of the data file.
            rad.append(columns1[1])
        for line in linesmat:
            columns2 = line.split(",")
            mat.append(columns2[1])

    elif tfinal == 0.31623:
        for line in linesrad:
            columns1 = line.split(",")
            x.append(columns1[0])   # Appends the 0th element of the list 'columns' to the list 'x', because the x values are found in the 1st column of the data file.
            rad.append(columns1[2])
        for line in linesmat:
            columns2 = line.split(",")
            mat.append(columns2[2])

    elif tfinal == 1.0:
        for line in linesrad:
            columns1 = line.split(",")
            x.append(columns1[0])   # Appends the 0th element of the list 'columns' to the list 'x', because the x values are found in the 1st column of the data file.
            rad.append(columns1[3])
        for line in linesmat:
            columns2 = line.split(",")
            mat.append(columns2[3])

    elif tfinal == 3.16228:
        for line in linesrad:
            columns1 = line.split(",")
            x.append(columns1[0])   # Appends the 0th element of the list 'columns' to the list 'x', because the x values are found in the 1st column of the data file.
            rad.append(columns1[4])
        for line in linesmat:
            columns2 = line.split(",")
            mat.append(columns2[4])

    elif tfinal == 10.0:
        for line in linesrad:
            columns1 = line.split(",")
            x.append(columns1[0])   # Appends the 0th element of the list 'columns' to the list 'x', because the x values are found in the 1st column of the data file.
            rad.append(columns1[5])
        for line in linesmat:
            columns2 = line.split(",")
            mat.append(columns2[5])

    elif tfinal == 31.6228:
        for line in linesrad:
            columns1 = line.split(",")
            x.append(columns1[0])   # Appends the 0th element of the list 'columns' to the list 'x', because the x values are found in the 1st column of the data file.
            rad.append(columns1[6])
        for line in linesmat:
            columns2 = line.split(",")
            mat.append(columns2[6])

    elif tfinal == 100.0:
        for line in linesrad:
            columns1 = line.split(",")
            x.append(columns1[0])   # Appends the 0th element of the list 'columns' to the list 'x', because the x values are found in the 1st column of the data file.
            rad.append(columns1[7])
        for line in linesmat:
            columns2 = line.split(",")
            mat.append(columns2[7])
    
    else:
        print("Su_Olson function called for time not tabulated in paper.")
        assert(0)
    

    #print("mat = ", mat)

    del(x[0])
    del(rad[0])
    del(mat[0])

    for k in range(16):
        rad[:] = [item for item in rad if item != k*' ']
        mat[:] = [item for item in mat if item != k*' ']

    x = x[:len(rad)]

    #print("rad after filtering: ", rad)
    #print("mat after filtering; ", mat)
    #print("x after filtering: ", x)
    x = np.asarray(x).astype(float)
    rad = np.asarray(rad).astype(float)
    mat = np.asarray(mat).astype(float)

    x2 = np.zeros(2*len(x))
    rad2 = np.zeros(2*len(x))
    mat2 = np.zeros(2*len(x))
    #print("length of x = ", len(x))
    #print("length of x2 = ", len(x2))

    for j in range(len(x)):
        x2[j] = - x[len(x) - 1 - j]
        rad2[j] = rad[len(x) - 1 - j]
        mat2[j] = mat[len(x) - 1 - j]
    
    for j in range(len(x), len(x2)):
        x2[j] = x[j - len(x)]
        rad2[j] = rad[j - len(x)]
        mat2[j] = mat[j - len(x)]

    #print(x)
    #print(x2)
    #print(rad)
    #print(rad2)
    #print(mat)
    #print(mat2)

    plt.plot(x2 + radius, rad2, '-',label='Radiation Energy Density (Su-Ol)', marker='o')
    plt.plot(x2 + radius, mat2, '-.',label='Material Energy Density (Su-Ol)')
    plt.xlabel("x")
    plt.ylabel("Energy Density")
    plt.legend()
    #t2 = time.perf_counter()
    #print("Su-Olson function took {0:.5} seconds to execute.".format(t2-t1))
    plt.show()

# Time values tabulated in Su-Olson paper:
# 0.10000    ,0.31623    ,1.00000    ,3.16228    ,10.0000    ,31.6228    ,100.000

#su_olson(0.1)

#infile = open("Su-Olson_rad_en_dens.txt", "r")

#linetxt = infile.readlines()

#infile.close()  

#print(linetxt[0])

#y = np.array(linetxt[0])
#print(type(y))

#print(y)

#print(type(linetxt))

#linetxt = np.array(linetxt)

#print(type(linetxt))
#print(linetxt)
#print(linetxt.shape)

# energy densities for t=0.01000

#
# rad = np.array([0.09531,0.27526,0.64308,1.20052,2.23575,0.69020,0.35720])
#mat = np.array([0.00468,0.04093,0.27126,0.94670,2.11186,0.70499,0.35914])
