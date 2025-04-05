from typing import Dict
from dataclasses import dataclass

@dataclass
class Connection:
    from_node: str
    from_output: str
    to_node: str
    to_input: str

    def prettify(self) -> Dict:
        return {
            "from": {
                "node": self.from_node,
                "output": self.from_output
            },
            "to": {
                "node": self.to_node,
                "input": self.to_input
            }
        }