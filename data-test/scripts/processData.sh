#! /bin/sh

# NOT finished yet 

# Wiki
wget http://snap.stanford.edu/data/wikiElec.ElecBs3.txt.gz
gunzip wikiElec.ElecBs3.txt.gz
python wikiRaw_edges_users.py
#fix yaml to work w this file  
mv wiki_timing_edges.csv ../Input_Data/
mv wiki_timing_users.csv ../Input_Data/

wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Amazon_Instant_Video_5.json.gz

python amazon_edges_users.py reviews_Amazon_Instant_Video_5.json.gz

wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Musical_Instruments_5.json.gz

python amazon_edges_users.py reviews_Musical_Instruments_5.json.gz

wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Digital_Music_5.json.gz

python amazon_edges_users.py reviews_Digital_Music_5.json.gz

#move output to Input_Data 

#erase .gz 

#proceed 
exit 0
