#!/usr/bin/python

import sys,getopt
import os.path
#require python-whois
import whois

'''
WHOIS.py
Versao 1b
'''

def check_whois(domain,validNS):
    err = 0
    msg = ""
    servers = []
    res = whois.whois(domain)

    if ( not res.status ):
       err = 1
       msg = "DOMAIN NOT FOUND"
    else:
        if ( res.name_servers ):
            servers = res.name_servers
        else:
            if ( res.nserver ):
                servers = res.nserver
            else:
                err = 1
                msg = "NO NAMESERVERS"

    if ( err == 0 ):
        for n in servers:
            if (n.split(' ')[0] in validNS):
                msg = "OK"
                break
            else:
                msg = "OTHER SERVER"

    print domain + ":" + msg


def usage():
    print "USE: " + sys.argv[0] + " -d <DomainFile> -l <ListValidServersFile>"

def readServersList(serversfile):
    try:
        vs = open(serversfile,"r")
    except IOError:
        print "ERRO: Falha ao ler o arquivo ",serversfile
        return None

    vl = vs.readline()
    valid = []
    while True:
        line = vl.split("\n")[0]
        if (len(line) > 0):
            valid.append(line)

        vl = vs.readline()
        if (not vl):
            break
    vs.close()
    return valid;


def main(argv):
    domainfile = ''
    validsrv = ''
    if (len(argv) != 5):
        usage()
        return

    try:
        opts,args = getopt.getopt(argv[1:],"d:l:h")
    except getopt.GetoptError:
        print "ERRO:"
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h","--help"):
            usage()
            sys.exit()
        elif opt in ("-d","--domainfile"):
            domainfile = arg
        elif opt in ("-l","--listvalidserversfile"):
            validsrv = arg

    validServers = readServersList(validsrv)

    if (not validServers or len(validServers) <= 0):
        print "ERRO: Informe pelo menos um servidor para validacao."
        sys.exit(2)

    try:
        fd = open(domainfile,"r")
    except IOError:
        print "ERRO: Falha ao ler o arquivo",domainfile
        sys.exit(2)

    l = fd.readline()
    domain = None
    while True:
        domain = l.split("\n")[0]
        if (len(domain) > 5 and "." in domain):
           check_whois(domain,validServers)

        l = fd.readline()
        if (not l):
            break
    fd.close()


if (__name__ == "__main__"):
    main(sys.argv)
