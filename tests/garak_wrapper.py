from tests.garak_probe import VertexAIGenerator

_gen = None

def generate_response(prompt: str, **kwargs):
    global _gen
    if _gen is None:
        _gen = VertexAIGenerator(generations=1)
    return _gen._generate(prompt)
