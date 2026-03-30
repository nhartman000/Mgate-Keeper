#!/usr/bin/env python3
import os
import json
from mgate_keeper import MGateKeeper

if not os.getenv('OPENAI_API_KEY'):
    print("ERROR: Set OPENAI_API_KEY")
    exit(1)

# Load project
keeper = MGateKeeper(project_file="mgate_keeper/projects/photosynthesis.mg8")

print("\n" + "="*70)
print("DEMO 2: Deterministic Reproducibility with Gates & Gestalt")
print("="*70)

print(f"\n📋 PROJECT FILE LOADED: photosynthesis.mg8")
print(f"   Project: {keeper.project['project_name']}")
print(f"   ID: {keeper.project['project_id']}")

print(f"\n🔐 GATES ASSEMBLED ({len(keeper.gates)}):")
for gate in keeper.gates:
    print(f"   ✓ {gate.gate_id}: {gate.gate_name}")
    for req in gate.atomic_requirements:
        print(f"      - {req['requirement']}")

print(f"\n🎭 GESTALT CONTEXT LOADED:")
print(f"   Posture: {keeper.context.interpretation_posture}")
print(f"   Modality: {keeper.context.primary_modality}")

print(f"\n📝 PROMPT:")
prompt = "What is photosynthesis? Explain simply."
print(f"   '{prompt}'")

print("\n" + "="*70)
print("API CALL #1:")
print("="*70)
response1 = keeper.query(user_prompt=prompt, gates=keeper.gates, context=keeper.context)
answer1 = response1.choices[0].message.content
print(f"\n{answer1}\n")

print("="*70)
print("API CALL #2 (same prompt, gates, gestalt):")
print("="*70)
keeper2 = MGateKeeper(project_file="mgate_keeper/projects/photosynthesis.mg8")
response2 = keeper2.query(user_prompt=prompt, gates=keeper2.gates, context=keeper2.context)
answer2 = response2.choices[0].message.content
print(f"\n{answer2}\n")

# Create audit log
audit_log = {
    "audit_id": "AUDIT_PHOTO_001",
    "query": prompt,
    "timestamp": "2026-03-30T00:00:00Z",
    "project_id": keeper.project['project_id'],
    "gates_applied": [g.gate_id for g in keeper.gates],
    "context_applied": keeper.context.interpretation_posture,
    "model": keeper.llm_model,
    "seed": keeper.seed,
    "responses": [
        {
            "call_number": 1,
            "response_id": response1.id,
            "content": answer1
        },
        {
            "call_number": 2,
            "response_id": response2.id,
            "content": answer2
        }
    ]
}

# Save audit log
with open(keeper.project['qson_audit_log'], 'w') as f:
    json.dump(audit_log, f, indent=2)

print("="*70)
if answer1 == answer2:
    print("✅ DETERMINISTIC: Identical answers from two API calls")
    print(f"✅ AUDIT LOG SAVED: {keeper.project['qson_audit_log']}")
else:
    print("❌ Different answers")
    print(f"✓ AUDIT LOG SAVED: {keeper.project['qson_audit_log']}")
print("="*70 + "\n")