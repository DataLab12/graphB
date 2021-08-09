
# Input Datasets for graphB

All datasets are pre-processed to an internal standard csv format
* _users.csv - relates original vertex name to graphB ID
* _edges.csv - signed edge information for each existing edge, and original edge weight, if any  

## Amazon Product [Ratings](https://jmcauley.ucsd.edu/data/amazon/) Data

Data source [link](https://jmcauley.ucsd.edu/data/amazon/)

| Amazon Ratings | Data             | No. vertices in Largest Connected Component | No. edges  in Largest Connected Component | No. cycles in Largest Connected Component |
| :------------- | :--------------- |  ---------------: |  ---------------: | ---------------: | 
| Patio, Lawn, and Garden | [users](Amazon_Garden_users.csv) and [edges](Amazon_Garden_edges.csv) | 735,815	| 939,679	| 203,865 |
| Baby 	  | [users](Amazon_Baby_users.csv) and [edges](Amazon_Baby_edges.csv) | 559,040 | 892,231 | 333,192 |
| Digital Music	| [users](Amazon_Music_users.csv) and [edges](Amazon_Music_edges.csv) | 525,522	| 702,584	| 177,063	| 
| Instant Video	|  [users](Amazon_Video_users.csv) and [edges](Amazon_Video_edges.csv) | 433,702 | 572,834 | 139,133 |
| Musical Instruments | [users](Amazon_Instruments_users.csv) and [edges](Amazon_Instruments_edges.csv) | 355,507 | 457,140 | 101,634 |

## Amazon Product [Reviews](https://jmcauley.ucsd.edu/data/amazon/) Data

Data source [link](https://jmcauley.ucsd.edu/data/amazon/)

| Amazon Ratings | Data             | No. vertices in Largest Connected Component | No. edges  in Largest Connected Component | No. cycles in Largest Connected Component |
| :------------- | :--------------- |  ---------------: |  ---------------: | ---------------: | 
| Digital Music	core5| [users](amazonDigitalMusic_core5_users.csv) and [edges](amazonDigitalMusic_core5_edges.csv) | 9,109 | 64,706 | 55,598 |
| Instant Video	core5 |  [users](amazonVideo_core5_users.csv) and [edges](amazonVideo_core5_edges.csv) | 6,815 | 37,126 |	30,312 |
| Musical Instruments core5 | [users](amazonMusicalInstruments_core5_users.csv) and [edges](amazonMusicalInstruments_core5_edges.csv) | 2,329	| 10,261 | 7,933 |


## [SNAP](http://snap.stanford.edu/data/index.html#signnets) Signed Networks	Data

Data source [link](http://snap.stanford.edu/data/index.html#signnets) 

| Amazon Ratings | Data             | No. vertices in Largest Connected Component | No. edges  in Largest Connected Component | No. cycles in Largest Connected Component |
| :------------- | :--------------- |  ---------------: |  ---------------: | ---------------: | 
| soc-sign-epinions | [users](eopinions_all_edges.csv) and [edges](eopinions_all_edges.csv) | 119,130	| 704,267	| 585,138 |
| soc-sign-Slashdot090221 |  [users](slashdot_all_users.csv) and [edges](slashdot_all_edges.csv) | 82,140	| 500,481	| 418,342 |
| wiki-Elec | [users](wiki_breadthTiming_users.csv) and [edges](wiki_breadthTiming_edges.csv) | 7,539	| 112,058	| 104,520 |
