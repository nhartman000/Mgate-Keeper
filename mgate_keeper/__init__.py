import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class MGateKeeper:
    def __init__(self, llm_model='gpt-4-turbo', seed=None, determinism_level=None):
        self.llm_model = llm_model
        self.seed = seed if seed is not None else 42
        self.determinism_level = determinism_level
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def query(self, user_prompt, gates=None, context=None):
        gates = gates or []
        
        # Make API call with seed
        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": user_prompt}],
            seed=self.seed
        )
        
        # Return the actual OpenAI response object
        return response
    
    def save_audit_log(self, response, filename):
        audit_data = {
            'response_id': response.id,
            'model': response.model,
            'content': response.choices[0].message.content,
            'tokens_used': response.usage.total_tokens
        }
        with open(filename, 'w') as f:
            json.dump(audit_data, f, indent=2)
    
    def load_audit_log(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

class G8sonGate:
    def __init__(self, gate_id, gate_name, atomic_requirements=None):
        self.gate_id = gate_id
        self.gate_name = gate_name
        self.atomic_requirements = atomic_requirements or []

class GstContext:
    def __init__(self, interpretation_posture, primary_modality):
        self.interpretation_posture = interpretation_posture
        self.primary_modality = primary_modality

__all__ = ['MGateKeeper', 'G8sonGate', 'GstContext']