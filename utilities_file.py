import numpy as np



   

def array_to_integer(arr):
    binary_string = ''.join(str(i) for i in arr)
    decimal_integer = int(binary_string, 2)
    return decimal_integer    


def integer_to_padded_binary(integer, m):
    binary_string = bin(integer)[2:]  # Converte l'intero in una stringa binaria
    padded_binary_string = binary_string.zfill(2**m)  # Aggiunge lo zero padding
    return padded_binary_string

def to_spin(x):
    return 2*x-1

def rev_to_spin(x):
    return (1/2)*(x+1)

def alpha(N,m):
    return 2**m/N

def volatility(x,N, trans):
    sum_a = np.sum(x[trans:])
    sum_a_sq = (np.sum(x[trans:]**2))
    T=len(x)
    return ((T-trans) * sum_a_sq - sum_a*sum_a)/((T-trans)*(T-trans))


def predictabiity():
    pass


def log_message(agent, message):
    agent.log_info(f'Received: {message}')

def reply(agent, message):
    return 'Received ' + str(message)