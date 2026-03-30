#!/usr/bin/env python3
import os
import json
from mgate_keeper import MGateKeeper, G8sonGate, GstContext

model = os.getenv('MGATE_MODEL', 'gpt-4-turbo')
if not os.getenv('OPENAI_API_KEY'):
    print("ERROR: Set OPENAI_API_KEY")
    exit(1)

keeper = MGateKeeper(llm_model=model)
gate = G8sonGate(gate_id="G5", gate_name="Audit", atomic_requirements=[
    {"req_id": "R1", "requirement": "Complete", "threshold_efficiency": 0.75}
])

print("\n" + "="*70)
print("DEMO 5: Audit Trail")
print("="*70)
print(f"\nModel: {model}\n")

print("Asking: 'What is machine learning?'")
response = keeper.query(user_prompt="What is machine learning?", gates=[gate])

print("\n" + "="*70)
print("AUDIT TRAIL")
print("="*70)
print(f"\nResponse ID: {response.audit_trail['full_chain_hash']}")
print(f"Gates Applied: {response.audit_trail['gates_applied']}")
print(f"Model Used: {response.audit_trail['model']}")
print(f"Prompt Tokens: {response.audit_trail['prompt_tokens']}")
print(f"Completion Tokens: {response.audit_trail['completion_tokens']}")
print(f"Confidence: {response.overall_confidence * 100:.1f}%")
print(f"\nAnswer: {response.content[:150]}...")
print("\n✅ Complete audit trail captured!")
print("="*70 + "\n")