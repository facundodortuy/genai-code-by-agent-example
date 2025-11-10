# genai-code-by-agent-example

A simple prompt generator that creates structured prompts based on user-provided subjects.

## Features

- Generate comprehensive prompts for any subject
- Interactive command-line interface
- Input validation and error handling
- Unit tests included

## Usage

### Interactive Mode

Run the prompt generator interactively:

```bash
python3 prompt_generator.py
```

You'll be prompted to enter a subject, and the program will generate a structured prompt about that subject.

### Example

```
Enter a subject to generate a prompt: Machine Learning

Generated Prompt:
------------------------------------------------------------

Generate a comprehensive explanation about Machine Learning.

Please include:
1. A clear definition or introduction to Machine Learning
2. Key concepts and principles related to Machine Learning
3. Practical applications or examples of Machine Learning
4. Common challenges or misconceptions about Machine Learning
5. Resources for learning more about Machine Learning

Provide a detailed and informative response.
```

### Programmatic Usage

You can also import and use the `generate_prompt` function in your own code:

```python
from prompt_generator import generate_prompt

prompt = generate_prompt("Artificial Intelligence")
print(prompt)
```

## Testing

Run the unit tests:

```bash
python3 test_prompt_generator.py
```

Run with verbose output:

```bash
python3 test_prompt_generator.py -v
```

## Requirements

- Python 3.6 or higher
- No external dependencies required