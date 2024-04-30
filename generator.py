import random
f = open("example.txt", 'w')
f.write("1000\n")
for i in range(1000):
    for j in range(1000):
        if(i==j):
            f.write(str(random.randint(1,50)*10000)+' ')
        else:
            f.write(str(random.randint(-10,10))+' ')
    f.write(str(random.randint(-10000,10000))+'\n')
f.write(str(0.0001))
