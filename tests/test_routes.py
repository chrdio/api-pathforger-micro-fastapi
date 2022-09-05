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
def test_generation_200(body, length):
    payload = body.json()
    response = TEST_APP.post(f'/generate/{str(length)}', payload)
    assert response.status_code == 200

@given(length=st.integers(min_value=2, max_value=4))
def test_generation_200_no_body(length):
    payload = "{}"
    response = TEST_APP.post(f'/generate/{str(length)}', payload)
    assert response.status_code == 200

def test_generation_422():
    payload = '{"graph": 4}'
    response = TEST_APP.post(f'/generate/{str(3)}', payload)
    assert response.status_code == 422

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
def test_amendment_200(index, graph):
    progression = getProgression(4, graph, NODES)
    payload = progression.json()
    response = TEST_APP.post(f'/amend/{str(index)}', payload)
    assert response.status_code == 200

@given(
    index=st.integers(
        min_value=4,
        ),
    graph=st.sampled_from(
        [
            GRAPH_DICT["major_graph"],
            GRAPH_DICT["minor_graph"],
            GRAPH_DICT["master_graph"],
        ]
        )
    )
def test_amendment_500(index, graph):
    progression = getProgression(4, graph, NODES)
    payload = progression.json()
    response = TEST_APP.post(f'/amend/{str(index)}', payload)
    assert response.status_code == 500

@given(
    index=st.integers(
        min_value=0,
        max_value=3
        )
    )
def test_amendment_422(index):
    payload = '{"graph": "test_graph"}'
    response = TEST_APP.post(f'/amend/{str(index)}', payload)
    assert response.status_code == 422

def test_healthcheck():
    assert TEST_APP.get("/healthcheck").status_code == 200



def test_endpoint_builder():
    raw = """{"name": "microaccountant/music","host": "127.0.0.1","port": "8004","path": "ensure/music"}"""
    ep = Endpoint.parse_raw(raw)
    ep.option = "5"
    assert str(ep)