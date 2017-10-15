# COSC-6368-AI-UH
Projects for COSC 6368

To run the program have 2 possible ways:
1) in command line type: python TSP.py <cost function you want to use (c1,c2,c3)> <Number of cities> <Method (SIM, SOPH, DFS, BFS)>

2) type in file INPUT.txt lines with parameters you want to execute TSP.py. For example:
c1,30,SIM
c2,30,SOPH
c1,10,DFS
and then type in command line: python TSP.py

All the results print out in file OUTPUT.txt. 
IMPORTANT:
Method DFS works best for N=10, for larger number of cities may take a while to produce output.
