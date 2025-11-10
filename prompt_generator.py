#!/usr/bin/env python3
"""
Prompt Generator - Generate prompts based on user-provided subjects
"""


def generate_prompt(subject):
    """
    Generate a prompt based on the given subject.
    
    Args:
        subject (str): The subject to generate a prompt about
        
    Returns:
        str: A generated prompt related to the subject
    """
    if not subject or not subject.strip():
        return "Please provide a valid subject."
    
    subject = subject.strip()
    
    # Generate a thoughtful prompt based on the subject
    prompt = f"""Generate a comprehensive explanation about {subject}.

Please include:
1. A clear definition or introduction to {subject}
2. Key concepts and principles related to {subject}
3. Practical applications or examples of {subject}
4. Common challenges or misconceptions about {subject}
5. Resources for learning more about {subject}

Provide a detailed and informative response."""
    
    return prompt


def main():
    """
    Main function to run the prompt generator interactively.
    """
    print("=" * 60)
    print("Prompt Generator")
    print("=" * 60)
    print()
    
    subject = input("Enter a subject to generate a prompt: ").strip()
    
    if not subject:
        print("\nError: No subject provided.")
        return
    
    print("\n" + "-" * 60)
    print("Generated Prompt:")
    print("-" * 60)
    print()
    print(generate_prompt(subject))
    print()


if __name__ == "__main__":
    main()
