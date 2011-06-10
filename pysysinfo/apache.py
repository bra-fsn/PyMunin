"""Implements ApacheInfo Class for gathering stats from Apache Web Server.

The statistics are obtained by connecting to and querying the server-status
page of local and/or remote Apache Web Servers. 

"""

__author__="Ali Onur Uyar"
__date__ ="$Dic 29, 2010 2:55:43 PM$"

import re
import urllib
import util


defaultApachePort = 80
defaultApacheSSLport = 443

buffSize = 4096


class ApacheInfo:
    """Class to retrieve stats for Apache Web Server."""

    def __init__(self, host=None, port=None, user=None, password=None,
                 ssl=False, autoInit=True):
        """Initialize Apache server-status URL access.
        
        @param host:     Apache Web Server Host. (Default: 127.0.0.1)
        @param port:     Apache Web Server Port. (Default: 8080, SSL: 8443)
        @param user:     Username. (Not needed unless authentication is required 
                             to access server-status page.
        @param password: Password. (Not needed unless authentication is required 
                             to access server-status page.
        @param ssl:      Use SSL if True. (Default: False)
        @param autoInit: If True connect to Apache Web Server on creation.
            
        """
        if host is not None:
            self._host = host
        else:
            self._host = '127.0.0.1'
        if port is not None:
            self._port = port
        else:
            if ssl:
                self._port = defaultApacheSSLport
            else:
                self._port = defaultApachePort
        self._user = user
        self._password = password
        if ssl:
            self._proto = 'https'
        else:
            self._proto = 'http'
        self._statusDict = None 
        if autoInit:
            self.initStats()

    def initStats(self):
        """Query and parse Apache Web Server Status Page."""
        if self._user is not None and self._password is not None:
            url = "%s://%s:%s@%s:%d/server-status?auto" % (self._proto,
                urllib.quote(self._user), urllib.quote(self._password), 
                self._host, self._port)
        else:
            url = "%s://%s:%d/server-status?auto" % (self._proto, self._host, self._port)
        fp = urllib.urlopen(url)
        response = ''
        oldlen = 0
        newlen = 0
        while True:
            response += fp.read(buffSize)
            newlen = len(response)
            if newlen - oldlen == 0:
                break
            else:
                oldlen = newlen
        fp.close()
        self._statusDict = {}
        for line in response.splitlines():
            mobj = re.match('(\S.*\S)\s*:\s*([\w\.]+)$', line)
            if mobj:
                self._statusDict[mobj.group(1)] = util.parse_value(mobj.group(2))
        if self._statusDict.has_key('Scoreboard'):
            self._statusDict['MaxWorkers'] = len(self._statusDict['Scoreboard'])
    
    def getServerStats(self):
        """Return Stats for Apache Web Server.
        
        @return: Dictionary of server stats.
        
        """
        return self._statusDict;
    
        