#
# QCoin
# *****
# 
# Created by Kevin Thomas 11/16/19.
# Modified by Kevin Thomas 11/16/19.
# Apache License, Version 2.0
# 
# QCoin is the worlds FIRST qapp!  A qapp is a full-stack quantum
# application that interfaces directly with the IBMQ Research HQ at
# the Thomas J. Watson Research Center in the cloud.  QCoin is a
# heads or tails game to which the user chooses either heads or
# tails when the game begins.  The application then connects to a
# REAL IBMQ quantum computer to which it will put qubit 1 into
# superposition and then entangle two qubits and finally measure the
# qubits, irrevocably disturbing the superposition state and forcing
# a classical 0 or 1 as output to determine the games result.
#


from flask_socketio import SocketIO, emit
from flask import Flask, request, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import numpy as np
from qiskit import *

__author__ = 'mytechnotalent'

app = Flask(__name__)
app.config['SECRET_KEY'] = '8675309'
app.config['DEBUG'] = True
socketio = SocketIO(app)

thread = Thread(daemon=True)
thread_stop_event = Event()


class MessageThread(Thread):
    '''
    MessageThread class to allow SocketIO RESTful operations within the app.
    '''
    def __init__(self):
        self.delay = 1
        super(MessageThread, self).__init__()

    def gameEngine(self):
        '''
        Game engine comprising the coin toss logic with the IBM
        quantum computer.
        '''
        try:
            message = 'Initializing qapp.'
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            sleep(self.delay)

            message = 'Creating circuit of two quantum registers and two classical registers.'
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            sleep(self.delay)
            shots = 1000
            qr = QuantumRegister(2)
            cr = ClassicalRegister(2)
            circuit = QuantumCircuit(qr, cr)

            message = 'Initializing quantum superposition and quantum entanglement (SPOOKY AT A DISTANCE).'
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            sleep(self.delay)
            circuit.h(qr[0])
            circuit.cx(qr[0], qr[1])

            message = 'Measuing qubits and irrevocably disturbing the superposition state.'
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            sleep(self.delay)
            circuit.measure(qr, cr)
            
            message = 'Logging into the IBMQ Research HQ at the Thomas J. Watson Research Center.'
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            sleep(self.delay)
            try:
                IBMQ.load_account()
            except:
                message = 'Please ensure you have your IBM Q Experience account setup properly.  Visit https://github.com/mytechnotalent/qapp for details of how to properly setup your IBM Q Experience account.'
                socketio.emit('newmessage', {'message': message}, namespace='/temp')
                sleep(self.delay)
                temp_disconnect()
            from qiskit.providers.ibmq import least_busy
            provider = IBMQ.get_provider(hub='ibm-q')
            IBMQ.get_provider(project='main')
            least_busy_device = provider.backends(filters=lambda x: x.configuration().n_qubits >= 5 
                                                  and not x.configuration().simulator)
            backend = least_busy(least_busy_device)
            backend_name = backend.name()
            backend_new_name = provider.get_backend(backend_name)
            
            message = 'Executing application on the REAL IBMQ {} quantum computer!'.format(backend_new_name)
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            sleep(self.delay)
            job = execute(circuit, shots=shots, backend=backend_new_name)
            from qiskit.tools.monitor import job_monitor
            job_monitor(job)
            result = job.result()
            counts = result.get_counts(circuit)
            tails = int(counts['00'])
            heads = int(counts['11'])  
            str_tails = str(tails)
            str_heads = str(heads)
            try:
                message = 'Your Choice: ' + choice
                socketio.emit('newmessage', {'message': message}, namespace='/temp')
                sleep(self.delay)
            except NameError:
                pass
            message = 'Heads has {} counts out of 1000 shots.'.format(str_heads)
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            message = 'Tails has {} counts out of 1000 shots.'.format(str_tails)
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            sleep(self.delay)
            if choice == 'heads' and heads > tails:
                message = 'YOU WON!'
                socketio.emit('newmessage', {'message': message}, namespace='/temp')
                sleep(self.delay)
            elif choice == 'tails' and tails > heads:
                message = 'YOU WON!'
                socketio.emit('newmessage', {'message': message}, namespace='/temp')
                sleep(self.delay)
            elif choice == 'heads' and heads < tails:
                message = 'YOU LOST!'
                socketio.emit('newmessage', {'message': message}, namespace='/temp')
                sleep(self.delay)
            elif choice == 'tails' and tails < heads:
                message = 'YOU LOST!'
                socketio.emit('newmessage', {'message': message}, namespace='/temp')
                sleep(self.delay)

            temp_disconnect()
        
        except:
            temp_disconnect()

    def run(self):
        self.gameEngine()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global choice
        choice = request.form.get('choice')

        return render_template('index.html', choice=choice)   

    return render_template('index0.html')

@app.route('/about')
def about():
    return render_template('about.html')

@socketio.on('connect', namespace='/temp')
def temp_connect():
    global thread
    print('Client Connected...')

    if not thread.isAlive():
        print("Starting Thread...")
        thread = MessageThread()
        thread.start()

@socketio.on('disconnect', namespace='/temp')
def temp_disconnect():
    print('Client Disconnected...')
    print("Stopping Thread...")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
