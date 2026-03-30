#!/usr/bin/env python3
import os
from mgate_keeper import MGateKeeper, G8sonGate, GstContext

model = "gpt-4-turbo-preview"
if not os.getenv('OPENAI_API_KEY'):
    print("ERROR: Set OPENAI_API_KEY")
    exit(1)

keeper = MGateKeeper(llm_model=model, seed=42)
gate = G8sonGate(gate_id="G2", gate_name="Test")
context = GstContext(interpretation_posture="Factual", primary_modality="👁️")

print("\n" + "="*70)
print("DEMO 2: Deterministic Reproducibility")
print("="*70)
print(f"\nModel: {model} (seed=42)\n")

print("API CALL #1:\n")
response1 = keeper.query(user_prompt="What is photosynthesis? Explain simply.", gates=[gate], context=context)
answer1 = response1.choices[0].message.content
print(f"{answer1}\n")

print("="*70)
print("\nAPI CALL #2 (same question):\n")
keeper2 = MGateKeeper(llm_model=model, seed=42)
response2 = keeper2.query(user_prompt="What is photosynthesis? Explain simply.", gates=[gate], context=context)
answer2 = response2.choices[0].message.content
print(f"{answer2}\n")

print("="*70)
if answer1 == answer2:
    print("✅ DETERMINISTIC: Identical answers from two API calls")
else:
    print("❌ Different answers")
print("="*70 + "\n")