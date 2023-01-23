# PixelNaturalSelectionSim

**Natural Selection represented by pixels**

<p align="center"> <img src="patches_length=9.avi" width="640" height="480" /> </p>


Each pixel represents an indiviual organism assigned an n-length genetic code from DNA nucleotides. Pixels randomly reproduce and die at a rate determined by the user. As pixels reproduce, they also have a specified rate of mutation causing one of the DNA nucleotides to be randomly swapped. This also often results in a change of color. A random threat code is selected at the start of the simultion. Pixels that that have mutated to have the same code as this threat code will no longer die. Pixel color for the above simulation was determined by the number of differences in the species code to that of the threat code. Lighter colors represent pixels with a more similair genetic code to that of the threat.

<p align="center"> <img src="full_selection_purple.avi" width="640" height="480" /> </p>


For the above simulation, each genetic code is assigned to a random color by a hash function. 
