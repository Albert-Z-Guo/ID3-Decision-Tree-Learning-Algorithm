# ID3 Decision Tree Learning Algorithm

This repository contains the implementation of a variant of ID3 (Iterative Dichotomiser 3) Decision Tree Learning Algorithm with recursive PostOrder error-reduced pruning from gound up.

Note that this algorithm supports learning from examples with missing attributes.

`parse.py` takes a filename and returns attribute information and all the data in array of dictionaries.

`node.py` defines the node class with fields.

`ID3.py` contains the main implementation of the algorithm, which is modularized for better readability.

`house_votes_84.data` is the example data (policy votes) used for classification (political parties).

To test all functions, run:
```python
python3 unit_tests.py
```

To plot the learning curves with and without pruning, run:
```python
python3 plot.py
```

![alt_text](https://github.com/Albert-Z-Guo/ID3-Decision-Tree-Learning-Algorithm/blob/master/Learning%20Curves.png)
