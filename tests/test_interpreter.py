import pprint
from datetime import date, timedelta

import bt.algos

from interpreter import BTInterpreter


def print_backtest_results(result: bt.backtest.Result):
    result.display()
    for k, v in result.items():
        pprint.pp(result.get_transactions(k))
        pprint.pp(result.get_weights(k))
        pprint.pp(result.get_security_weights(k))


def test_traverse_asset():
    node: dict = {
        'id': 'df876984-3be8-40c9-8847-e3b3c6af3cdc',
        'strategy-type': 'asset',
        'ticker': 'QQQ'
    }

    subject = BTInterpreter(node, date.today() - timedelta(weeks=4), date.today())
    asset: bt.core.Node = subject.traverse()
    strategy: bt.Strategy = subject.build_strategy(asset.name, [asset])
    backtest: bt.Backtest = subject.build_backtest(strategy)
    result: bt.backtest.Result = bt.run(backtest)
    print_backtest_results(result)


def test_traverse_first_level_asset():
    node: dict = {
        'id': '5fc986bf-d7c8-4582-bc27-f1ede76bdc29',
        'strategy-type': 'group',
        'children': [
            {
                'id': 'df876984-3be8-40c9-8847-e3b3c6af3cdc',
                'strategy-type': 'asset',
                'ticker': 'QQQ'
            },
            {
                'id': '742dc790-d0f7-472d-bd3e-405e411c0b2c',
                'strategy-type': 'asset',
                'ticker': 'SPY'
            }
        ]
    }

    subject = BTInterpreter(node, date.today() - timedelta(weeks=4), date.today())
    strategy: bt.core.Strategy = subject.traverse()
    backtest: bt.Backtest = subject.build_backtest(strategy)
    result: bt.backtest.Result = bt.run(backtest)
    print_backtest_results(result)


def test_traverse_second_level_asset():
    node: dict = {
        'id': 'c20d0968-2dfa-4ff7-8dfc-4c3d0df36dd4',
        'strategy-type': 'group',
        'children': [
            {
                'id': '5fc986bf-d7c8-4582-bc27-f1ede76bdc29 ',
                'strategy-type': 'group',
                'children': [
                    {
                        'id': 'df876984-3be8-40c9-8847-e3b3c6af3cdc',
                        'strategy-type': 'asset',
                        'ticker': 'QQQ'
                    },
                    {
                        'id': '742dc790-d0f7-472d-bd3e-405e411c0b2c ',
                        'strategy-type': 'asset',
                        'ticker': 'SPY'
                    }
                ]
            },
            {
                'id': 'e5286ea7-9591-4b43-896e-cf34fb63a0e0',
                'strategy-type': 'group',
                'children': [
                    {
                        'id': '9e4f255b-343a-43ee-a433-f2366f8e9e62',
                        'strategy-type': 'asset',
                        'ticker': 'IYY'
                    },
                    {
                        'id': '57033cdf-c185-4091-9d3e-3fc1e17913be',
                        'strategy-type': 'asset',
                        'ticker': 'IWM'
                    }
                ]
            },
            {
                'id': '07306351-709d-41d8-b8dd-d8f6e6ae2900',
                'strategy-type': 'asset',
                'ticker': 'IVV'
            }
        ]
    }

    subject = BTInterpreter(node, date.today() - timedelta(weeks=4), date.today())
    strategy: bt.core.Strategy = subject.traverse()
    backtest: bt.Backtest = subject.build_backtest(strategy)
    result: bt.backtest.Result = bt.run(backtest)
    print_backtest_results(result)


def test_traverse_third_level_asset():
    node: dict = {
        'id': 'ba3dcb45-dbe4-4f72-9eb6-598f2e893bca',
        'strategy-type': 'group',
        'children': [{
            'id': 'c20d0968-2dfa-4ff7-8dfc-4c3d0df36dd4',
            'strategy-type': 'group',
            'children': [
                {
                    'id': '5fc986bf-d7c8-4582-bc27-f1ede76bdc29 ',
                    'strategy-type': 'group',
                    'children': [
                        {
                            'id': 'df876984-3be8-40c9-8847-e3b3c6af3cdc',
                            'strategy-type': 'asset',
                            'ticker': 'QQQ'
                        },
                        {
                            'id': '742dc790-d0f7-472d-bd3e-405e411c0b2c ',
                            'strategy-type': 'asset',
                            'ticker': 'SPY'
                        }
                    ]
                },
                {
                    'id': 'e5286ea7-9591-4b43-896e-cf34fb63a0e0',
                    'strategy-type': 'group',
                    'children': [
                        {
                            'id': '9e4f255b-343a-43ee-a433-f2366f8e9e62',
                            'strategy-type': 'asset',
                            'ticker': 'IYY'
                        },
                        {
                            'id': '57033cdf-c185-4091-9d3e-3fc1e17913be',
                            'strategy-type': 'asset',
                            'ticker': 'IWM'
                        }
                    ]
                },
                {
                    'id': '07306351-709d-41d8-b8dd-d8f6e6ae2900',
                    'strategy-type': 'asset',
                    'ticker': 'IVV'
                }
            ]
        },
            {
                'id': 'fff6be49-6116-4ec0-a878-266d0b530e0b',
                'strategy-type': 'asset',
                'ticker': 'AMD'
            }
        ]}

    subject = BTInterpreter(node, date.today() - timedelta(weeks=4), date.today())
    strategy: bt.core.Strategy = subject.traverse()
    backtest: bt.Backtest = subject.build_backtest(strategy)
    result: bt.backtest.Result = bt.run(backtest)
    print_backtest_results(result)
