import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class MGateKeeper:
    def __init__(self, llm_model='gpt-3.5-turbo', seed=None, determinism_level=None, project_file=None):
        self.llm_model = llm_model
        self.seed = seed if seed is not None else 42
        self.determinism_level = determinism_level
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.project = None
        self.gates = []
        self.context = None
        
        if project_file:
            self.load_project(project_file)
    
    def load_project(self, project_file):
        """Load project configuration from .mg8 file"""
        with open(project_file, 'r') as f:
            self.project = json.load(f)
        
        self.llm_model = self.project.get('model', self.llm_model)
        self.seed = self.project.get('seed', self.seed)
        
        # Load gates
        for gate_path in self.project.get('g8son_gates', []):
            with open(gate_path, 'r') as f:
                gate_data = json.load(f)
                self.gates.append(G8sonGate(
                    gate_id=gate_data['gate_id'],
                    gate_name=gate_data['gate_name'],
                    atomic_requirements=gate_data.get('atomic_requirements', [])
                ))
        
        # Load context
        context_path = self.project.get('gst_context')
        if context_path:
            with open(context_path, 'r') as f:
                ctx_data = json.load(f)
                self.context = GstContext(
                    context_id=ctx_data.get('context_id'),
                    interpretation_posture=ctx_data['interpretation_posture'],
                    primary_modality=ctx_data['primary_modality']
                )
    
    def query(self, user_prompt, gates=None, context=None):
        """Execute query with gates and context"""
        gates = gates or self.gates or []
        context = context or self.context
        
        # Make API call with seed for determinism
        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": user_prompt}],
            seed=self.seed
        )
        
        return response
    
    def save_audit_log(self, audit_data, filename):
        """Save audit log to .qson file"""
        with open(filename, 'w') as f:
            json.dump(audit_data, f, indent=2)
    
    def load_audit_log(self, filename):
        """Load audit log from .qson file"""
        with open(filename, 'r') as f:
            return json.load(f)

class G8sonGate:
    """Represents a gate with atomic requirements"""
    def __init__(self, gate_id, gate_name, atomic_requirements=None):
        self.gate_id = gate_id
        self.gate_name = gate_name
        self.atomic_requirements = atomic_requirements or []

class GstContext:
    """Represents a gestalt context for interpretation"""
    def __init__(self, context_id=None, interpretation_posture=None, primary_modality=None):
        self.context_id = context_id
        self.interpretation_posture = interpretation_posture
        self.primary_modality = primary_modality

__all__ = ['MGateKeeper', 'G8sonGate', 'GstContext']