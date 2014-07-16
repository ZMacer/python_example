#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import reactor, protocol

class LoginClient(protocol.Protocol):
    def connectionMade(self):
        #self.transport.write("#1<<<<<Bh<<<<<<<<<!")
        self.transport.write("#1<<<<<Bh<<<<<<<<<!")

    def dataReceived(self, data):
        print "Server said:", data
        #self.transport.loseConnection()
        
class LoginFactory(protocol.ClientFactory):

    def buildProtocol(self, addr):
        return EchoClient()
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed."
        reactor.stop()
    def clientConnectionLost(self, connector, reason):
        print "Connection lost."
        reactor.stop()

if __name__ == '__main__':
	reactor.connectTCP("192.168.40.220", 7000, LoginFactory())
	reactor.run()
