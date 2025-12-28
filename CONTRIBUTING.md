# Contributing to Energetic Epicenter Detector

Thank you for your interest in contributing to EED! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Optical-flow-epicenter-detection-.git
   cd Optical-flow-epicenter-detection-
   ```
3. **Set up the development environment**:
   ```bash
   ./setup.sh
   source .venv/bin/activate
   ```

## Development Workflow

1. **Create a branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Run tests** to ensure nothing breaks:
   ```bash
   python -m unittest discover tests -v
   ```

4. **Commit your changes** with clear, descriptive messages:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

### Documentation

- Update README.md if you add new features
- Add docstrings to new functions with Args, Returns, and Raises sections
- Update SETUP.md if installation process changes

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage
- Tests should be in the `tests/` directory

Example test structure:

```python
import unittest
from energetic_detector import EnergeticEpicenterDetector

class TestNewFeature(unittest.TestCase):
    def test_feature(self):
        # Test code here
        self.assertTrue(True)
```

## Adding New Features

### New Detection Algorithms

If adding new detection algorithms:
1. Add implementation to `energetic_detector.py`
2. Maintain backward compatibility
3. Add configuration options
4. Write comprehensive tests
5. Update documentation with usage examples

### New Tools

If creating new tools or integrations:
1. Create new file in project root
2. Follow existing code style
3. Add tests to `tests/` directory
4. Update README and SETUP.md
5. Add entry point to setup.py if needed

## Reporting Bugs

When reporting bugs, include:
- Python version
- Operating system
- OpenCV version
- Full error traceback
- Minimal code to reproduce the issue
- Expected vs actual behavior

## Feature Requests

For feature requests:
- Check if feature already exists or is planned
- Explain the use case clearly
- Provide examples if possible
- Consider if it fits the project scope

## Code Review Process

All submissions require review. We use GitHub pull requests for this purpose.

Reviewers will check:
- Code quality and style
- Test coverage
- Documentation completeness
- Performance impact
- Security considerations

## Testing Locally

Run the full test suite:

```bash
# All tests
python -m unittest discover tests -v

# Specific test file
python -m unittest tests.test_detector -v

# With coverage (if installed)
coverage run -m unittest discover tests
coverage report
```

## Performance Considerations

- Profile code for performance-critical sections
- Consider memory usage for large videos
- Document any performance trade-offs
- Test with various video sizes and formats

## Security

- Never commit credentials or API keys
- Sanitize user inputs
- Be cautious with file operations
- Follow security best practices

## Questions?

If you have questions:
- Check existing issues and discussions
- Read the documentation thoroughly
- Ask in a new issue with the "question" label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!
