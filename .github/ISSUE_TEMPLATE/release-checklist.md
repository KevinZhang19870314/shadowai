---
name: Release Checklist
about: Checklist for preparing a new release
title: 'Release v[VERSION]'
labels: 'release'
assignees: ''

---

## Release Checklist for v[VERSION]

### Pre-release
- [ ] All tests are passing on main branch
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated with new features/fixes
- [ ] Version number is updated in pyproject.toml
- [ ] No outstanding critical issues

### Release Process
- [ ] Create release tag: `git tag -a v[VERSION] -m "Release v[VERSION]"`
- [ ] Push tag: `git push origin v[VERSION]`
- [ ] Verify GitHub Actions workflow completes successfully
- [ ] Confirm package is published to PyPI
- [ ] Verify GitHub release is created with correct artifacts

### Post-release
- [ ] Test installation from PyPI: `pip install shadowai==[VERSION]`
- [ ] Update any dependent projects
- [ ] Announce release (if applicable)
- [ ] Close this issue

### Notes
- Release workflow is triggered automatically when a tag matching `v*` is pushed
- The workflow will:
  1. Run tests
  2. Build the package
  3. Publish to PyPI
  4. Create GitHub release with assets 