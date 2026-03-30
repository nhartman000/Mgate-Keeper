#!/usr/bin/env python3
import os
from mgate_keeper import MGateKeeper, G8sonGate, GstContext

model = os.getenv('MGATE_MODEL', 'gpt-4-turbo')
if not os.getenv('OPENAI_API_KEY') and not os.getenv('GOOGLE_API_KEY'):
    print("ERROR: Set OPENAI_API_KEY or GOOGLE_API_KEY")
    exit(1)

keeper = MGateKeeper(llm_model=model)
gate = G8sonGate(gate_id="G5", gate_name="Audit", atomic_requirements=[
    {"req_id": "R1", "requirement": "Complete", "threshold_efficiency": 0.75}
])

print("\n" + "="*70)
print("DEMO 5: Save Audit Logs")
print("="*70)
print(f"\nModel: {model}\n")

print("Asking: 'What is machine learning?'")
response = keeper.query(user_prompt="What is machine learning?", gates=[gate])

audit_file = "audit_log.qson"
keeper.save_audit_log(response, audit_file)
print(f"\n✅ Saved to: {audit_file}\n")

loaded = keeper.load_audit_log(audit_file)

print("="*70)
print("AUDIT LOG")
print("="*70)
print(f"\nID: {loaded['audit_id']}")
print(f"Question: {loaded['query_input']['user_prompt']}")
print(f"Gates Passed: {loaded['gates_passed']}")
print(f"Confidence: {loaded['overall_confidence'] * 100:.1f}%")
print(f"\nAnswer: {loaded['llm_response']['content'][:150]}...")
print("\n✅ Complete record saved and loaded!")
print("="*70 + "\n")