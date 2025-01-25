# Internship-2025

This is a repo tracking my progress while working on a project as part of the "Data science for crystal structures" internship within the Open Science project organized by the Czech Academy of Sciences. 

## Formulas for D*

### ChatGPT D* for 2d (Complicated)
This is the general formula he gave me:

$$D^*(P) = sup(x,y)\in [0,1)^2\left| \sum_{(x_{i},y_{i})\in P}^{} 1_{[0,x)\times [0,y)}(x_{i},y_{i}) - xy | (x,y) \in [0,1)^2\right| $$

### Meeting notes (Simpler)

This is the more complicated version:

$$D_{N}^{*} = \begin{matrix}sup \\ B\in  \mathbf{B} \end{matrix}\left | \frac{(P\cap B)}{N} - V(B)\right |$$

This is the simplified version:

$$D_{N}^{*} = \begin{matrix}max \\ B\in  \mathbf{B} \end{matrix}\left | \frac{n}{N} - \frac{a}{A}\right | $$

This is what the following symbols/characters mean : 
- sup and max -> Same thing  (supremum = nejmenší hodnota, která je větší než všechny ostatní :P)  
- B and **B** -> Represents all the possible shapes the area of the region can have (doesnt really matter)
- n and N -> N is the number of all points and n is the number of points inside of area we are checking
- a and A -> A is the total area and a is the area of the part we are checking

## Literature

Jiří Matoušek - Geometric Discrepancy : https://people.fjfi.cvut.cz/vybirja2/TUM-IBC/Matousek_Geometric_Discrepancy.pdf

