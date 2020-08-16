#Metode Global variable

def var1(x):
    global y
    global z
    y=x+15
    z=y+89
    return z,y

def var10(x):
    y=x+15
    z=y+89
    return z,y

print("y og z globalvariable udskrift ")
var1(3)
print(y)
print(z)

print()
print("Tuple udskrift")
var2=var10(15)
print(var2[1])
print(var2[0])
print()

#Metode nr. 2
print("Tuple udskrift2")
var3z, var3y =var10(4)
print(var3y)
print(var3z)

