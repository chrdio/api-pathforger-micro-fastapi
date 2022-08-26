from pydantic import BaseModel
from typing import Optional
from chrdiotypes.data_enums import ChordSymbolStructures
from chrdiotypes.transport import PathTransport
from pathforger import Progression

class Endpoint(BaseModel):
    name: str
    host: str
    port: str
    path: str
    option: Optional[str] = None
    prefix: str = 'http://'

    def __str__(self):
        if self.option is not None:
            option = '/' + self.option
        else:
            option = ''
        return f"{self.prefix}{self.host}:{self.port}/{self.path}{option}"


def construct_path_transport(progression: Progression) -> PathTransport:
    graph = progression.graph
    node_names = [node.node_id for node in progression.nodes]
    structure_names = [
        ChordSymbolStructures[structure.name]
        for structure in progression.structures
        ] 
    nodes = list(zip(node_names, structure_names))
    return PathTransport(nodes=nodes, graph_name=graph)
