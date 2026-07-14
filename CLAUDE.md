# Using Claude in Git

This guide explains how to use [Claude](https://claude.ai) (Anthropic's AI assistant) to help with git workflows in this project.

---

## What Claude Can Help With

Claude can assist you at every stage of a git-based development workflow:

- **Writing commit messages** – describe your changes and let Claude suggest a clear, conventional commit message
- **Code review** – paste a diff and ask Claude to review it for bugs, security issues, or style
- **Resolving merge conflicts** – share the conflicting sections and Claude can suggest how to resolve them
- **Understanding diffs** – ask Claude to explain what a `git diff` or PR change actually does
- **Drafting PR descriptions** – paste your changes and have Claude write a pull request summary
- **Debugging git commands** – ask Claude what a specific git command does or how to fix a git mistake

---

## Quick Start

### Use Claude via the Web

The simplest approach is to open [claude.ai](https://claude.ai) in your browser alongside your terminal and paste relevant git output directly into the chat.

### Use Claude via the API

If you want to integrate Claude into scripts, set up an API key from the [Anthropic Console](https://console.anthropic.com) and use it with the [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python):

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_api_key_here
```

Then call the API from your own scripts to pass git output to Claude programmatically.

---

## Example Workflows

### Generate a Commit Message

Run `git diff --staged` in your terminal, copy the output, and paste it into [claude.ai](https://claude.ai) with the prompt:

> "Write a concise git commit message for these staged changes following the Conventional Commits format."

**Example prompt:**
```
Write a git commit message for this diff:

<paste your git diff --staged output here>
```

---

### Review a Pull Request Diff

Run `git diff main...feature-branch`, copy the output, and paste it into Claude with:

> "Review this diff for bugs, security issues, and style improvements."

---

### Resolve a Merge Conflict

When `git merge` or `git rebase` leaves conflict markers in a file, paste the conflicting section into Claude:

```
<<<<<<< HEAD
your_code_here
=======
incoming_code_here
>>>>>>> feature-branch
```

Ask:
> "Help me resolve this merge conflict. The HEAD version does X, and the incoming version does Y."

---

### Understand a Git Log

Run `git log --oneline -20`, copy the output, and paste it into Claude with:

> "Summarize the recent development history of this project based on these commits."

---

### Fix a Git Mistake

If you accidentally committed to the wrong branch, reset a file, or need to undo something, ask:

> "I accidentally committed directly to main. How do I move my last commit to a new branch?"

---

## Tips for This Project

- When adding new facial biometric feature extraction or cryptographic key generation code, use Claude to review your implementation for security best practices before committing.
- Paste your `git diff` into Claude and ask it to check for common issues like hardcoded secrets, unhandled exceptions, or insecure key derivation patterns.
- Use Claude to help write clear commit messages that follow the project history (see `git log --oneline`).
- When exploring Solidity or web3 integration (planned next phase), ask Claude to review smart contract code for common vulnerabilities before pushing.

---

## Resources

- [Claude Documentation](https://docs.anthropic.com)
- [Conventional Commits Specification](https://www.conventionalcommits.org)
- [Git Documentation](https://git-scm.com/doc)
