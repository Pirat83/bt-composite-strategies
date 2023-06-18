from datetime import date
from typing import Union

import bt
from pandas import DataFrame


class BTInterpreter:
    root: dict

    start: date
    end: date
    rebalance: bt.algos.RunPeriod
    prices: DataFrame = None

    def __init__(self, root: dict, start: date, end: date):
        self.root = root

        self.start = start
        self.end = end

    def traverse(self, node: dict = None) -> bt.Strategy:
        if node is None:
            node = self.root
        node_type: str = node.get('node-type')
        match node_type:
            case 'group':
                return self.parse_group(node)
            case 'asset':
                return self.parse_asset(node)
            case _:
                raise NotImplementedError()

    def parse_group(self, node: dict) -> bt.Strategy:
        identifier: str = node.get('id')

        children: list = node.get('children')
        children: list[bt.Strategy] = [self.traverse(c) for c in children]

        result: bt.Strategy = self.build_strategy(identifier, children, debug=True)
        return result

    def parse_asset(self, node: dict) -> bt.Strategy:
        identifier: str = node.get('id')

        ticker: str = node.get('ticker')
        prices: DataFrame = bt.data.get(ticker, clean_tickers=False, start=self.start, end=self.end)
        if self.prices is None:
            self.prices = prices
        else:
            self.prices = self.prices.join(prices)

        result: bt.Strategy = self.build_strategy(identifier, [ticker], debug=True)
        return result

    def build_strategy(self, name: str,
                       children: Union[list[str], list[bt.core.Node]],
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
            algos.append(bt.algos.PrintTempData("Selected: {selected}"))
            algos.append(bt.algos.PrintTempData("Weights: \n{weights}"))

        algos.append(bt.algos.Rebalance())
        result: bt.Strategy = bt.Strategy(name, algos, children)
        return result

    def build_backtest(self, strategy: bt.Strategy) -> bt.Backtest:
        return bt.Backtest(strategy, self.prices, integer_positions=False)
