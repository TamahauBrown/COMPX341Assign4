import time
import sympy 
import redis
import argparse

from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/isPrime/<number>')
def hello(number):
    primeNumbers = [];
    i = 0;
    count = int(number)
    if(cache.exists(count)):
        return "{} is prime".format(count)

    else:
        #This checks if it is a prime number using the library from https://www.sympy.org/en/ index.html
        if sympy.isprime(count):
             cache.set(count, "")
             #primeNumbers.set(count)
             return "{} is prime".format(count)

        else:
            return "{} is not prime".format(count)

@app.route('/primesStored/')
def getPrimes():
    val = ""
    for n in cache.keys():
        val = val + " " + str(int(n))
    
    return val
