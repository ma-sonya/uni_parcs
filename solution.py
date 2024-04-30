from Pyro4 import expose
from random import randint
import random
class Solver:
    A=[]
    n=0
    eps=0.0
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")
    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        (Solver.n,Solver.A,Solver.eps) = self.read_input()
        step = int(Solver.n / len(self.workers))
        if((Solver.n%len(self.workers))>0):
            step+=1
        st=0
        ii=0
        x=[0 for i in range(Solver.n)]
        for t in range(1000):
            mapped = []
            for i in xrange(0, len(self.workers)):
                mapped.append(self.workers[i].mymap(Solver.n,Solver.A,x,i*step,i*step+step,st))
            xnew=self.myreduce(mapped)
            norm=0
            for i in range(Solver.n):
                norm+=abs(xnew[i]-x[i])
            if(norm<-1):
                break
            else:
                x=xnew
                st=1
                Solver.A=[]
        self.write_output(xnew)
    @staticmethod
    @expose
    def mymap(n,A,x,l,r,st):
        if(st==0):
            Solver.n=n
            Solver.A=A
        xnew=[]
        for k in range(l,min(r,Solver.n)):
            xnew.append(float(Solver.A[k][Solver.n]))
            for i in range(Solver.n):
                if(not(i==k)):
                    xnew[k-l]=xnew[k-l]-Solver.A[k][i]*x[i]
            xnew[k-l]/=Solver.A[k][k]
        return xnew
    @staticmethod
    @expose
    def myreduce(mapped):
        print("reduce")
        output = []
        for xs in mapped:
            print("reduce loop")
            output = output + xs.value
        print("reduce done")
        
        return output 
    def read_input(self):
        f = open(self.input_file_name, 'r')
        n=int(f.readline())
        A=[]
        for i in range(n):
            A.append([int(x) for x in ((f.readline()).split())] )
        eps=float(f.readline())
        return (n,A,eps)
    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        for a in output:
            f.write(str(a) + ' ')
        f.close()
        print("output done") 
