
from weyl_groups import *
import math


def support(anylist): # distinct elements in a list
    new = []
    for el in anylist:
        if el not in new:
            new+=[el]
    return new

def get_nonsimple_Cartan(code): # get cartan matrix for non-simple types
                      #         A1xA1, A1xA2, A1xB2, A1xG2, A1xA1xA1
    if code=='A1xA1':
        return Matrix([[2,0],
                       [0,2]])
    if code=='A1xA2':
        return Matrix([[2,0,0],
                       [0,2,-1],
                       [0,-1,2]])
    if code=='A1xB2':
        return Matrix([[2,0,0],
                       [0,2,-2],
                       [0,-1,2]])
    if code=='A1xG2':
        return Matrix([[2,0,0],
                       [0,2,-1],
                       [0,-3,2]])
    if code=='A1xA1xA1':
        return Matrix([[2,0,0],
                       [0,2,0],
                       [0,0,2]])
        


def get_COB(code): # code can be 'A1','A2','A3','A1xA1','A1xA2',
                   #             'B2','B3','C3','A1xB2','G2','A1xG2','A1xA1xA1'
                   #
                   # the COB is change of basis from fundamental weights to
                   # Euclidean space with usual dot product
                   # the coCOB is the same thing for fundamental coweights
                   # (not necessarily invertible as we are embedding into 3-space)
    ## -------
    ## simples
    ## -------
                   
    if code=='A3':
        COB=Matrix([[0.5,0,-0.5],
                    [0.5,1,0.5],
                    [0.5,0,0.5]])
        coCOB = COB
    elif code=='A2':
        COB=Matrix([[math.sqrt(2)/2,0],
                    [math.sqrt(6)/6,math.sqrt(6)/3],
                    [0,0]])
        coCOB = COB
    elif code=='A1':
        COB=Matrix([[1],
                    [0],
                    [0]])
        coCOB=COB
    elif code=='B3':
        COB=Matrix([[1,1,0.5],
                    [0,1,0.5],
                    [0,0,0.5]])
        coCOB=Matrix([[1,1,1],
                      [0,1,1],
                      [0,0,1]])
    elif code=='B2':
        COB=Matrix([[1,0.5],
                    [0,0.5],
                    [0,0]])
        coCOB=Matrix([[1,1],
                      [0,1],
                      [0,0]])
    elif code=='C3':
        coCOB=0.7*Matrix([[1,1,0.5],
                    [0,1,0.5],
                    [0,0,0.5]])
        COB=0.7*Matrix([[1,1,1],
                      [0,1,1],
                      [0,0,1]])
    elif code=='G2':
        COB=(0.5)*Matrix([[math.sqrt(2)/2,0],
                    [math.sqrt(6)/2,math.sqrt(6)],
                    [0,0]])
        coCOB=(0.5)*Matrix([[math.sqrt(2)/2,0],
                      [math.sqrt(6)/2,math.sqrt(6)/3],
                      [0,0]])

    ## -----------
    ## non-simples
    ## -----------
    
    elif code=='A1xA1xA1':
        COB=Matrix([[1,0,0],
                    [0,1,0],
                    [0,0,1]])
        coCOB=COB
    elif code=='A1xA2':
        COB=Matrix([[1,0,0],
                    [0,math.sqrt(2)/2,0],
                    [0,math.sqrt(6)/6,math.sqrt(6)/3]])
        coCOB=COB
    elif code=='A1xB2':
        COB=Matrix([[1,0,0],
                    [0,1,0.5],
                    [0,0,0.5]])
        coCOB=Matrix([[1,0,0],
                      [0,1,1],
                      [0,0,1]])
    elif code=='A1xG2':
        COB=(0.5)*Matrix([[2,0,0],
                    [0,math.sqrt(2)/2,0],
                    [0,math.sqrt(6)/2,math.sqrt(6)]])
        coCOB=(0.5)*Matrix([[2,0,0],
                      [0,math.sqrt(2)/2,0],
                      [0,math.sqrt(6)/2,math.sqrt(6)/3]])
    elif code=='A1xA1':
        COB=Matrix([[1,0],
                    [0,1],
                    [0,0]])
        coCOB=COB
                    
    return (COB,coCOB)



def extract_type_rank_override(in_info):
    info = in_info
    if info in ['A1','A2','A3','B2','B3','C3','G2']:
        typ=info[0]
        ran=int(info[1])
        override=None
    else:
        info=info.replace(' ','')
        #print(info)
        typ=''
        ran=sum([int(info[i]) for i in range(1,len(info)+1,3)])
        override=get_nonsimple_Cartan(info)
    return (typ,ran,override)


def order(unordered,idxlist=[]): ## order a set of points in the plane via angle around
                                 ## the average of the points
                                 ## idxlist is an optional record for the indices of the
                                 ## points in some known collection

## TO DO:
## RETURN THE ORDER OF THE INDICES FROM IDXLIST AS WELL

    N = len(unordered)

    idx=False
    if N==len(idxlist):
        idx=True

    xavg = 1/N*sum([unordered[i][0] for i in range(N)])
    yavg = 1/N*sum([unordered[i][1] for i in range(N)])

    D = {}
    I = {}

    for i in range(len(unordered)):
        (x,y)=unordered[i]
        if idx:
            ji=idxlist[i]
            
        d = math.sqrt((x-xavg)**2+(y-yavg)**2)
        if d==0:
            ang=-math.pi/2
            #D[-math.pi/2] = (x,y)
        else:
            t1 = math.acos((x-xavg)/d)
            t2 = math.asin((y-yavg)/d)
            if t1<math.pi/2 and t2>0:
                #D[t1] = (x,y)
                ang=t1
            elif t1<math.pi/2 and t2<0:
                #D[t2] = (x,y)
                ang=t2
            elif t2>=0:
                #D[t1] = (x,y)
                ang=t1
            elif t2<=0:
                #D[2*math.pi-t1] = (x,y)
                ang=2*math.pi-t1
        D[ang] = (x,y)
        if idx:
            I[ang] = ji
            

    ts = list(D.keys())
    ts.sort()
    ordered = [D[el] for el in ts]
    if idx:
        idxo = [I[el] for el in ts]
    else:
        idxo = []
    return (ordered,idxo)


class Facet: # a 3d polygon defined by its vertices.
             # The outward normal decides shading later.
             # idxlist is an optional record for the indices of the vertices in
             # some known collection of points

    def __init__(self,vertices,out_normal,idxlist=[]):
        self.vertices=vertices
        self.normal=out_normal
        self.idxlist = idxlist
        # Coordinates in the plane of the face;
        # can use x-y coordinates as long as normal has a z-component, otherwise
        # try other planes
        if self.normal.lst[2]!=0:
            self.coordsys = [0,1]
        elif self.normal.lst[1]!=0:
            self.coordsys = [0,2]
        else:
            self.coordsys = [1,2]
        self.node = 1 # should this be the default value? 
        

    def flatten(self): # output to tuples (not vectors)
        # Now we need this to return coordinates in the plane of the face;
        # can use x-y coordinates as long as normal has a z-component, otherwise
        # try other planes as determined already by self.coordsys
        [i,j] = self.coordsys
        ret = []
        for el in self.vertices:
            x = el.lst[i]
            y = el.lst[j]
            ret+=[(x,y)]
        return ret 
        

    def gradient(self): # assign a value in [0,1] based on how
                        # the normal direction compares to the z-axis ([0,0,1])
        n=self.normal
        return (n.lst[2]/math.sqrt(n*n)+1)/2


    def triangulate(self): # only for use if idxlist-live
                           # returns a collection of 'triangles', each triangle being
                           # a list of three indices
        flat = self.flatten()
        if len(self.idxlist)<3:
            return []
        if len(self.idxlist)==3:
            return [self.idxlist]
        ordered_pair = order(flat,self.idxlist)
        ordered_indices = ordered_pair[1]
        #print(len(self.idxlist))
        #print(len(ordered_indices))
        assert len(ordered_indices)>3 # just double-check that the ordering was successful
        N = len(ordered_indices)
        tris = []
        for i in range(1,N-1):
            newtri = [ordered_indices[0],ordered_indices[i],ordered_indices[i+1]]
            tris+=[newtri]
        return tris
                           
        


class LieSys:

    def __init__(self,lie_type):
        self.info = lie_type.replace(' ','')
        (typ,ran,override) = extract_type_rank_override(lie_type)
        self.typ = typ
        self.ran = ran
        self.override = override
        (COB,coCOB) = get_COB(self.info)
        self.COB = COB
        self.coCOB = coCOB
        self.W = WeylGroup(self.typ,self.ran,'s',self.override)
        self.W.get_all()
        self.W.get_REPS()
        self.Wlist={}
        self.wordlist=[]
        for w in self.W.all:
            self.Wlist[str(w)] = w
            self.wordlist+=[str(w)]

    def match(self,word):
        lastindex=len(self.wordlist)-1
        if word!='':
            allowed=['1','2','3'][:self.ran]
            new=''
            lst=[]
            for bit in word:
                if bit in allowed:
                    new+=bit
                    lst+=[int(bit)]

            win = self.W.Dem_from_word(lst)

            found=False

            i=0
            while not found and i < len(self.wordlist):
                if self.wordlist[i]==str(win):
                    lastindex=i
                    found=True
                i+=1
        return lastindex


class DemPoly:

    def __init__(self,LS,thew,lam): # thew is a string type, key for the Wlist dict
                                    # in LS
                                    # lam is a Vector of weights in the weight basis
        self.LS = LS
        self.w = self.LS.Wlist[thew]
        self.lam = lam

        self.eff_dim = self.get_eff_dim()

        self.flist=[]
        self.globvx=[]
        self.gvxd={}


    def get_eff_dim(self):
        minw = self.w
        minl = len(self.w.word)
        for v in self.LS.W.all:
            if v.weight_matrix()*self.lam==self.w.weight_matrix()*self.lam:
                newl = len(v.word)
                if newl<minl:
                    minw = v
                    minl = newl
        supp = support(minw.word)
        return len(supp)
            

    def get_faces(self): # this function is exclusively for the rank 3s

        flist = []
        globvx = []
        gvxd = {}

        for i in range(1,self.LS.ran+1):
            l = list(range(1,self.LS.ran+1))
            l.pop(i-1)
            for v in self.LS.W.REPS[i]:
                u = (self.w.inv().Dem(v)).reduce(l)
                y = (v.inv().Dem(self.w))*u
                vxlist = []
                idxlist = []
                lam2 = u.inv().weight_matrix()*self.lam
                for yp in y.all_subwords():
                    new = (v*yp).weight_matrix()*lam2
                    new = (self.LS.COB*new)
                    if new not in vxlist:
                        vxlist+=[new] # new at least to the face
                        if new not in globvx: # new to everybody, add new index
                            j = len(globvx)
                            globvx+=[new]
                            gvxd[str(new)] = j
                            idxlist+=[j]
                        else: # new just on the face, existing index known
                            idxlist+=[gvxd[str(new)]]
                
                xi = [0]*self.LS.ran
                xi[i-1] = 1
                xi = Vector(xi)
                normal = self.LS.coCOB*v.coweight_matrix()*xi

                newf = Facet(vxlist,normal,idxlist)
                newf.node = i
                flist+=[newf]
                
        self.flist=flist
        self.globvx=globvx
        self.gvxd=gvxd
        
        return flist




    def get_face(self): # for ranks 2 or 1

        globvx = []
        gvxd = {} # this might be unnecessary
        idxlist = [] # and this is just [0,...,len-1]

        for v in self.w.all_subwords():
            new = v.weight_matrix()*self.lam
            new = self.LS.COB*new
            if new not in globvx:
                j = len(globvx)
                globvx+=[new]
                gvxd[str(new)] = j
                idxlist+=[j]

        f = Facet(globvx,Vector([0,0,1]),idxlist)

        self.flist=[f]
        self.globvx=globvx
        self.gvxd=gvxd

        return [f]

    def get_plotly_input(self,colors=['green','red','blue']): # should run get_faces or get_face first
        points = []
        for el in self.globvx:
            points+=[el.lst]
        pts2 = Matrix(points)
        [x,y,z] = pts2.transp().mat

        tris = []
        cols=[]
        for f in self.flist:
            temp = f.triangulate()
            if len(temp)>0:
                tris+=temp
                for ii in range(len(temp)):
                    cols+=[colors[f.node-1]]
        if len(tris)>0:
            tr2 = Matrix(tris)
            [i,j,k] = tr2.transp().mat
        else:
            [i,j,k] = [[], [], []]

        return [x,y,z,i,j,k,cols]
        


'''
LS = LieSys('A3')

p1 = DemPoly(LS,"s1*s2",Vector([0,0,1]))

p2 = DemPoly(LS,"s1*s2",Vector([1,0,0]))

p3 = DemPoly(LS,"s1*s2",Vector([0,1,0]))

p4 = DemPoly(LS,"s1*s2",Vector([1,1,1]))

p5 = DemPoly(LS,"s1*s2*s3",Vector([1,1,1]))

for p in [p1,p2,p3,p4,p5]:
    print(p.eff_dim)



flist = p5.get_faces()

f3 = flist[3]
'''


LS = LieSys('B3')
p = DemPoly(LS,'s2*s3*s1*s2*s3',Vector([3,3,3]))
p.get_faces()
[x,y,z,i,j,k,cols]=p.get_plotly_input()








