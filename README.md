# ID3 Decision Tree Learning Algorithm

This repository contains a basic implementation of ID3 (Iterative Dichotomiser 3) Decision Tree Learning Algorithm with error-reduced pruning from gound up.

```python
parse.py # takes a filename and returns attribute information and all the data in array of dictionaries
```

```python
node.py # defines the node class
```

```python
ID3.py # contains the main implementation of the algorithm
```

```python
house_votes_84.data # contains the data used
```

To test all functions, run:
```python
unit_tests.py
```

To plot the learning curves with and without pruning, run:
```python
plot.py
```

![alt_text](https://github.com/Albert-Z-Guo/ID3-Decision-Tree-Learning-Algorithm/blob/master/Learning%20Curves.png)
