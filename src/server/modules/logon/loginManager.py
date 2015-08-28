#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import sys

### PANDA Imports ###
from direct.showbase.ShowBase import ShowBase

## Server Imports ##
from shared.opcodes import *
from server.modules.utils.util import generateUUID
from client import Client

########################################################################


class LoginManager():
    
    def __init__(self, _serverManager):

    	self.serverManager = _serverManager

    
    def handleRegister(self, _data, _client):
    	print "MSG in Packet:", _data.getString()
    	cid = generateUUID()
    	addr = _client#.getAddress()

    	self.serverManager.clients[cid] = Client(cid, addr)

    	# Send reply to client & tell client about other already connected clients
        for client in self.serverManager.clients:
            connectedClientIds = []
            ids = self.serverManager.clients[client].id
            connectedClientIds.append(ids)

        pkt = self.serverManager.packetManager.packet.buildPacket(MSG_REGISTER_ACK, connectedClientIds)
        self.serverManager.udpConnection.sendPacket(pkt, addr)

        # Update other clients about the new client
        pkt = self.serverManager.packetManager.packet.buildRegisterBroadcast(cid)
        self.serverManager.udpConnection.sendBroadcast(pkt, cid)

    	