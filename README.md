#  Automated run on sample data 
	```
     >>source [testRun.sh](testRun.sh]	 
	```
   * The example is set to run 10 trees, 1000 trees from the paper would take too long.
   
## [Docker image of the test run](https://hub.docker.com/repository/docker/jtesic/graph_balancing)
   
   1. Install [Docker](https://docs.docker.com/get-docker/)
   2. In terminal: 
   ```
   >>docker pull jtesic/graph_balancing:latest
   >>docker run latest
   ```
   * To build docker image in current folder
   ```
   >>docker build -t latest .
   >>docker run latest
   >>docker tag latest <USERNAME>/<REPO>:latest
   >>docker push <USERNAME>/<REPO>:latest
   ```

# Citation 

Please cite graphB 2020 publication if it helps your research:  Rusnak, L., Tešić, J. [_Characterizing attitudinal network graphs through frustration cloud_](https://link.springer.com/article/10.1007/s10618-021-00795-z). Data Min Knowl Disc 35, 2498–2539 (2021). 

BibTeX entry: 

```
@article{2020Cloud,
  author       = {Lucas Rusnak and Jelena Te\v{s}i\'{c}},
  title        = {Characterizing Attitudinal Network Graphs through Frustration Cloud},
  journal = {Data Mining and Knowledge Discovery},
  volume = {6},
  no = {35},
  month        = {November},
  year         = {2021},
  publisher = {Springer},
  doi = {https://doi.org/10.1007/s10618-021-00795-z}
}
```
  
# graphB 

**graphB** algorithmm, short for **graph B**alancing, implements graph frustration cloud and resulting graph measures, as presented in this [paper](https://arxiv.org/abs/2009.07776).  

The graphB project is led by  Texas State faculty [Jelena Tešić](jtesic.github.io) and [Lucas Rusnak](https://www.math.txstate.edu/about/people/faculty/rusnak.html). First public release og graphB software was summer 2020 (ver 1.0 development led by graduate student [Joshua Mitchell](https://lelon.io/), and second release was Dec 2020, led by undergraduate student [Eric Hull](https://github.com/hullo-eric).  
* Timing Analysis [experiment](graphB/TIMING.md)
* graphB [notebook](graphB/GRAPHB.md) contains detailed setup and run steps 

* Martin Burtscher's team scaled the discovery and balancing of fundamental cycles in 2021, and allowed us to extend the frustration cloud concept to larger social graphs, see new implementation [here](https://userweb.cs.txstate.edu/~burtscher/research/graphB/).

## Timing Analysis 

  * [Detailed timing experiment](data-test/TIMING.md)
  * [Data Format and code run](data-test/README.md)


[Data Lab @ TXST](DataLab12.github.io)
