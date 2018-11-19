#!/usr/bin/python

import sys,getopt
import os.path
#require pythondns
#USE: pip install pythondns
import dns.resolver

'''
DNSCheck.py
Versao 0
'''

#You can change myNameServers for query yours NameServers
myNameServers = ['8.8.8.8','1.1.1.1']

def check_Record(host,qtype,validServers):
    print host
    print qtype
    print validServers

    flag = 0
    motivo = ""
    answers = None

    rs = dns.resolver.Resolver(configure=False)
    rs.nameservers = myNameServers
    try:
        answers = rs.query(host,qtype)
    except dns.resolver.NoNameservers:
        motivo = "NoNameServers"
        pass
    except dns.resolver.NoAnswer:
        motivo = "NoAnswer"
        pass
    except dns.resolver.NXDOMAIN:
        motivo = "NXDOMAIN"
        pass
    except dns.exception.Timeout:
        motivo = "Timeout"
        pass
    
    if (answers):
        for r in answers:
            record = r.to_text()
            if record in str(validServers):
                flag = 1
                break
            else:
                motivo = "OTHER Server"
    else:
        motivo = "NAO EXISTE REGISTRO " + qtype

    if (flag == 1):
        print host,":OK"
    else:
        print host,":",motivo



def usage():
    print "USE: " + sys.argv[0] + " -d <HostsFile> -l <ListValidServersFile>"

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
    hostsfile = ''
    validsrv = ''
    rType = 'a'

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
        elif opt in ("-d","--hostsfile"):
            hostsfile = arg
        elif opt in ("-l","--listvalidserversfile"):
            validsrv = arg

    validServers = readServersList(validsrv)

    if (not validServers or len(validServers) <= 0):
        print "ERRO: Informe pelo menos um servidor para validacao."
        sys.exit(2)

    try:
        fd = open(hostsfile,"r")
    except IOError:
        print "ERRO: Falha ao ler o arquivo",hostsfile
        sys.exit(2)

    l = fd.readline()
    host = None
    while True:
        host = l.split("\n")[0]
        if (len(host) > 5 and "." in host):
           check_Record(host,rType,validServers)

        l = fd.readline()
        if (not l):
            break
    fd.close()


if (__name__ == "__main__"):
    main(sys.argv)
