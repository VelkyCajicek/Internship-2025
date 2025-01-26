# Internship-2025

This is a repo tracking my progress while working on a project under the guidance of my lecturer, Wolfgang Hornfeck, as part of the 'Data Science for Crystal Structures' internship within the Open Science project organized by the Czech Academy of Sciences.

## Formulas for D*

### Meeting version (Simplest)

This is the more complicated version:

$$D_{N}^{*} = \begin{matrix}sup \\ B\in  \mathbf{B} \end{matrix}\left | \frac{(P\cap B)}{N} - V(B)\right |$$

This is the simplified version:

$$D_{N}^{*} = \begin{matrix}max \\ B\in  \mathbf{B} \end{matrix}\left | \frac{n}{N} - \frac{a}{A}\right | $$

This is what the following symbols/characters mean : 
- sup and max -> Either max or smallest value thats larger than every other value :P 
- B and **B** -> Represents all the possible shapes the area of the region can have (doesnt really matter)
- n and N -> N is the number of all points and n is the number of points inside of area we are checking
- a and A -> A is the total area and a is the area of the part we are checking

[Implementation here : ](Star_Discrepancy/Simple_Algorithm.py)

### Bundschuh & Zhu algorithm(Don't yet understand)

This one is supposed to be the faster one for D*, but I as of 26.1.25 I dont understand it

$$D_{n}(pointset) = max(0\leq l< n)max(0\leq k< l)max(\left | k/n -  x_{l}\xi_{l,k} \right|, \left | k/n -  x_{l+1}\xi_{l,k+1} \right |) $$

[Implementation here : ](Star_Discrepancy/Bundschuh_Zhu_Algorithm.py)

### ChatGPT D* for 2d (Complicated)
This is the general formula he gave me:

$$D^*(P) = sup(x,y)\in [0,1)^2\left| \sum_{(x_{i},y_{i})\in P}^{} 1_{[0,x)\times [0,y)}(x_{i},y_{i}) - xy | (x,y) \in [0,1)^2\right| $$

## Books containing formulas

Jiří Matoušek - Geometric Discrepancy : https://people.fjfi.cvut.cz/vybirja2/TUM-IBC/Matousek_Geometric_Discrepancy.pdf

