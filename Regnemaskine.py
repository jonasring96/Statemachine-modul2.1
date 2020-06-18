#Regnemaskine
Menutal=0
#tal1=0
#tal2=0

def Plus(x,y):
    resultat =x+y
    return resultat

def Minus(x,y):
    resultat = x-y
    return resultat

def Gange(x,y):
    resultat=x*y
    return resultat

def Divider(x,y):
    if y==0:
        print("Kan ikke lade sig gøre, der divideres med 0!!")
        return
    resultat=x/y
    return resultat

def menu():
    global Menutal
    print("Tast 1(+), 2(-), 3(*), 4(/), 5(slut)")
    Menutal = int(input("tast tal nu!!"))
    if Menutal <0 or Menutal>5:
        print("Dit indtast er forkert!!")
        menu()

menu()


while Menutal==1:
    print("Nu skal der lægges sammen(+)!")
    tal1=float(input("Indtast det første tal?"))
    tal2=float(input("Indtast det andet tal?"))
    print("Resultatet af",tal1,"+",tal2,"=",Plus(tal1, tal2))
    print()
    menu()


while Menutal==2:
    print("Nu skal der  trækkes fra(-)!")
    tal1=float(input("Indtast det første tal?"))
    tal2=float(input("Indtast det andet tal?"))
    print("Resultatet af",tal1,"-",tal2,"=",Minus(tal1, tal2))
    print()
    menu()


while Menutal==3:
    print("Nu skal der ganges(*)!")
    tal1=float(input("Indtast det første tal?"))
    tal2=float(input("Indtast det andet tal?"))
    print("Resultatet af",tal1,"*",tal2,"=",Gange(tal1, tal2))
    print()
    menu()


while Menutal==4:
    print("Nu skal der dividers(/)!")
    tal1=float(input("Indtast det første tal?"))
    tal2=float(input("Indtast det andet tal?"))
    print("Resultatet af",tal1,"/",tal2,"=",Divider(tal1, tal2))
    print()
    menu()



while Menutal==5:
    print("Slut!!!!!!!")
    break
