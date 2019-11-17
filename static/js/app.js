//
// QCoin
// *****
// 
// Created by Kevin Thomas 11/16/19.
// Modified by Kevin M. Thomas 11/16/19.
// CC BY
// 
// QCoin is the worlds FIRST qapp!  A qapp is a full-stack quantum
// application that interfaces directly with the IBMQ Research HQ at
// the Thomas J. Watson Research Center in the cloud.  QCoin is a
// heads or tails game to which the user chooses either heads or
// tails when the game begins.  The application then connects to a
// REAL IBMQ quantum computer to which it will put qubit 1 into
// superposition and then entangle two qubits and finally measure the
// qubits, irrevocably disturbing the superposition state and forcing
// a classical 0 or 1 as output to determine the games result.
//


$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/temp');
    var messages_received = [];

    socket.on('newmessage', function(msg) {
        console.log("Received Message" + msg.message);
        
        if (messages_received.length >= 10){
            messages_received.shift()
        }            
        
        messages_received.push(msg.message);
        messages_string = '';
        
        for (var i = 0; i < messages_received.length; i++) {
            messages_string = messages_string + '<p>' + messages_received[i].toString() + '</p>';
        }
        $('#log').html(messages_string);
    });
});