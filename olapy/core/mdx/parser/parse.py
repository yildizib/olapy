# -*- encoding: utf8 -*-

"""
This module Parse Mdx Query, And Break it in parts
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import re


class Parser(object):
    """
    Class for Parsing MdxQuery
    """
    # french characters
    # or use new regex 2017.02.08
    regex = "(\[[\w+\d ]+\](\.\[[\w+\d\.\,\s\_\-\:\é\ù\è\ù\û\ü\ÿ\€\’\à\â\æ\ç\é\è\ê\ë\ï\î" \
            "\ô\œ\Ù\Û\Ü\Ÿ\À\Â\Æ\Ç\É\È\Ê\Ë\Ï\Î\Ô\Œ\& ]+\])*\.?((Members)|(\[Q\d\]))?)"

    def __init__(self, mdx_query=None):
        self.mdx_query = mdx_query

    @staticmethod
    def split_tuple(tupl):
        """
        Split Tuple (String) into items.

        example::

             input : '[Geography].[Geography].[Continent].[Europe]'

             output : ['Geography','Geography','Continent','Europe']

        :param tupl: MDX Tuple as String
        :return: Tuple items in list
        """
        splitted_tupl = tupl.strip(' \t\n').split('].[')
        splitted_tupl[0] = splitted_tupl[0].replace('[', '')
        splitted_tupl[-1] = splitted_tupl[-1].replace(']', '')
        return splitted_tupl

    @classmethod
    def get_tuples(cls, query, start=None, stop=None):
        """Get all tuples in the mdx query.

        Example::


            SELECT  {
                        [Geography].[Geography].[All Continent].Members,
                        [Geography].[Geography].[Continent].[Europe]
                    } ON COLUMNS,

                    {
                        [Product].[Product].[Company]
                    } ON ROWS

                    FROM {sales}

        It returns ::

            [
                ['Geography','Geography','Continent'],
                ['Geography','Geography','Continent','Europe'],
                ['Product','Product','Company']
            ]


        :param query: mdx query
        :param start: keyword in the query where we start (examples start = SELECT)
        :param stop:  keyword in the query where we stop (examples start = ON ROWS)

        :return:  nested list of tuples (see the example)
        """

        if start is not None:
            start = query.index(start)
        if stop is not None:
            stop = query.index(stop)

        # clean the query (remove All, Members...)
        return [
            [
                tup_att.replace('All ', '').replace('[', "").replace("]", "")
                for tup_att in tup[0].replace('.Members', '').replace('.MEMBERS', '', ).split('].[') if tup_att
            ]
            for tup in re.compile(cls.regex).findall(
                query[start:stop], )
            if len(tup[0].split('].[')) > 1
            # for tup in re.compile(MdxEngine.regex).findall(
            #     query.encode("utf-8", 'replace')[start:stop],)
            # if len(tup[0].split('].[')) > 1
        ]

    def decorticate_query(self, query):
        """Get all tuples that exists in the MDX Query by axes.

        Example::

            query : SELECT  {
                                [Geography].[Geography].[All Continent].Members,
                                [Geography].[Geography].[Continent].[Europe]
                            } ON COLUMNS,

                            {
                                [Product].[Product].[Company]
                            } ON ROWS

                            FROM {sales}

            output : {
                    'all': [   ['Geography', 'Geography', 'Continent'],
                               ['Geography', 'Geography', 'Continent', 'Europe'],
                               ['Product', 'Product', 'Company']],

                    'columns': [['Geography', 'Geography', 'Continent'],
                                ['Geography', 'Geography', 'Continent', 'Europe']],

                    'rows': [['Product', 'Product', 'Company']],
                    'where': []
                    }

        :param query: MDX Query
        :return: dict of axis as key and tuples as value
        """

        # Hierarchize -> ON COLUMNS , ON ROWS ...
        # without Hierarchize -> ON 0

        tuples_on_mdx_query = self.get_tuples(query)
        on_rows = []
        on_columns = []
        on_where = []

        try:
            # ON ROWS
            if 'ON ROWS' in query:
                stop = 'ON ROWS'
                if 'ON COLUMNS' in query:
                    start = 'ON COLUMNS'
                else:
                    start = 'SELECT'
                on_rows = self.get_tuples(query, start, stop)

            # ON COLUMNS
            if 'ON COLUMNS' in query:
                start = 'SELECT'
                stop = 'ON COLUMNS'
                on_columns = self.get_tuples(query, start, stop)

            # ON COLUMNS (AS 0)
            if 'ON 0' in query:
                start = 'SELECT'
                stop = 'ON 0'
                on_columns = self.get_tuples(query, start, stop)

            # WHERE
            if 'WHERE' in query:
                start = 'FROM'
                on_where = self.get_tuples(query, start)

        except BaseException:
            raise SyntaxError('Please check your MDX Query')

        return {
            'all': tuples_on_mdx_query,
            'columns': on_columns,
            'rows': on_rows,
            'where': on_where,
        }

    @staticmethod
    def add_tuple_brackets(tupl):
        """
        After splitting tuple with :func:`splitted_group`, you got some tuple like **aa].[bb].[cc].[dd**
        so add_tuple_brackets fix this by adding missed brackets **[aa].[bb].[cc].[dd]**.

        :param tupl: Tuple as string example  'aa].[bb].[cc].[dd'.
        :return: [aa].[bb].[cc].[dd] as string.
        """
        tupl = tupl.strip()
        if tupl[0] != '[':
            tupl = '[' + tupl
        if tupl[-1] != ']':
            tupl = tupl + ']'
        return tupl

    def split_group(self, group):
        """
        Split group of tuples.
        example::

            group : '[Geo].[Geo].[Continent],[Prod].[Prod].[Name],[Time].[Time].[Day]'

            out : ['[Geo].[Geo].[Continent]','[Prod].[Prod].[Name]','[Time].[Time].[Day]']

        :param group: Group of tuple as string.
        :return: Separated tuples as list.
        """
        splitted_group = group.replace('\n', '').replace('\t', '').split('],')
        return list(map(lambda tupl: self.add_tuple_brackets(tupl), splitted_group))

    def get_nested_select(self):
        """
        Get tuples groups in query like ::

                Select {
                    ([Time].[Time].[Day].[2010].[Q2 2010].[May 2010].[May 19,2010],
                    [Geography].[Geography].[Continent].[Europe],
                    [Measures].[Amount]),

                    ([Time].[Time].[Day].[2010].[Q2 2010].[May 2010].[May 17,2010],
                    [Geography].[Geography].[Continent].[Europe],
                    [Measures].[Amount])
                    }

                out :
                    ['[Time].[Time].[Day].[2010].[Q2 2010].[May 2010].[May 19,2010],\
                    [Geography].[Geography].[Continent].[Europe],[Measures].[Amount]',

                    '[Time].[Time].[Day].[2010].[Q2 2010].[May 2010].[May 17,2010],\
                    [Geography].[Geography].[Continent].[Europe],[Measures].[Amount]']

        :return: All groups as list of strings.

        """
        return re.findall(r'\(([^()]+)\)', self.mdx_query)

    def hierarchized_tuples(self):
        """Check if `hierarchized <https://docs.microsoft.com/en-us/sql/mdx/hierarchize-mdx>`_  mdx query.

        :return: True | False
        """
        return 'Hierarchize' in self.mdx_query