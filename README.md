# Natural Selection By Pixels

https://user-images.githubusercontent.com/91089724/214685450-2acb3162-f718-4693-9f88-386edac01ce7.mp4

Each pixel represents an indiviual organism assigned an n-length genetic sequence from DNA nucleotides. Pixels randomly reproduce and die at a rate determined by the user. As pixels reproduce, they also have a specified rate of mutation causing one of the DNA nucleotides to be randomly swapped. This also often results in a change of color. A random threat sequence is selected at the start of the simultion. Pixels that have mutated to have the same sequence as this threat sequence will no longer die. Pixel color for the above simulation was determined by the number of differences in the species sequence to that of the threat sequence. Lighter colors represent pixels with a more similair genetic sequence to that of the threat.

https://user-images.githubusercontent.com/91089724/214709186-afd6bbc9-bd5c-4876-883d-f9cf9604bad7.mp4

For the above simulation, each genetic sequence is assigned to a random color by a hash function. 

**Adding Sexual Selection (Bacterial Conjugation)**

For this simulation, mutations only occur when a pixel is born near two pixels with different genetic sequences. The two sequences are randomly spliced together as a result.

https://user-images.githubusercontent.com/91089724/214709548-ce292432-5bf2-46df-a312-4b0f3d37b047.mp4




