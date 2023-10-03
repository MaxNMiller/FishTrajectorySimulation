import numpy as np

# my mathamatical understanding of noise generation primarily came from this lecture:
# cs.umd.edu/class/fall2018/cmsc425/Lects/lect14-perlin.pdf
bilerp = lambda v0,v1,t : v0 + t * (v1-v0)
"""two-dimentional linear interpolation"""

ease_curve = lambda t : 6 * t**5 - 15 * t**4 + 10 * t**3
"""A Fade function for smoothing linear interpolation"""
    
def noisemap(x, y, setseed = 0):
    np.random.random(setseed)
    table = np.arange(256,dtype=int)
    np.random.shuffle(table)
    table = np.stack([table,table]).flatten()

    # I converged my solution with a similar implementation found online. 
    # I don't take credit for the following ideas nor present them as my own work 
    # program creator: https://stackoverflow.com/users/7207392/paul-panzer

    # noise components
    a = gradient(table[table[x.astype(int)]+y.astype(int)], x - x.astype(int), y - y.astype(int))
    b = gradient(table[table[x.astype(int)+1]+y.astype(int)],x - x.astype(int)-1,y - y.astype(int))
    c = gradient(table[table[x.astype(int)]+y.astype(int)+1],x - x.astype(int),y - y.astype(int)-1)
    d = gradient(table[table[x.astype(int)+1]+y.astype(int)+1],x - x.astype(int)-1,y - y.astype(int)-1) #n11

    # combine noises
    x1 = bilerp(a,b,ease_curve(x - x.astype(int)))
    x2 = bilerp(c,d,ease_curve(x - x.astype(int)))
    return bilerp(x1,x2,ease_curve(y - y.astype(int)))

def gradient(h,x,y):
    "returns the scalar product of x, y"
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h%4]
    return g[:,:,0] * x + g[:,:,1] * y