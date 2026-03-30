#!/usr/bin/env python3
import os
from mgate_keeper import MGateKeeper, G8sonGate, GstContext

model = os.getenv('MGATE_MODEL', 'gpt-4-turbo')
if not os.getenv('OPENAI_API_KEY') and not os.getenv('GOOGLE_API_KEY'):
    print("ERROR: Set OPENAI_API_KEY or GOOGLE_API_KEY")
    exit(1)

keeper = MGateKeeper(llm_model=model, determinism_level="strict", seed=42)
gate = G8sonGate(gate_id="G2", gate_name="Test", atomic_requirements=[
    {"req_id": "R1", "requirement": "Answer", "threshold_efficiency": 0.75}
])
context = GstContext(interpretation_posture="Factual", primary_modality="👁️")

print("\n" + "="*70)
print("DEMO 2: Reproducible (Ask Twice, Get Same Answer)")
print("="*70)
print(f"\nModel: {model}\n")

print("Query 1: 'What is the capital of France?'\n")
response1 = keeper.query(user_prompt="What is the capital of France?", gates=[gate])
print(f"Answer 1: {response1.content}")
print(f"Hash: {response1.audit_trail['full_chain_hash'][:16]}...\n")

print("Query 2: 'What is the capital of France?' (same)\n")
response2 = keeper.query(user_prompt="What is the capital of France?", gates=[gate])
print(f"Answer 2: {response2.content}")
print(f"Hash: {response2.audit_trail['full_chain_hash'][:16]}...\n")

print("="*70)
if response1.content == response2.content:
    print("✅ IDENTICAL!")
else:
    print("❌ Different")
print("="*70 + "\n")