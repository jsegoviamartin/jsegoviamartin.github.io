# app.py

from flask import Flask, render_template, request
from Jevons_10 import scenario
import matplotlib.pyplot as plt
import string
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    # Get simulation parameters from the form
    eps = request.form['eps']
    t = request.form['t']
    N = request.form['N']
    bs = request.form['bs']
    r_t0 = request.form['r_t0']
    rep_rate = request.form['rep_rate']
    rebound = request.form['rebound']

    # Run the simulation
    result = scenario(a_effic[0], a_effic[1], a_effic[2], a_effic[3], eps, t, N, bs, r_t0, rep_rate, rebound)

    # Generate the plots
    plt.plot(result[0], label='eps = {}'.format(eps))
    plt.legend()
    plt.xscale('log')
    plt.ylabel('pop. efficiency')
    plt.xlabel('log(time)')
    plt.savefig('pop_efficiency.png')

    plt.plot(result[1], label='eps = {}'.format(eps))
    plt.legend()
    plt.xscale('log')
    plt.ylabel('existing resources')
    plt.xlabel('log(time)')
    plt.savefig('existing_resources.png')

    plt.plot(result[2], label='eps = {}'.format(eps))
    plt.legend()
    plt.xscale('log')
    plt.ylabel('mean consumption')
    plt.xlabel('log(time)')
    plt.savefig('mean_consumption.png')

    # Render the results template and pass the plots to it
    return render_template('results.html', eps=eps, t=t, N=N, bs=bs, r_t0=r_t0, rep_rate=rep_rate, rebound=rebound,
                           pop_efficiency='pop_efficiency.png', existing_resources='existing_resources.png',
                           mean_consumption='mean_consumption.png')
