#!/usr/bin/env python3
"""
Unit tests for the prompt generator
"""

import unittest
from prompt_generator import generate_prompt


class TestPromptGenerator(unittest.TestCase):
    """Test cases for the prompt generator"""
    
    def test_generate_prompt_with_valid_subject(self):
        """Test that a valid subject generates a proper prompt"""
        subject = "Python programming"
        result = generate_prompt(subject)
        
        # Check that the prompt contains the subject
        self.assertIn(subject, result)
        self.assertIn("Python programming", result)
        
        # Check that the prompt has expected structure
        self.assertIn("definition", result.lower())
        self.assertIn("key concepts", result.lower())
        self.assertIn("practical applications", result.lower())
        
    def test_generate_prompt_with_empty_subject(self):
        """Test that an empty subject returns an error message"""
        result = generate_prompt("")
        self.assertEqual(result, "Please provide a valid subject.")
        
    def test_generate_prompt_with_whitespace_only(self):
        """Test that whitespace-only subject returns an error message"""
        result = generate_prompt("   ")
        self.assertEqual(result, "Please provide a valid subject.")
        
    def test_generate_prompt_with_none(self):
        """Test that None subject returns an error message"""
        result = generate_prompt(None)
        self.assertEqual(result, "Please provide a valid subject.")
        
    def test_generate_prompt_strips_whitespace(self):
        """Test that leading/trailing whitespace is handled correctly"""
        subject = "  Machine Learning  "
        result = generate_prompt(subject)
        
        # The trimmed subject should appear in the prompt
        self.assertIn("Machine Learning", result)
        
    def test_generate_prompt_different_subjects(self):
        """Test that different subjects generate different prompts"""
        subject1 = "Artificial Intelligence"
        subject2 = "Data Science"
        
        result1 = generate_prompt(subject1)
        result2 = generate_prompt(subject2)
        
        # Results should be different
        self.assertNotEqual(result1, result2)
        
        # Each should contain its respective subject
        self.assertIn(subject1, result1)
        self.assertIn(subject2, result2)


if __name__ == "__main__":
    unittest.main()
