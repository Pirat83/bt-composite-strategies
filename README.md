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
We create a combined strategy containing two buy and hold strategies of QQQ and SPY
* The strategy does not have a return, but some other statistics. 
* It has sold everything on the 4th day and rebalancing is not propagated to the children. 

# Second level composite strategy
We create a combined strategy containing to combined strategies and one asset. 
* The execution fails with 
```shell
ZeroDivisionError: Could not update df876984-3be8-40c9-8847-e3b3c6af3cdc on 2023-05-17 00:00:00. Last value was 0.0 and net flows were 0. Currentvalue is 1000000.0. Therefore, we are dividing by zero to obtain the return for the period.
```

# How to get this working?

```shell
git clone https://github.com/Pirat83/bt-composite-strategies.git
cd bt-composite-strategies/
conda create --name bt-composite-strategies
conda env update
```

If you can contribute to the solution I would appreciate it very much.  