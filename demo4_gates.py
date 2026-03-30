#!/usr/bin/env python3
import os
from mgate_keeper import MGateKeeper, G8sonGate, GstContext

model = os.getenv('MGATE_MODEL', 'gpt-4-turbo')
if not os.getenv('OPENAI_API_KEY') and not os.getenv('GOOGLE_API_KEY'):
    print("ERROR: Set OPENAI_API_KEY or GOOGLE_API_KEY")
    exit(1)

keeper = MGateKeeper(llm_model=model)

gates = [
    G8sonGate(gate_id="G_U", gate_name="Understanding",
        atomic_requirements=[{"req_id": "R1", "mmol_vector": "👁️", "requirement": "Understand", "threshold_efficiency": 0.75}]),
    G8sonGate(gate_id="G_R", gate_name="Research",
        atomic_requirements=[{"req_id": "R1", "mmol_vector": "🧠💭", "requirement": "Research", "threshold_efficiency": 0.80}]),
    G8sonGate(gate_id="G_V", gate_name="Verify",
        atomic_requirements=[{"req_id": "R1", "mmol_vector": "📌", "requirement": "Verify", "threshold_efficiency": 0.85}])
]

print("\n" + "="*70)
print("DEMO 4: Multiple Quality Gates")
print("="*70)
print(f"\nModel: {model}\n")

response = keeper.query(user_prompt="What are benefits of exercise?", gates=gates)

print("GATE RESULTS:\n")
for gate in response.g8son_gates_applied:
    status = "✅ PASS" if gate['gate_passed'] else "❌ FAIL"
    print(f"{status} - {gate['gate_name']}: {gate['overall_confidence'] * 100:.1f}%")

print(f"\nANSWER:\n{response.content}")
print(f"\nOverall: {response.overall_confidence * 100:.1f}%")
print("="*70 + "\n")