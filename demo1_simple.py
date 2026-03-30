#!/usr/bin/env python3
import os
from mgate_keeper import MGateKeeper, G8sonGate, GstContext

model = os.getenv('MGATE_MODEL', 'gpt-4-turbo')
if not os.getenv('OPENAI_API_KEY') and not os.getenv('GOOGLE_API_KEY'):
    print("ERROR: Set OPENAI_API_KEY or GOOGLE_API_KEY")
    exit(1)

keeper = MGateKeeper(llm_model=model)
gate = G8sonGate(gate_id="G1", gate_name="Simple", atomic_requirements=[
    {"req_id": "R1", "requirement": "Answer clearly", "threshold_efficiency": 0.75}
])
context = GstContext(interpretation_posture="Simple", primary_modality="👁️")

response = keeper.query(
    user_prompt="What is photosynthesis? Explain simply.",
    gates=[gate],
    context=context
)

print("\n" + "="*70)
print("DEMO 1: Simple Question")
print("="*70)
print(f"\nModel: {model}\n")
print(f"Answer:\n{response.content}\n")
print(f"Gate Passed: {response.gates_passed}")
print(f"Confidence: {response.overall_confidence * 100:.1f}%")
print("="*70 + "\n")