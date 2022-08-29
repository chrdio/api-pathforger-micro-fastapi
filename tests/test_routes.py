import pytest
from micropathforger import APP
from micropathforger.transport.schemas import Endpoint
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from chrdiotypes.musical import ProgressionRequest, ProgressionFields
from hypothesis import given, strategies as st, settings, HealthCheck
from pathforger import getProgression, TEST_GRAPH, NODES, GRAPH_DICT

# Ignore server exceptions, since there are calls to another server that
# simply cannot be fulfilled
TEST_APP = TestClient(APP, raise_server_exceptions=False)

@given(body=st.builds(ProgressionRequest), length=st.integers(min_value=2, max_value=4))
def test_generation(body, length):
    payload = body.json()
    response = TEST_APP.post(f'/generate/{str(length)}', payload)
    assert response.status_code == 200

@settings(suppress_health_check=[HealthCheck(9)])
@given(
    index=st.integers(
        min_value=0,
        max_value=3
        ),
    graph=st.sampled_from(
        [
            GRAPH_DICT["major_graph"],
            GRAPH_DICT["minor_graph"],
            GRAPH_DICT["master_graph"],
        ]
        )
    )
def test_amendment(index, graph):
    progression = getProgression(4, graph, NODES)
    payload = progression.json()
    response = TEST_APP.post(f'/amend/{str(index)}', payload)
    assert response.status_code == 200



def test_endpoint_builder():
    raw = """{"name": "microaccountant/music","host": "127.0.0.1","port": "8004","path": "ensure/music"}"""
    ep = Endpoint.parse_raw(raw)
    ep.option = "5"
    assert str(ep)