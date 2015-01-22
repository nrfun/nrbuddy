// nrbuddy.js
// ibuddy node red wrapper
// cwhite
// Jan 2015


"option strict";
var util = require('util');
var exec  = require('child_process').exec;
var spawn = require('child_process').spawn;
var fs    = require('fs');

var wrapperCommand = __dirname+'/nrbuddy.sh';

module.exports = function(RED) {

    
    if (!fs.existsSync("/dev/ttyAMA0")) { // unlikely if not on a Pi
        throw "Info : Ignoring Raspberry Pi specific node.";
    }

    // TODO: detect we have the correct usb and pyBuddy pieces


    
    function NRBuddy(config) {
        RED.nodes.createNode(this,config);
        var node = this;

        node.log("nrbuddy");

        var command    = config.command;



		if(RED.settings.verbose){ node.log( "cmd: " + command); }

        startBuddyDriver(node);
        node.status({fill:"amber",shape:"circle",text:"ooo"});
        node.on('input', function(msg) {
            if(RED.settings.verbose) { node.log("string " + msg.payload);}
            msg.command = command;
            display(node, msg);
            node.status({fill:"green",shape:"circle",text:msg.payload});
        });

        
        node.on("close", function() {
            // Called when the node is shutdown - eg on redeploy.
            node.log("closing in js node" );
            stopBuddyDriver(this);
        });


        // --- child events

        node.child.stderr.on('data', function (data) {
            if (RED.settings.verbose) { node.log("err: "+data+" :"); }
        });

        node.child.on('close', function (code) {
            if (RED.settings.verbose) { node.log("ret: "+code+" :"); }
            node.child = null;
            node.running = false;
            node.status({fill:"red",shape:"circle",text:""});
        });

        node.child.on('error', function (err) {
            if (err.errno === "ENOENT") { node.warn('Command not found'); }
            else if (err.errno === "EACCES") { node.warn('Command not executable'); }
            else { node.log('error: ' + err); }
        });

    }
    RED.nodes.registerType("nrbuddy",NRBuddy);
}


// call out to the python wrapper, but tell it to stick around
function startBuddyDriver(node) {
    node.log("starting the 'driver'");
    node.child = spawn(wrapperCommand, ["persist"]);
}



function stopBuddyDriver(node) {
    if (node.child != null) {
        node.child.stdin.write("close");
        node.child.kill('SIGKILL');
    }
    
    // should probably make that conditional.
    node.log("driver stopped");
}




// send the message out to the PIFaceCAD lcd module via the python process we
// started earlier
function display(node, msg) {
    console.log( "got:" + msg.command);
	
    // preprocess the string if we want
    //  - dimensions?
    //  - screen scrollage?

    // clear the screen
    // push the new message 
    
    
    if (node.child != null) {
        node.log("push the msg to the buddy");
        //node.child.stdin.write('light ' + msg.light +  '\n');
        node.child.stdin.write( ""+msg.command +  '\n');
    } else {
        executeCmd(node, ""+msg.command );
    }

} // display function

// hand off to the python process via stdio
function executeCmd(node, commandString) {
    node.log ("execute " + commandString)
    exec(wrapperCommand + " " + commandString, function(error, stdout, stderr) {
        node.log('stdout: ', stdout);
        node.log('stderr: ', stderr);
        if (error !== null) {
            console.log('exec error: ', error);
        }
    });
}


