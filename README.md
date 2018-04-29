## Routing and Wavelength Assignment Simulator
[Paper](https://link.springer.com/chapter/10.1007%2F978-3-319-65340-2_35): 
A Genetic Algorithm (GA) Approach for Routing and Wavelength Assignment (RWA) in
All-Optical Wavelength Division Multiplexing (WDM) Networks with Static Traffic
(SLE, which stands for _Static Lightpath Establishment_)

This repo basically basically contains a simulator that covers the routing and
wavelength assignment problem with the following algorithms:

* Routing 
    * Dijkstra's algorithm  
    * Yen's algorithm (also known as K-shortest path algorithm)  

* Wavelength Assignment
    * First-fit algorithm  
    * Vertex coloring algorithm  

* RWA as one   
     * General Objective Function  
     * Genetic algorithm (ours :)  

## Citation

If you use this code or want to mention the paper referred above, please cite us
as one of the following: 

>Teixeira D.B.A., Batista C.T., Cardoso A.J.F., de S. Araújo J. (2017) A Genetic Algorithm Approach for Static Routing and Wavelength Assignment in All-Optical WDM Networks. In: Oliveira E., Gama J., Vale Z., Lopes Cardoso H. (eds) Progress in Artificial Intelligence. EPIA 2017. Lecture Notes in Computer Science, vol 10423. Springer, Cham

```
@inproceedings{Teixeira17,
	author    = {Teixeira, Diego Bento A. and Batista, Cassio T. and Cardoso, Afonso Jorge F. and de S. Ara{\'u}jo, Josivaldo},
	editor    = {Oliveira, Eug{\'e}nio and Gama, Jo{\~a}o and Vale, Zita and Lopes Cardoso, Henrique},
	title     = {A Genetic Algorithm Approach for Static Routing and Wavelength Assignment in All-Optical WDM Networks},
	booktitle = {Progress in Artificial Intelligence},
	year      = {2017},
	publisher = {Springer International Publishing},
	address   = {Cham},
	pages     = {421--432},
	doi       = {10.1007/978-3-319-65340-2_35},
	url       = {\url{https://github.com/cassiobatista/RWA-WDM}},
	isbn      = {978-3-319-65340-2}
}
```
