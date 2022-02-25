# graphB 

**graphB** algorithmm implements graph frustration cloud and resulting concensus measures

** Automated run on sample data** - The example is set to run 10 trees 
	```
     >>source [testRun.sh](testRun.sh]	 
	```
**graphB [notebook](graphB/GRAPHB.md)** contains detailed setup and run steps 

# Citation

Please cite this publication:  Rusnak, L., Tešić, J. [_Characterizing attitudinal network graphs through frustration cloud_](https://link.springer.com/article/10.1007/s10618-021-00795-z). Data Min Knowl Disc 35, 2498–2539 (2021). 

 **BibTeX entry:**
 
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
 
# [Docker image of the test run](https://hub.docker.com/repository/docker/jtesic/graph_balancing)
   
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

# Next Steps

* Timing Analysis [experiment](graphB/TIMING.md)
* [Detailed timing experiment](data-test/TIMING.md)
* [Data Format and code run](data-test/README.md)
  
  
[Data Lab @ TXST](DataLab12.github.io)
