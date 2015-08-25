#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import os
from panda3d.core import (
    ConfigVariableInt,
    ConfigPageManager,
    OFileStream,
    loadPrcFile,
    Filename
)

########################################################################

prcFile = os.path.join("..", "client.prc")

class Config():

    def __init__(self):
        # if exist load the config file
        if os.path.exists(prcFile):
            loadPrcFile(Filename.fromOsSpecific(prcFile))
        # set the variables using the config files content or set a default value
        self.UDPPORT = ConfigVariableInt('udp-port', '6001').getValue()
        self.TIMEOUT = ConfigVariableInt('timeout-in-ms', '3000').getValue()

    def WritePRCFile(self):
        page = None
        customConfigVariables = ["", "port", "timeout-in-ms"]
        if os.path.exists(prcFile):
            # load the existing config file
            page = loadPrcFile(Filename.fromOsSpecific(prcFile))
            removeDecls = []
            for dec in range(page.getNumDeclarations()):
                # Check if our variables are given.
                # NOTE: This check has to be done to not loose our base or other
                #       manual config changes by the user
                if page.getVariableName(dec) in customConfigVariables:
                    decl = page.modifyDeclaration(dec)
                    removeDecls.append(decl)
            for dec in removeDecls:
                page.deleteDeclaration(dec)
        else:
            # create a new config file
            cpMgr = ConfigPageManager.getGlobalPtr()
            page = cpMgr.makeExplicitPage("Grim Net Pandaconfig")

        # config declarations
        page.makeDeclaration("port", str(self.UDPPORT))
        page.makeDeclaration("timeout-in-ms", str(self.TIMEOUT))

        # create a stream to the specified config file
        configfile = OFileStream(prcFile)
        # and now write it out
        page.write(configfile)
        # close the stream
        configfile.close()


#s = Config()
#s.WritePRCFile()
# Writing & Testing
#s = Config()
