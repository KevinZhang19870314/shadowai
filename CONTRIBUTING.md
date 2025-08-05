# Contributing Guide

Thank you for your interest in the ShadowAI project! We welcome all forms of contributions.

## 🤝 How to Contribute

### Reporting Issues

If you found a bug or have feature suggestions, please:

1. Search existing issues to ensure the problem hasn't been reported
2. Create a new issue with detailed description
3. Include reproduction steps, expected behavior, and actual behavior
4. Provide relevant environment information

### Contributing Code

1. **Fork the project** - Fork this repository on GitHub
2. **Create a branch** - Create a new branch for your feature
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Write code** - Implement your feature or fix
4. **Write tests** - Add test cases for new features
5. **Run tests** - Ensure all tests pass
   ```bash
   python -m pytest tests/
   ```
6. **Check code style** - Run code quality checks
   ```bash
   black lib/
   isort lib/
   flake8 lib/
   ```
7. **Commit changes** - Commit your changes
   ```bash
   git commit -m "Add: brief description of your changes"
   ```
8. **Push branch** - Push to your fork
   ```bash
   git push origin feature/amazing-feature
   ```
9. **Create Pull Request** - Create a PR on GitHub

## 📝 Code Standards

### Coding Style

- Use Black for code formatting
- Use isort for import sorting
- Follow PEP 8 code style
- Use meaningful variable and function names
- Add appropriate type annotations

### Commit Message Format

Use the following format for commit messages:

```
Type: brief description

Detailed description (optional)

Related issue: #123
```

**Types include:**
- `Add`: Adding new features
- `Fix`: Bug fixes
- `Update`: Updating existing features
- `Remove`: Removing features
- `Docs`: Documentation changes
- `Test`: Test-related
- `Refactor`: Code refactoring

### Documentation

- Add docstrings for all public functions and classes
- Update relevant README and documentation
- Include usage examples

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_rule.py

# Run tests with coverage report
python -m pytest tests/ --cov=shadowai --cov-report=html
```

### Writing Tests

- Write unit tests for new features
- Ensure test coverage remains high
- Use descriptive test names
- Include boundary conditions and error case tests

## 📦 Release Process

For maintainers only:

1. Update version number
2. Update CHANGELOG
3. Run release script
   ```bash
   python scripts/publish.py --version 0.1.1 --test  # Test release
   python scripts/publish.py --version 0.1.1         # Production release
   ```

## ❓ Getting Help

If you have any questions:

1. Check existing documentation and examples
2. Search closed issues
3. Ask questions in Discord/discussion forums
4. Create a new issue

## 📄 License

By contributing code, you agree that your contributions will be licensed under the MIT License.

---

Thank you again for your contributions! 🎉 