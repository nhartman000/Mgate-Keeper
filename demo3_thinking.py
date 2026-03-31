#!/usr/bin/env python3
import os
import json
from mgate_keeper import MGateKeeper

if not os.getenv('OPENAI_API_KEY'):
    print("ERROR: Set OPENAI_API_KEY")
    exit(1)

keeper = MGateKeeper(llm_model="gpt-3.5-turbo")

print("\n" + "="*70)
print("DEMO 3: Photosynthesis with Detailed Explanation")
print("="*70)
print(f"\nModel: gpt-3.5-turbo\n")

question = "What is photosynthesis? Explain the process step by step."
response = keeper.query(question)

print("="*70)
print("DETAILED EXPLANATION")
print("="*70 + "\n")

answer = response.choices[0].message.content
print(f"{answer}\n")

print("="*70)
print("RESPONSE METRICS")
print("="*70)
print(f"Response ID: {response.id}")
print(f"Prompt Tokens: {response.usage.prompt_tokens}")
print(f"Completion Tokens: {response.usage.completion_tokens}")
print(f"Total Tokens: {response.usage.total_tokens}")
print("="*70 + "\n")
