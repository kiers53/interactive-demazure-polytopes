

class Vector:
    def __init__(self,lst):
        self.lst=lst
        self.m=len(lst)

    def posQ(self):
        for el in self.lst:
            if el<0:
                return False
        return True

    def __str__(self):
        s='['
        for el in self.lst:
            s+=str(el)+' '
        return s[:-1]+']'

    def __mul__(self,other):
        if self.m!=other.m:
            raise ValueError("Incompatible vector dimensions")
        return sum([self.lst[i]*other.lst[i] for i in range(self.m)])

    def __eq__(self,other):
        return self.lst==other.lst

    def zeros(n):
        return Vector([0]*n)

    def __rmul__(self,scalar):
        if isinstance(scalar,int) or isinstance(scalar,float):
            new=[scalar*self.lst[i] for i in range(self.m)]
            return Vector(new)
        else:
            raise TypeError("Invalid scalar multiplication")



class Matrix:
    def __init__(self,mat):
        self.mat=mat
        self.m=len(mat)
        self.n=len(mat[0])

    def __mul__(self,other):
        if isinstance(other,Matrix):
            if self.n!=other.m:
                raise ValueError("Incompatible matrix dimensions")
            new=[[sum([self.mat[i][j]*other.mat[j][k] for j in range(self.n)]) for k in range(other.n)] for i in range(self.m)]
            return Matrix(new)
        elif isinstance(other,Vector):
            if self.n!=other.m:
                raise ValueError("Incompatible matrix and vector dimensions")
            new=[sum([self.mat[i][j]*other.lst[j] for j in range(self.n)]) for i in range(self.m)]
            return Vector(new)
        else:
            raise TypeError("Can only multiply matrix by another matrix or vector")

    def __rmul__(self,scalar):
        if isinstance(scalar,int) or isinstance(scalar,float):
            new=[[scalar*self.mat[i][j] for j in range(self.n)] for i in range(self.m)]
            return Matrix(new)
        else:
            raise TypeError("Invalid scalar multiplication")

    def __eq__(self,other):
        return self.mat==other.mat

    def __str__(self):
        s=''
        for el in self.mat:
            s+=str(el)+'\n'
        return s[:-1]

    def transp(self):
        return Matrix([[self.mat[i][j] for i in range(self.m)] for j in range(self.n)])

    def zeros(n):
        return Matrix([[0 for i in range(n)] for j in range(n)])

    def ident(n):
        return Matrix([[1*(i==j) for i in range(n)] for j in range(n)])


        




def get_Cartan_matrix(typ,ran):
    blank = Matrix.zeros(ran).mat
    for i in range(ran):
        blank[i][i]=2
    if typ=='A':
        for i in range(ran):
            for j in range(ran):
                if abs(i-j)==1:
                    blank[i][j]=-1
        return Matrix(blank)
    if typ=='B':
        for i in range(ran-1):
            for j in range(ran-1):
                if abs(i-j)==1:
                    blank[i][j]=-1
        blank[ran-1][ran-2]=-1
        blank[ran-2][ran-1]=-2
        return Matrix(blank)
    if typ=='C':
        for i in range(ran-1):
            for j in range(ran-1):
                if abs(i-j)==1:
                    blank[i][j]=-1
        blank[ran-1][ran-2]=-2
        blank[ran-2][ran-1]=-1
        return Matrix(blank)
    if typ=='D':
        for i in range(ran-1):
            for j in range(ran-1):
                if abs(i-j)==1:
                    blank[i][j]=-1
        blank[ran-1][ran-3]=-1
        blank[ran-3][ran-1]=-1
        return Matrix(blank)
    if typ=='E':
        for i in range(2,ran):
            for j in range(2,ran):
                if abs(i-j)==1:
                    blank[i][j]=-1
        blank[0][2]=-1
        blank[2][0]=-1
        blank[1][3]=-1
        blank[3][1]=-1
        return Matrix(blank)
    if typ=='F':
        return Matrix([[2,-1,0,0],[-1,2,-2,0],[0,-1,2,-1],[0,0,-1,2]])
    if typ=='G':
        return Matrix([[2,-1],[-3,2]])

            
def simple_refl(cm,ran,j): # j between 1 and ran
    init=Matrix.ident(ran).mat
    for i in range(ran):
        init[j-1][i]-=cm.mat[i][j-1]
    return Matrix(init)



class WeylGroup:

    def __init__(self,typ,ran,prefix='s',override_CM=None): 
        if isinstance(override_CM,Matrix):
            self.cm=override_CM
            self.ran=len(override_CM.mat)
        else:
            types=['A','B','C','D','E','F','G']
            self.typ = typ
            if typ not in types:
                raise ValueError('Invalid type: '+str(typ)+'. Valid types are '+str(types))
            self.ran = ran
            if ran<1 or (typ in ['B','C'] and ran<2) or (typ=='D' and ran<4) or (typ=='E' and ran not in [6,7,8]) or (typ=='F' and ran!=4) or (typ=='G' and ran!=2):
                raise ValueError('Invalid rank for type '+str(typ)+': '+str(ran))
            self.cm=get_Cartan_matrix(typ,ran)

        self.s = prefix
        self.get_simple_matrices()
        self.get_simple_roots()
        self.get_simples()
        self.get_weight_simples()

    def get_simple_matrices(self):
        self.S={}
        for i in range(1,self.ran+1):
            self.S[i]=simple_refl(self.cm,self.ran,i)

    def get_simple_roots(self):
        self.Delta={}
        for i in range(self.ran):
            v=Vector.zeros(self.ran).lst
            v[i]=1
            self.Delta[i+1]=Vector(v)

    def get_simples(self):
        self.simples={}
        for i in range(1,self.ran+1):
            self.simples[i]=element(self,self.S[i])
        
    def get_word(self,mat):
        for i in range(1,self.ran+1):
            if not (mat*self.Delta[i]).posQ():
                return self.get_word(mat*self.S[i])+[i]
        return []
            
    def get_w0(self,mat=None,word=[]): ## currently this does not return the 'canonical' reduced word
        if isinstance(mat,Matrix):
            m = mat
        else:
            m = Matrix.ident(self.ran)
        for i in range(1,self.ran+1):
            if (m*self.Delta[i]).posQ():
                return self.get_w0(m*self.S[i],word+[i])
        return element(self,m,word)

    def get_weight_simples(self):
        self.weight_S={}
        for i in range(1,self.ran+1):
            self.weight_S[i]=simple_refl(self.cm.transp(),self.ran,i).transp()

    def get_all(self):
        self.w0=self.get_w0()
        self.all=self.w0.all_subwords()

    def __len__(self):
        return len(self.all)

    def from_red_word(self,lst):
        mat=Matrix.ident(self.ran)
        for j in lst:
            mat=mat*self.S[j]
        return element(self,mat,lst)

    def from_word(self,lst):
        mat=Matrix.ident(self.ran)
        for j in lst:
            mat=mat*self.S[j]
        return element(self,mat)

    def identity(self):
        return self.from_red_word([])

    def Dem_from_word(self,lst):
        return self.identity().Dem(lst)
        
            

    
    def get_REPS(self): ## to get reps modulo maximal parabolics
        REPS={} 
        for i in range(1,self.ran+1):
            REPS[i]=[]
            l=list(range(1,self.ran+1))
            l.pop(i-1)
            for w in self.all:
                wp=w.reduce(l)
                if wp not in REPS[i]:
                    REPS[i]+=[wp]
        self.REPS = REPS
            

class element:
    def __init__(self,wg,mat,word=None):
        self.wg=wg
        self.mat=mat
        if word==None:
            self.word=self.wg.get_word(mat)
        else:
            self.word=word
        
    def __len__(self):
        return len(self.word)

    def __str__(self):
        if self.word==[]:
            return '1'
        st=''
        for j in self.word:
            st+=self.wg.s+str(j)+'*'
        return st[:-1]

    def __mul__(self,other):
        return element(self.wg,self.mat*other.mat)

    def __eq__(self,other):
        return self.mat==other.mat

    def inv(self):
        new=[]
        for el in self.word:
            new=[el]+new
        return self.wg.from_red_word(new)

    def has_right_desc(self,j): ## test if w*s_j is smaller than w
        return not (self.mat*self.wg.Delta[j]).posQ()

    def Dem(self,other):
        if isinstance(other,element):
            return self.Dem(other.word)
        if len(other)==0:
            return self

        if self.has_right_desc(other[0]):
            return self.Dem(other[1:])
        temp=self*self.wg.simples[other[0]]
        return temp.Dem(other[1:])


    def __le__(self,other):
        if self==other:
            return True
        if len(other)==0:
            return False
        if len(self)==0:
            return True
        for i in range(-1,-len(other)-1,-1):
            j = other.word[i]
            if self.has_right_desc(j):
                return (self*self.wg.simples[j])<=self.wg.from_red_word(other.word[:i])
        return False

    def all_subwords(self): ## really slow implementation...
                            ## I suppose the fast way would involve defining all positive roots
                            ## actually, see `bruhat_lower_covers' in sage documentation for fast algorithm?
        al = []
        l=len(self)
        for j in range(2**l):
            st = ('%'+str(l)+'s')%(bin(j)[2:])
            sub=[]
            for i in range(l):
                if st[i]=='1':
                    sub+=[self.word[i]]
            w=self.wg.from_word(sub)
            if w not in al:
                al+=[w]
        return al

    def weight_matrix(self): ## matrix for action in the weight basis
        mat=Matrix.ident(self.wg.ran)
        for j in self.word:
            mat=mat*self.wg.weight_S[j]
        return mat

    def coweight_matrix(self):
        t=self.inv()
        return t.mat.transp()

    ## coroot matrix not implemented

    def reduce(self,indices): ## find min-length representative modulo subgroup generated by indices
        w=self
        long=True
        while long:
            long=False
            for i in indices:
                if w.has_right_desc(i):
                    #print(w)
                    w=w*self.wg.simples[i]
                    #print(w)
                    long=True
        return w
                    

    








