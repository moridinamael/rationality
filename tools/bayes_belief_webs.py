# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 12:40:35 2017

@author: mfreeman
"""

from bayesian.bbn import build_bbn

def f_coina(flipa):
    if(flipa=='H'):
        return 0.5
    elif(flipa=='T'):
        return 0.5

def f_coinb(flipa,flipb):
    if(flipa=='H'):
        if(flipb=='H'):
            return 0.6
        elif(flipb=='T'):
            return 0.4

    elif(flipa=='T'):
        if(flipb=='H'):
            return 0.5
        elif(flipb=='T'):
            return 0.5


if __name__ == '__main__':

    coins = build_bbn(
        f_coina,
        f_coinb,
        domains=dict(flipa=['H','T'],
                     flipb=['H','T']))