from __future__ import absolute_import, division, print_function

import os

import pandas as pd
import pytest
import sqlalchemy
from pandas.util.testing import assert_frame_equal
from tests.queries import query3, query6, query10

CUBE = 'sales_sqlite'


@pytest.mark.skipif("'DB_TEST' not in os.environ or os.environ['DB_TEST'] != 'SQLITE' or 'SQLITE_URI' not in os.environ")
@pytest.fixture(scope='function')
def connect():
    """Returns a connection and a metadata object"""
    if 'SQLITE_URI' in os.environ:
        return sqlalchemy.create_engine(os.environ['SQLITE_URI'])


@pytest.mark.skipif("'DB_TEST' not in os.environ or os.environ['DB_TEST'] != 'SQLITE' or 'SQLITE_URI' not in os.environ")
@pytest.fixture(scope='module')
def executor():
    from olapy.core.mdx.executor.execute import MdxEngine
    MdxEngine.source_type = ('csv', 'db')
    return MdxEngine(CUBE)


@pytest.mark.skipif("'DB_TEST' not in os.environ or os.environ['DB_TEST'] != 'SQLITE' or 'SQLITE_URI' not in os.environ")
def test_execution_query1(executor):
    df = executor.execute_mdx(query3)['result']
    test_df = pd.DataFrame({
        'Country': ['France', 'Spain', 'Switzerland', 'United States'],
        'Amount': [4, 3, 248, 768],
    }).groupby(['Country']).sum()
    assert assert_frame_equal(df, test_df) is None


@pytest.mark.skipif("'DB_TEST' not in os.environ or os.environ['DB_TEST'] != 'SQLITE' or 'SQLITE_URI' not in os.environ")
def test_execution_query2(executor):
    df = executor.execute_mdx(query6)['result']
    test_df = pd.DataFrame({
        'Year': [
            2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010,
            2010, 2010
        ],
        'Quarter': [
            -1, 'Q2 2010', 'Q2 2010', 'Q2 2010', 'Q2 2010', 'Q2 2010',
            'Q2 2010', 'Q2 2010', 'Q2 2010', 'Q2 2010', 'Q2 2010', 'Q2 2010',
            'Q2 2010'
        ],
        'Month': [
            -1, -1, 'May 2010', 'May 2010', 'May 2010', 'May 2010', 'May 2010',
            'May 2010', 'May 2010', 'May 2010', 'May 2010', 'May 2010',
            'May 2010'
        ],
        'Day': [
            -1, -1, -1, 'May 12,2010', 'May 13,2010', 'May 14,2010',
            'May 15,2010', 'May 16,2010', 'May 17,2010', 'May 18,2010',
            'May 19,2010', 'May 20,2010', 'May 21,2010'
        ],
        'Amount': [1023, 1023, 1023, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    }).groupby(['Year', 'Quarter', 'Month', 'Day']).sum()

    assert assert_frame_equal(df, test_df) is None


@pytest.mark.skipif("'DB_TEST' not in os.environ or os.environ['DB_TEST'] != 'SQLITE' or 'SQLITE_URI' not in os.environ")
def test_execution_query10(executor):
    df = executor.execute_mdx(query10)['result']
    test_df = pd.DataFrame({
        'Year': [2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010],
        'Quarter': [
            'Q2 2010', 'Q2 2010', 'Q2 2010', 'Q2 2010', 'Q2 2010', 'Q2 2010',
            'Q2 2010', 'Q2 2010'
        ],
        'Month': [
            'May 2010', 'May 2010', 'May 2010', 'May 2010', 'May 2010',
            'May 2010', 'May 2010', 'May 2010'
        ],
        'Day': [
            'May 19,2010',
            'May 17,2010',
            'May 15,2010',
            'May 13,2010',
            'May 12,2010',
            'May 14,2010',
            'May 16,2010',
            'May 18,2010',
        ],
        'Continent': [
            'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe',
            'Europe', 'Europe'
        ],
        'Count': [13, 65, 231, 841, 84, 2, 4, 64]
    }).groupby(
        ['Year', 'Quarter', 'Month', 'Day', 'Continent'], sort=False).sum()

    assert assert_frame_equal(df, test_df) is None
