import time as tempo
from tqdm import tqdm 
from utilities_file import *
from model_file import *
import matplotlib.pyplot as plt

def main():
    N=201
    trans=500
    x=[]
    y=[]
    t1=tempo.time()
    for m in tqdm([3,7,11,13]):
        model=MinorityGame(m,N,2,'highest_score','random')
        
        for t in tqdm(range(1000)):
            model.step()
        ini = model.datacollector.get_model_vars_dataframe()
        y.append(volatility(ini,N,trans))
        x.append( alpha(N,m))
    t2=tempo.time()    

    

    print(f"exec time:{t2-t1} ")
        
    plt.loglog(x,y,'*-')
    plt.show()

    
if __name__=='__main__':
    main()