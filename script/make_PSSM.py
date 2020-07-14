import sys
import argparse
import pickle
import pandas as pd
import numpy as np
import sys
from matrix2 import *


def mapAligns(gapped_fam_dict, alphamap):
    """convert alignments in the new alphabet"""
    for RF in gapped_fam_dict:
        print(RF)
        for ID in gapped_fam_dict[RF]:
            if gapped_fam_dict[RF][ID].get('bear') :
                gapped_fam_dict[RF][ID]['alpha'] = "".join([alphamap[ch] 
                                                            for ch in gapped_fam_dict.get(RF).get(ID).get('bear')])


#mbrVersion = "Zbear_62"
mbrVersion = sys.argv[1]

#MBR = "62/MBR_Zbear_62.tsv"
MBR = sys.argv[2]

#ALPHAMAP = "Zbear.tsv"
ALPHAMAP = sys.argv[3]

GAPFAMDICT = "gapped_fam_dict.pickle"

ignore_these_families = ['RF00210','RF01879', 'RF02767', 'RF02768','RF02770', 'RF02773', 'RF02775','RF02781', 'RF02783']


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mbr", help="the substitution matrix to test")
parser.add_argument("-a", "--alpha", help="pickle of alphabet dictionary (must correspond to the alphabet \
                                            used with the substitution matrix). With respect to standard BEAR")
parser.add_argument("-gfd", "--gapfamdict", help="the rfam alignments with gaps and bear pickle")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")

args = parser.parse_args(args=['--alpha', ALPHAMAP,'-v', '-m',MBR, '-gfd', GAPFAMDICT])

with open(args.gapfamdict, 'rb') as afile:
    gapped_fam_dict = pickle.load(afile)
    
    
f=open(args.alpha).readlines()
alph_bear={x.split()[0]:x.split()[1] for x in f}
alph_bear['-']='-'

alphamaps = [{key:alph_bear[KEY] for key in KEY} for KEY in alph_bear]
alphamap = {}
for ap in alphamaps:
    alphamap.update(ap)
    
mbr=pd.read_table(args.mbr, index_col=0)

mapAligns(gapped_fam_dict, alphamap)

rfams = {}
for RF in gapped_fam_dict:
    print(RF)
    if RF not in ignore_these_families:
        rfams[RF] = [ [gapped_fam_dict[RF][ID]['sequence'] for ID in gapped_fam_dict[RF]],
                     [gapped_fam_dict[RF][ID]['alpha'] for ID in gapped_fam_dict[RF]] ]
    



PSSMs_alpha = []

rfam_list = []
#use RFAMS 
counter = 0
for rfam in rfams:
    print(rfam)
    rfam_list.append(rfam)  
    PSSM_b = buildPSSM_alphabet(rfams[rfam], mbr) ###TODO load MBR (dataframe)
    
    PSSMs_alpha.append(PSSM_b)
    counter+=1
    
with open('rfam_PSSM_{}.pickle'.format(mbrVersion), 'wb') as handle:
    pickle.dump(PSSMs_alpha, handle)
    
    
dic_PSSM={}
for i in range(0, len(rfam_list)):
    dic_PSSM[rfam_list[i]]=PSSMs_alpha[i]
    
    
with open('rfam_PSSM_dic_{}.pickle'.format(mbrVersion), 'wb') as handle:
    pickle.dump(dic_PSSM, handle) 