#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import sys

### PANDA Imports ###
from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import QueuedConnectionListener
from panda3d.core import ConnectionWriter
from panda3d.core import PointerToConnection, NetAddress, NetDatagram
from panda3d.core import Datagram
from panda3d.core import DatagramIterator

from direct.task.Task import Task

## Server Imports ##
from Client.protocol.opcodes import MSG_NONE

########################################################################


class TCP():

    def __init__(self, _core):
        print ("TCP Protocol Startup...")
        self.core = _core
        self.config = self.core.client.config

        # Connection on TCP 
        self.tcpConnection = None


    def start(self):
        self.setupTCP()
        self.startTCPTasks()


    def setupTCP(self):
        self.tcpManager = QueuedConnectionManager()
        self.tcpReader = QueuedConnectionReader(self.tcpManager, 0)
        self.tcpWriter = ConnectionWriter(self.tcpManager, 0)

    def startTCPTasks(self):
        taskMgr.add(self.tcpReaderTask, "tcpReaderTask", -10)
        print ("TCP Reader Started")


    def tcpReaderTask(self, task):
        """
        Handle any data from clients by sending it to the Handlers.
        """
        while 1:
            (datagram, data, opcode) = self.tcpNonBlockingRead(self.tcpReader)
            if opcode is MSG_NONE:
                # Do nothing or use it as some 'keep_alive' thing.
                break
            else:
                # Handle it
                self.core.packetManager.handlePacket(opcode, data)

        return Task.cont


    # TCP NonBlockingRead??
    def tcpNonBlockingRead(self, qcr):
        """
        Return a datagram collection and type if data is available on
        the queued connection udpReader
        """
        if self.tcpReader.dataAvailable():
            datagram = NetDatagram()
            if self.tcpReader.getData(datagram):
                data = DatagramIterator(datagram)
                opcode = data.getUint8()

            else:
                data = None
                opcode = MSG_NONE

        else:
            datagram = None
            data = None
            opcode = MSG_NONE

        # Return the datagram to keep a handle on the data
        return (datagram, data, opcode)


    def connectToServer(self, _ip, _port):
        self.tcpConnection = self.tcpManager.openTCPClientConnection(_ip, _port, 1000)

        if self.tcpConnection != None:
            self.tcpReader.addConnection(self.tcpConnection)
            # Close the main menu and move the client into the game
            # for now we will make a shortcut
            #self.clientManager.guiManager.menu.hide()