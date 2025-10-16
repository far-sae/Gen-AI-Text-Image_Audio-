def build_few_shot(template: str, examples: list, input_text: str):
    parts = []
    for ex in examples:
        parts.append(f"### Example\nInput: {ex['input']}\nOutput: {ex['output']}\n")
    parts.append("### Prompt\n" + template.format(input_text=input_text))
    return "\n\n".join(parts)
