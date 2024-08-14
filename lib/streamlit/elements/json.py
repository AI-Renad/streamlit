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

from __future__ import annotations

import json
import types
from collections import ChainMap, UserDict
from typing import TYPE_CHECKING, Any, cast

from streamlit.proto.Json_pb2 import Json as JsonProto
from streamlit.runtime.metrics_util import gather_metrics
from streamlit.type_util import is_custom_dict, is_namedtuple

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator


def _ensure_serialization(o: object) -> str | list[Any]:
    """A repr function for json.dumps default arg, which tries to serialize sets
    as lists."""
    return list(o) if isinstance(o, set) else repr(o)


class JsonMixin:
    @gather_metrics("json")
    def json(
        self,
        body: object,
        *,  # keyword-only arguments:
        expanded: bool | int = True,
    ) -> DeltaGenerator:
        """Display object or string as a pretty-printed JSON string.

        Parameters
        ----------

        body : object or str
            The object to print as JSON. All referenced objects should be
            serializable to JSON as well. If object is a string, we assume it
            contains serialized JSON.

        expanded : bool or int
            Controls the initial expansion state of the json element.
            If bool, ``True`` expands all levels, ``False`` collapses all levels.
            If int, specifies the depth to which the json should be expanded,
            collapsing deeper levels. Defaults to ``True``.

        Example
        -------
        >>> import streamlit as st
        >>>
        >>> st.json(
        ...     {
        ...         "foo": "bar",
        ...         "stuff": [
        ...             "stuff 1",
        ...             "stuff 2",
        ...             "stuff 3",
        ...         ],
        ...         "level1": {"level2": {"level3": {"a": "b"}}},
        ...     },
        ...     expanded=2,
        ... )

        .. output::
           https://doc-json.streamlit.app/
           height: 385px

        """
        import streamlit as st

        if is_custom_dict(body):
            body = body.to_dict()

        if is_namedtuple(body):
            body = body._asdict()

        if isinstance(body, (map, enumerate)):
            body = list(body)

        if isinstance(body, (ChainMap, types.MappingProxyType, UserDict)):
            body = dict(body)

        if not isinstance(body, str):
            try:
                # Serialize body to string and try to interpret sets as lists
                body = json.dumps(body, default=_ensure_serialization)
            except TypeError as err:
                st.warning(
                    "Warning: this data structure was not fully serializable as "
                    f"JSON due to one or more unexpected keys.  (Error was: {err})"
                )
                body = json.dumps(body, skipkeys=True, default=_ensure_serialization)

        json_proto = JsonProto()
        json_proto.body = body

        if isinstance(expanded, bool):
            json_proto.expanded = expanded
        elif isinstance(expanded, int):
            json_proto.expanded = True
            json_proto.max_expand_depth = expanded
        else:
            raise TypeError(
                f"The type {str(type(expanded))} of `expanded` is not supported"
                ", must be bool or int."
            )

        return self.dg._enqueue("json", json_proto)

    @property
    def dg(self) -> DeltaGenerator:
        """Get our DeltaGenerator."""
        return cast("DeltaGenerator", self)
