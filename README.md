# bio-image
This file ectracts trakingdata of cells from TrackMate XML and save it into a file similar to StarryNite (Bao Z, PNAS 2006) output.
Output is
X Y Z T ID Mother_ID Daughter1_ID Daughter2_ID #ofEdge
 
*******
T->1 start
ID-> if null, ID is set -1

Assumption:
Cell cannot divide into more than two.

HowtoCall:
Run from the Fiji's script editor.




