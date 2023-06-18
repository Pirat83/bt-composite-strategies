# BT composite strategies

This repository shows the effect of the issue https://github.com/pmorissette/bt/issues/415. 
For more details see the `test_interpreter.py` unit test or use the Jupyter notebook `example.ipynb`


# Simple buy and hold strategy:

We create a simple buy and hold strategy with the QQQ. 
* Everything is fine. 
* We have transactions. 
* The backtest works fine. 
* The portfolio gets rebalanced every day. 

# First level composite strategy
* Everything is fine. 
* We have transactions. 
* The backtest works fine. 
* The portfolio gets rebalanced every day. 

# Second level composite strategy
We create a combined strategy containing to combined strategies and one asset. 
* The execution fails with 
```shell
E   AttributeError: 'Strategy' object has no attribute '_values'

bt/core.py:763: AttributeError
```

# How to get this working?

```shell
git clone https://github.com/Pirat83/bt-composite-strategies.git
cd bt-composite-strategies/
conda create --name bt-composite-strategies
conda env update
```

If you can contribute to the solution I would appreciate it very much.  