#!/bin/bash
for idthres in 90 62 50; do
  for alph in "bear" "qbear" "zbear"; do
    echo "Calculating RIG scores applying the $alph encoding, and removing redundant primary sequences up to a $idthres% of identity"
    python3 scripts/make_RNA_Blocks.py outputs/alignments/bear_new_alignment_${alph}_${idthres} ${idthres} alphabets/${alph}.tsv
    python3 scripts/make_MBR.py outputs/RNA_Blocks/blocks_new_bear_${alph}_${idthres} ${idthres} data/alphabets/${alph}.tsv ${alph}_${idthres}
    python3 scripts/make_PSSM.py ${alph}_${idthres} outputs/MBRs/${alph}_${idthres}/MBR_${alph}_${idthres}.tsv data/alphabets/${alph}.tsv data/Rfam14.2/gapped_fam/gapped_fam_dict.pickle.gz
    python3 scripts/compute_RIG.py outputs/sPSSMs/${alph}_${idthres}/rfam_PSSM_dic_${alph}_${idthres}.pickle
  done
done