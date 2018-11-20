#!/bin/bash

# Gera todos os prefixos /48 possiveis de um bloco ipv6 /32
# Versao 1 beta

bloco="2001:db8:"
len=48


for m in `seq 0  15`
do
	for c in `seq 0 15`
	do
		for d in `seq 0 15`
		do
			for u in `seq 0 15`
			do
				printf "$bloco%x%x%x%x::/$len\n" $m $c $d $u
			done
		done
	done
done
