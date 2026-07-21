# Training Notes

## Formatting for Models

### Thinking Models (Chain-of-Thought)
Use entries as-is. The `<think>` tags train the model to reason before
generating code.

```
<think>
Analysis and reasoning here...
</think>

```bash
#!/bin/bash
# solution code
```
```

### Non-Thinking Models (Direct Response)
Strip the `<think>` block programmatically before training:

```python
import json, re

with open('terminal-training-set/batch1_system_diagnostics_oom.json') as f:
    entries = json.load(f)

for entry in entries:
    # Remove everything between <think> and </think> inclusive
    entry['output'] = re.sub(
        r'<think>.*?</think>\s*',
        '',
        entry['output'],
        flags=re.DOTALL
    ).strip()

with open('batch1_nonthinking.json', 'w') as f:
    json.dump(entries, f, indent=2)
```

### Chat Template (Recommended)

For instruction-tuned models, format each entry as:

```
<|system|>You are an expert Linux system administrator.
<|user|>{instruction}
<|assistant|>{output}
```

Adjust system prompt and separators to match your model's chat template.

## SFT (Supervised Fine-Tuning) Tips

- **Learning rate:** 1e-5 to 2e-5 for full fine-tune, 5e-6 for LoRA
- **Batch size:** 4-8 per GPU depending on context length
- **Context length:** 2048-4096 tokens (entries average ~1200 tokens)
- **Epochs:** 2-3 (dataset is high-quality, overfitting risk beyond 3)
- **LoRA rank:** 16-32 for adapter-based training

## Prompt Template Suggestions

### Zero-shot
```
Given the following system administration task, provide a step-by-step
solution with bash commands:

Task: {instruction}
```

### Few-shot (if mixing formats)
```
Task: {instruction from unrelated example}
Solution: <think>...</think> ```bash ... ```

Task: {target instruction}
Solution:
```
