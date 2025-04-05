from typing import Optional, List, Dict
from dataclasses import dataclass

@dataclass
class NodeConfig:
    path: Optional[str] = None
    defaultValue: Optional[str] = None
    store_messages: Optional[str] = None
    x_coordinate: Optional[int] = None
    y_coordinate: Optional[int] = None
    Text: Optional[str] = None
    sessionID: Optional[str] = None
    files: Optional[str] = None
    filepath: Optional[str] = None
    fileText: Optional[str] = None
    fileBase64: Optional[str] = None
    fileType: Optional[str] = None
    modelName: Optional[str] = None
    temperature: Optional[float] = None
    input: Optional[str] = None
    system_message: Optional[str] = None
    maximum_tokens: Optional[str] = None
    API_key: Optional[str] = None

@dataclass
class Node:
    type: str
    id: str
    config: NodeConfig
    inputs: List[str]
    outputs: List[str]

    def prettify(self) -> Dict:
        return {
            "type": self.type,
            "id": self.id,
            "config": self.config.__dict__,
            "inputs": self.inputs,
            "outputs": self.outputs
        }
