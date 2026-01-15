
import garak.generators.base
from vertexai.preview.generative_models import GenerativeModel


class VertexAIGenerator(garak.generators.base.Generator):
    """Wrapper for Vertex AI Gemini models."""
    def __init__(self, name="gemini-1.5-flash", generations=1):
        super().__init__(name)
        self.generations = generations
        self.name = name
        # Assume valid auth via ADC (which we set up via gcloud auth earlier)
        # In CI/CD this relies on OIDC.
        try:
             # Just init to check connectivity
             pass
        except Exception as e:
             print(f"Warning: Failed to init Vertex AI: {e}")

    def _generate(self, prompt):
        try:
            model = GenerativeModel(self.name)
            response = model.generate_content(prompt)
            return [response.text]
        except Exception as e:
            return [f"Error: {e}"]

# To run: garak --model_type custom --model_name garak_probe.VertexAIGenerator
