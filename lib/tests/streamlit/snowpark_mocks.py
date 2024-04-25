# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import pandas as pd


class DataFrame:
    """This is dummy DataFrame class,
    which imitates snowflake.snowpark.dataframe.DataFrame class
    for testing purposes."""

    __module__ = "snowflake.snowpark.dataframe"

    def __init__(self, data: pd.DataFrame):
        self._data: pd.DataFrame = data

    def to_pandas(self) -> pd.DataFrame:
        return self._data

    def limit(self, n: int) -> "DataFrame":
        """Returns the top n element of a mock version of snowflake.snowpark.dataframe.DataFrame"""
        return DataFrame(self._data.head(n))


class Table:
    """This is dummy Table class,
    which imitates snowflake.snowpark.dataframe.DataFrame class
    for testing purposes."""

    __module__ = "snowflake.snowpark.table"

    def __init__(self, data: pd.Series):
        self._data: pd.Series = data

    def to_pandas(self) -> pd.DataFrame:
        return self._data

    def limit(self, n: int) -> "Table":
        """Returns the top n element of a mock version of snowflake.snowpark.table.Table"""
        return Table(self._data.head(n))


class Row:
    """This is dummy Row class,
    which imitates snowflake.snowpark.row.Row class
    for testing purposes."""

    __module__ = "snowflake.snowpark.row"
