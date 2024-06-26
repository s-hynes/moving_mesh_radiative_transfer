"""Learning how to set up an if statement that is true if a certain element is in a list and false
otherwise."""

t = 0.1

x = [0.10000,0.31623,1.00000,3.16228,10.0000,31.6228,100.000]

if [i for i in x if i==t]:
    print("t is in array so statement evaluates to true.")
    print(t)
else:
    print("t is not in array so statement evaluates to false.")