from datetime import date
from typing import Union

import bt
import pandas as pd
from pandas import DataFrame, Series


def flatten(i, result=None) -> list[bt.Backtest]:
    if result is None:
        result = []
    if isinstance(i, bt.Backtest):
        result.append(i)
    elif isinstance(i, bt.backtest.Result):
        for b in i.backtest_list:
            flatten(b, result)
    elif isinstance(i, list):
        for b in i:
            flatten(b, result)
    elif isinstance(i, tuple):
        for b in i:
            flatten(b, result)
    else:
        raise NotImplementedError()

    return result


class BTInterpreter:
    root: dict

    start: date
    end: date
    rebalance: bt.algos.RunPeriod

    def __init__(self, root: dict, start: date, end: date):
        self.root = root

        self.start = start
        self.end = end

    def traverse(self, node: dict = None) -> bt.backtest.Result:
        if node is None:
            node = self.root
        node_type: str = node.get('node-type')
        match node_type:
            case 'group':
                return self.parse_group(node)
            case 'group':
                return self.parse_group(node)
            case 'asset':
                return self.parse_asset(node)
            case _:
                raise NotImplementedError()

    def parse_group(self, node: dict) -> bt.backtest.Result:
        identifier: str = node.get('id')

        children: list = node.get('children')
        children: list[bt.backtest.Result] = [self.traverse(c) for c in children]

        prices: DataFrame = pd.DataFrame()
        for p in [c.prices for c in children]:
            prices = bt.merge(p)

        backtests: list[bt.Backtest] = flatten([c.backtest_list for c in children])
        #for p in [b.data for b in backtests]:
        #    prices = bt.merge(prices, p)

        strategies: list[bt.Strategy] = [b.strategy for b in backtests]
        #for p in [s.universe for s in strategies]:
        #    prices = bt.merge(prices, p)

        strategy: bt.Strategy = self.build_strategy(identifier, strategies, debug=True)
        backtest: bt.Backtest = self.build_backtest(strategy, prices)
        result: bt.backtest.Result = bt.run(backtest)
        return result

    def parse_asset(self, node: dict) -> bt.backtest.Result:
        identifier: str = node.get('id')

        ticker: str = node.get('ticker')
        prices: DataFrame = bt.data.get(ticker, clean_tickers=False, start=self.start, end=self.end)
        strategy: bt.Strategy = self.build_strategy(identifier, [bt.Security(ticker)])
        backtest: bt.Backtest = self.build_backtest(strategy, prices)
        result: bt.backtest.Result = bt.run(backtest)
        return result

    def build_strategy(self, name: str,
                       children: Union[list[bt.algos.SecurityBase], list[bt.core.StrategyBase]],
                       selection: bt.algos.Algo = bt.algos.SelectAll(),
                       weight: bt.algos.Algo = bt.algos.WeighInvVol(),
                       debug: bool = False
                       ) -> bt.Strategy:
        algos: [list[bt.algos.Algo]] = [
            bt.algos.RunAfterDate(self.start),
            bt.algos.RunDaily(),
            selection,
            weight
        ]
        if debug:
            algos.append(bt.algos.PrintInfo('\n{now}: {name} -> Value:{_value:0.0f}, Price:{_price:0.4f}'))
            algos.append(bt.algos.PrintTempData('Weights: \n{weights}'))

        algos.append(bt.algos.Rebalance())
        result: bt.Strategy = bt.Strategy(name, algos, children)
        return result

    @staticmethod
    def build_backtest(strategy: bt.Strategy, prices: Union[Series, DataFrame]) -> bt.Backtest:
        return bt.Backtest(strategy, prices, integer_positions=False)


def main():
    print("Hello World!")


if __name__ == "__main__":
    main()
