import random
from pydantic import BaseModel, root_validator
from typing import List, Optional, Tuple
from pathforger import ChordIntervalStructures, ChordSymbolStructures, Progression, GraphNames

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


class PathData(BaseModel):
    nodes: List[Tuple[str, str]]
    graph_name: str

    def __str__(self):
        return f"{self.graph_name}:{self.nodes}"


class ProgressionRequest(BaseModel):
    graph: GraphNames

    class Config:
        use_enum_values = True

    @root_validator(pre=True)
    def graph_validator(cls, values):
        if values.get("graph") is None:
            values["graph"] = random.choice(list(GraphNames)[:2]).value
        return values


def construct_path_data(progression: Progression) -> PathData:
    graph = progression.graph
    node_names = [node.node_id for node in progression.nodes]
    structure_names = [
        ChordSymbolStructures[ChordIntervalStructures(structure).name].value # type: ignore Uses enum values
        for structure in progression.structures
        ] 
    nodes = list(zip(node_names, structure_names))
    return PathData(nodes=nodes, graph_name=graph)  # type: ignore Uses enum values
