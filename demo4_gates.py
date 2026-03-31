#!/usr/bin/env python3
import os
import json
from mgate_keeper import MGateKeeper

if not os.getenv('OPENAI_API_KEY'):
    print("ERROR: Set OPENAI_API_KEY")
    exit(1)

# Load project with gates
keeper = MGateKeeper(project_file="mgate_keeper/projects/photosynthesis.mg8")

print("\n" + "="*70)
print("DEMO 4: Multiple Quality Gates - Photosynthesis")
print("="*70)
print(f"\nModel: {keeper.llm_model}\n")

print(f"🔐 GATES LOADED ({len(keeper.gates)}):")
for gate in keeper.gates:
    print(f"   ✓ {gate.gate_id}: {gate.gate_name}")

question = "What is photosynthesis? Explain simply."
response = keeper.query(user_prompt=question, gates=keeper.gates)

print(f"\n{'='*70}")
print("ANSWER")
print("="*70)
answer = response.choices[0].message.content
print(f"\n{answer}\n")

print("="*70)
print("RESPONSE METRICS")
print("="*70)
print(f"Response ID: {response.id}")
print(f"Tokens Used: {response.usage.total_tokens}")
print("="*70 + "\n")
