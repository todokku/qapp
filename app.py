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
            # Create a circuit with 1000 shots with 2 quantum regs and 2 classic regs.
            shots = 1000
            qr = QuantumRegister(2)
            cr = ClassicalRegister(2)
            circuit = QuantumCircuit(qr, cr)

            message = 'Initializing quantum superposition and quantum entanglement (SPOOKY AT A DISTANCE).'
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            sleep(self.delay)
            # Create superposition.
            circuit.h(qr[0])
            # Create entanglement.
            circuit.cx(qr[0], qr[1])

            message = 'Measuing qubits and irrevocably disturbing the superposition state.'
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            sleep(self.delay)
            # Measure circuit.
            circuit.measure(qr, cr)
            
            message = 'Logging into the IBMQ Research HQ at the Thomas J. Watson Research Center.'
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            sleep(self.delay)
            try:
                # Load IBMQ account.
                IBMQ.load_account()
            except:
                # Handle if account is not setup to help the user gain access to 
                # the IBM Q Experience.
                message = 'Please ensure you have your IBM Q Experience account setup properly.  Visit https://github.com/mytechnotalent/qapp for details of how to properly setup your IBM Q Experience account.'
                socketio.emit('newmessage', {'message': message}, namespace='/temp')
                sleep(self.delay)
                temp_disconnect()
            # Look for the least busy quantum computer with the fewest number of queues.
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
            # Execute job on our quantum computer and store the results in new
            # variables, heads and tails.
            job = execute(circuit, shots=shots, backend=backend_new_name)
            from qiskit.tools.monitor import job_monitor
            job_monitor(job)
            result = job.result()
            counts = result.get_counts(circuit)
            tails = int(counts['00'])
            heads = int(counts['11'])  
            # Handle edge case where tails is equal to heads to which we will use
            # chance to determine our outcome utilizing modulo as we need to 
            # understand there are actually 4 values which are 00, 01, 10, 11 
            # however the values of 01 and 10 will be very small based on 
            # the advancement of the quantum computer handling noise.
            if tails == heads:
                if tails % 2 == 0:
                    tails += 1
                else:
                    heads += 1
            # In order to print out our variables we need to cast them to a string.
            str_tails = str(tails)
            str_heads = str(heads)
            
            try:
                message = 'Your Choice: ' + choice
                socketio.emit('newmessage', {'message': message}, namespace='/temp')
                sleep(self.delay)
            except NameError:
                pass

            message = 'Heads has {} counts.'.format(str_heads)
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            message = 'Tails has {} counts.'.format(str_tails)
            socketio.emit('newmessage', {'message': message}, namespace='/temp')
            sleep(self.delay)
            # Logic to determine outcome of the game and present to the results
            # to the user.
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
