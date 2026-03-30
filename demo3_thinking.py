#!/usr/bin/env python3
import os
from mgate_keeper import MGateKeeper, G8sonGate, GstContext

model = os.getenv('MGATE_MODEL', 'gpt-4-turbo')
if not os.getenv('OPENAI_API_KEY') and not os.getenv('GOOGLE_API_KEY'):
    print("ERROR: Set OPENAI_API_KEY or GOOGLE_API_KEY")
    exit(1)

keeper = MGateKeeper(llm_model=model)
gate = G8sonGate(gate_id="G3", gate_name="Thinking", atomic_requirements=[
    {"req_id": "R1", "mmol_vector": "🧠💭", "requirement": "Show reasoning", "threshold_efficiency": 0.75}
])
context = GstContext(interpretation_posture="Detailed", primary_modality="🧠")

print("\n" + "="*70)
print("DEMO 3: Watch AI Think")
print("="*70)
print(f"\nModel: {model}\n")

response = keeper.query(
    user_prompt="Why do we have gravity? Explain step by step.",
    gates=[gate],
    context=context
)

print("="*70)
print("AI'S THINKING PROCESS")
print("="*70 + "\n")

for step in response.llm_reasoning_chain:
    print(f"Step {step['step']}: {step['mmol_vector']}")
    print(f"  Thought: {step['internal_thought']}")
    print(f"  Confidence: {step['confidence'] * 100:.1f}%\n")

print("="*70)
print("FINAL ANSWER")
print("="*70)
print(f"\n{response.content}\n")
print(f"Overall Confidence: {response.overall_confidence * 100:.1f}%")
print("="*70 + "\n")