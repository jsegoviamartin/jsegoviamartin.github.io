# app.py

from flask import Flask, render_template, request
from Jevons_10 import scenario
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import string
import random
from io import BytesIO
import base64


a_effic = [0, 1, 2, 3]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    # Get simulation parameters from the form
    eps = float(request.form.get('eps', '1'))
    t = int(request.form.get('t', '1'))
    N = int(request.form.get('N', '1'))
    bs = float(request.form.get('bs', '1'))
    r_t0 = int(request.form.get('r_t0', '1'))
    rep_rate = float(request.form.get('rep_rate', '1'))
    rebound = float(request.form.get('rebound', '1'))

    a_effic = [0, 1, 2, 3]  # a_effic stands for efficiency rewards. We assume an equivalence
    # with the efficiency vector: Efficiency of acions=Rewards/10. That's it, we assume efficiencies from 0 to 0.3 in
    # steps of 0.1.

    # Run the simulation
    result = scenario(a_effic[0], a_effic[1], a_effic[2], a_effic[3], eps, t, N, bs, r_t0, rep_rate, rebound)

    # Generate the plots
    fig1, ax1 = plt.subplots()
    ax1.plot(result[0], label='eps = {}'.format(eps))
    ax1.legend()
    ax1.set_xscale('log')
    ax1.set_ylabel('pop. efficiency')
    ax1.set_xlabel('log(time)')

    buf1 = BytesIO()
    fig1.savefig(buf1, format='png')
    buf1.seek(0)
    pop_efficiency_plot = base64.b64encode(buf1.getvalue()).decode('ascii')

    fig2, ax2 = plt.subplots()
    ax2.plot(result[1], label='eps = {}'.format(eps))
    ax2.legend()
    ax2.set_xscale('log')
    ax2.set_ylabel('existing resources')
    ax2.set_xlabel('log(time)')

    buf2 = BytesIO()
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    existing_resources_plot = base64.b64encode(buf2.getvalue()).decode('ascii')

    fig3, ax3 = plt.subplots()
    ax3.plot(result[2], label='eps = {}'.format(eps))
    ax3.legend()
    ax3.set_xscale('log')
    ax3.set_ylabel('mean consumption')
    ax3.set_xlabel('log(time)')

    buf3 = BytesIO()
    fig3.savefig(buf3, format='png')
    buf3.seek(0)
    mean_consumption_plot = base64.b64encode(buf2.getvalue()).decode('ascii')

    # Render the results template and pass the plots to it
    return render_template('results.html', eps=eps, t=t, N=N, bs=bs, r_t0=r_t0, rep_rate=rep_rate, rebound=rebound,
                           pop_efficiency_plot=pop_efficiency_plot, existing_resources_plot=existing_resources_plot,
                           mean_consumption_plot=mean_consumption_plot)


if __name__ == '__main__':
    app.run()
