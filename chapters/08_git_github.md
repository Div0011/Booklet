# 8. Git & GitHub (Version Control & Collaboration)

## 1. Introduction

### What it is
**Git** is a distributed version control system (VCS) tracking changes to source code over time. **GitHub** is a cloud-hosted Git repository platform adding collaboration features: pull requests, issue tracking, code reviews, and CI/CD pipelines. Together, they form the foundation for modern software development, enabling teams to work on the same codebase without conflicts.

### Why it exists
Created by Linus Torvalds in 2005 to manage Linux kernel development, Git solved problems with centralized VCS (CVS, Subversion): single point of failure, slow network performance, and inflexible branching. Distributed model means every developer has a full repository copy, enabling offline work and decentralized collaboration. GitHub (2008) made Git accessible, adding graphical interface, social features, and integrations.

### Problems it solves
- **Code Conflicts**: Multiple developers editing simultaneously without overwriting each other.
- **History Tracking**: Know who changed what, when, and why (for debugging and audits).
- **Parallel Development**: Branches enable simultaneous work on features without blocking.
- **Code Review**: Pull requests enforce quality checks before merging.
- **Collaboration**: Central platform for discussion, issue tracking, and project management.
- **Disaster Recovery**: Distributed copies prevent data loss from single server failure.
- **CI/CD Integration**: Automated testing and deployment triggered by commits/PRs.

### Industry Use Cases
- **Open Source**: Linux, Kubernetes, React, TensorFlow hosted on GitHub. Contributors worldwide collaborate asynchronously.
- **Enterprises**: GitHub Enterprise, GitLab, Bitbucket for internal codebases with compliance controls.
- **Startups**: Git + GitHub enable small teams to ship features fast with code review discipline.
- **Data Science**: Jupyter notebooks, model code, experiment tracking in shared repositories.
- **DevOps**: Infrastructure-as-Code (Terraform, Ansible) version-controlled with Git.
- **Documentation**: README.md, wikis, and docs tracked alongside code.

### Analogy
Think of Git as a **time machine for code**. Each commit is a checkpoint you can return to. Branches are parallel timelines you can explore without affecting the main story. Merging is combining timelines. GitHub is the **public library** where you share your code, collaborators can check out your branches, suggest changes (PRs), and discussions happen transparently.

---

## 2. Core Concepts

### Beginner Concepts

#### Repository (Repo)
A folder containing project files and a `.git` subdirectory storing history (commits, branches, tags). Local repo lives on your machine; remote repo (GitHub) is a server copy.

```bash
git init                  # Create local repo
git clone <url>           # Copy remote repo to local
ls -la                    # Shows .git folder
```

#### Commits
Snapshots of code state. Each commit has:
- **Hash**: Unique SHA-1 identifier (e.g., `a1b2c3d`).
- **Author**: Who made the change.
- **Date**: When committed.
- **Message**: Description of changes.
- **Parent**: Link to previous commit (except root).

```bash
git add <file>            # Stage changes
git commit -m "Add login feature"  # Create commit with message
git log                   # View commit history
```

#### Branches
Independent lines of development. `main` (or `master`) is default. Feature branches isolate work.

```bash
git branch                # List branches
git branch feature/login  # Create new branch
git checkout feature/login  # Switch to branch
git checkout -b feature/login  # Create and switch (shorthand)
```

#### Staging Area
Intermediate zone between working directory and commits. `git add` stages changes; `git commit` locks them in.

```
[Working Dir] --add--> [Staging] --commit--> [Repository]
```

#### Merge
Combines two branches. Integrates feature branch into main.

```bash
git checkout main
git merge feature/login   # Merge feature/login into main
```

#### Pull Request (PR)
GitHub feature: propose merging your branch into main. Enables code review before merge. Typical workflow:
1. Push feature branch to GitHub.
2. Open PR on GitHub.
3. Team reviews and comments.
4. Author fixes issues.
5. Maintainer merges PR.

### Intermediate Concepts

#### Rebase
Alternative to merge. Replays commits from feature branch onto main, creating linear history.

```bash
git checkout feature/login
git rebase main           # Replay feature commits on top of main

# Result: linear history (main → feature)
# vs merge: two parent commits, non-linear
```

**Rebase vs Merge**:
- **Merge**: Non-linear, preserves history, easy to understand.
- **Rebase**: Linear, cleaner log, rewrites history (risky for shared branches).

#### Staging and Unstaging
Fine-grained control over what goes into commits.

```bash
git status                # See modified, staged, untracked files
git add file1 file2       # Stage specific files
git add .                 # Stage all changes
git reset file1           # Unstage file1
git checkout -- file1     # Discard changes to file1
```

#### Remote Tracking
Local branches can track remote branches (e.g., `origin/main` tracks `main` on GitHub).

```bash
git branch -a             # List all branches (local + remote)
git pull                  # Fetch + merge origin/main into local main
git push origin feature/login  # Push local branch to GitHub
```

#### Stashing
Temporarily save uncommitted changes without committing.

```bash
git stash                 # Save changes
git stash list            # List stashes
git stash pop             # Restore latest stash (and remove)
git stash apply           # Restore stash (keep it)
```

#### Tags
Named pointers to specific commits. Used for releases (v1.0.0, v2.1.1).

```bash
git tag v1.0.0            # Create lightweight tag
git tag -a v1.0.0 -m "Release 1.0"  # Annotated tag (with message)
git push origin v1.0.0    # Push tag to GitHub
```

### Advanced Concepts

#### Interactive Rebase
Edit, reorder, squash, or drop commits in history. Powerful but dangerous on shared branches.

```bash
git rebase -i HEAD~3      # Rebase last 3 commits interactively
# Editor opens; options: pick, reword, squash, drop
```

#### Cherry-Pick
Apply a specific commit to current branch without merging entire branch.

```bash
git cherry-pick a1b2c3d   # Apply commit to current branch
```

#### Blame and Bisect
- **Blame**: See who modified each line and when.
- **Bisect**: Binary search through commits to find bug introduction.

```bash
git blame file.py         # Show author of each line
git bisect start          # Binary search for bug
```

#### Reflog
Local reference log. Records all branch movements. Can recover lost commits.

```bash
git reflog                # View local history
git checkout @{1}         # Go back to previous HEAD state
```

#### Worktrees
Multiple working directories from same repo. Useful for parallel work.

```bash
git worktree add ../feature1 feature/login
git worktree add ../feature2 feature/payment
# Two directories with independent branches
```

---

## 3. Internal Working

### Git Data Model
```
Repository
  ├── objects/ (database)
  │   ├── commit objects (snapshots)
  │   ├── tree objects (directories)
  │   └── blob objects (file contents)
  ├── refs/
  │   ├── heads/ (local branches)
  │   └── remotes/ (remote tracking branches)
  └── HEAD (current branch pointer)

Commit object:
  ├── Tree (directory structure)
  ├── Parent commit(s)
  ├── Author
  ├── Date
  └── Message

Tree object:
  ├── Blob: file1.py (hash: abc123)
  ├── Blob: file2.py (hash: def456)
  └── Tree: src/ (hash: ghi789)
      └── Blob: main.py (hash: jkl012)
```

### Three-Way Merge
When merging branches, Git finds common ancestor and combines changes.

```
        A1 ← feature
       /
   A0 ← main
   |
   B1 ← feature

Merge: Compare A0→A1 (feature changes) with A0→B1 (main changes)
Result: Combine both changes if no conflict
```

**Conflicts**: If both branches modify same lines, Git marks conflict; developer resolves manually.

```
<<<<<<< HEAD (main)
print("Hello")
=======
print("Hi")
>>>>>>> feature
```

### Push, Pull, and Fetch
```
[Local Repo] --push--> [GitHub Remote]
[Local Repo] <--pull-- [GitHub Remote]
             <--fetch--

pull = fetch + merge
fetch = download without merging
```

### Branching Strategy Example
```
main (stable)
  └─→ develop (integration)
      ├─→ feature/auth (feature branch)
      ├─→ feature/ui (feature branch)
      └─→ hotfix/bug-fix (bug fix)

Workflow: feature → develop (PR+review) → main (release)
```

---

## 4. Important Terminology

| Term | Definition |
|------|-----------|
| **Repository** | Folder with .git directory storing history. |
| **Commit** | Snapshot with hash, author, date, message, parent. |
| **Branch** | Independent line of development; pointer to commit. |
| **HEAD** | Current commit/branch you're working on. |
| **Staging** | Intermediate zone (git add) between working dir and commits. |
| **Merge** | Combine two branches; creates merge commit if non-FF. |
| **Rebase** | Replays commits on new base; linear history. |
| **Remote** | Server copy of repo (GitHub, GitLab). `origin` is default. |
| **Pull** | Fetch + merge from remote. |
| **Push** | Upload commits to remote. |
| **Tag** | Named pointer to commit; used for releases. |
| **Stash** | Temporary save of uncommitted changes. |
| **Cherry-Pick** | Apply specific commit to current branch. |
| **Bisect** | Binary search to find bug-introducing commit. |
| **Reflog** | Local history of branch movements. |
| **Fast-Forward** | Move branch pointer forward without merge commit. |
| **Conflict** | Incompatible changes on same lines in both branches. |

---

## 5. Beginner Examples

### Example 1: Basic Workflow (Init, Add, Commit)
```bash
mkdir my_project
cd my_project
git init                    # Initialize repo

echo "print('hello')" > main.py
git add main.py             # Stage file
git commit -m "Add main.py"  # Create commit

git log                      # View commit history
# Output: commit a1b2c3d4... (HEAD -> main)
#         Author: Alice <alice@example.com>
#         Date: Mon Jan 1 00:00:00 2024 +0000
#         Add main.py
```

### Example 2: Branching and Merging
```bash
git branch                  # Show branches (* indicates current)
# Output: * main

git branch feature/login    # Create new branch
git checkout feature/login  # Switch to branch
# Or: git checkout -b feature/login (create + switch)

echo "def login():" >> main.py
git add main.py
git commit -m "Add login function"

git checkout main           # Switch back to main
git merge feature/login     # Merge feature into main

git branch -d feature/login # Delete feature branch (cleanup)
```

### Example 3: Remote Collaboration (GitHub)
```bash
git remote add origin https://github.com/alice/my_project.git
# Link local repo to GitHub

git push -u origin main     # Push main to GitHub (-u sets upstream)
# Now: local main tracks origin/main

git pull                    # Fetch + merge from origin/main
git push                    # Push local commits to origin/main
```

### Example 4: Checking Status and History
```bash
git status                  # See current state
# Output:
# On branch main
# Changes not staged for commit:
#   modified: main.py
# Untracked files:
#   test.py

git diff                    # Show changes in modified files
git diff --staged           # Show changes in staging area

git log --oneline           # Compact log
# Output:
# a1b2c3d Add login function
# def4567 Add main.py
# ghi8901 Initial commit

git log --graph --all --oneline --decorate  # Visual history
```

### Example 5: Undoing Changes
```bash
# Undo unstaged changes
git checkout -- main.py     # Discard changes to main.py

# Undo staged changes
git reset main.py           # Unstage main.py

# Undo commits
git revert a1b2c3d          # Create new commit undoing a1b2c3d
git reset --soft HEAD~1     # Undo last commit, keep changes staged
git reset --hard HEAD~1     # Undo last commit, discard changes
```

---

## 6. Intermediate Examples

### Example 1: Pull Request Workflow
```bash
# On GitHub: fork repo to your account
git clone https://github.com/yourname/someone_else_repo
cd someone_else_repo

git checkout -b feature/improvement
# Make changes
git add .; git commit -m "Improve performance"

git push origin feature/improvement
# Go to GitHub, open PR from feature/improvement → main
# Respond to review comments

git add .; git commit -m "Address review feedback"
git push  # Updates PR automatically

# Maintainer merges PR
git checkout main; git pull  # Sync local with merged PR
```

### Example 2: Rebase vs Merge Visualization
```bash
# Before:
# main:    A -- B -- D
#               \
# feature:      C

# After merge (non-linear):
# main:    A -- B -- D -- M (merge commit)
#               \         /
# feature:      C -------

git merge feature

# After rebase (linear):
# main:    A -- B -- D -- C'

git rebase main feature
git checkout main; git merge feature  # FF merge
```

### Example 3: Interactive Rebase (Squash Commits)
```bash
git log --oneline
# Output:
# a1b2c3d Add form field
# def4567 Fix form validation
# ghi8901 Refactor form component

git rebase -i HEAD~3       # Rebase last 3 commits
# Editor opens:
# pick ghi8901 Refactor form component
# pick def4567 Fix form validation
# pick a1b2c3d Add form field

# Change to:
# pick ghi8901 Refactor form component
# squash def4567 Fix form validation
# squash a1b2c3d Add form field

# Result: Single commit with all changes
```

### Example 4: Stashing Work in Progress
```bash
# Working on feature, emergency bug fix needed
git stash                   # Save uncommitted changes
git status                  # Working dir clean

git checkout -b hotfix/bug
# Fix bug, commit, push, PR merged

git checkout feature        # Switch back to feature
git stash pop               # Restore saved changes
# Continue working
```

### Example 5: Finding Bug with Bisect
```bash
git log --oneline           # Find when bug appeared
git bisect start
git bisect bad HEAD         # Current commit has bug
git bisect good v1.0        # Known good commit

# Git checks out middle commit
# Test: git bisect good (no bug) or git bisect bad (has bug)
# Repeat until bug-introducing commit found

git bisect log              # View bisect history
git bisect reset            # Exit bisect mode
```

---

## 7. Advanced Examples

### Example 1: Collaborative Workflow with Code Review
```bash
# Developer 1: Feature branch
git checkout -b feature/auth
# Make changes...
git push origin feature/auth

# On GitHub: create PR, request reviewer

# Developer 2: Review PR
git fetch origin
git checkout feature/auth  # Check out PR branch
# Review code locally, test

# Comment on GitHub with feedback

# Developer 1: Address feedback
# Make changes, commit, push
git push

# Developer 2: Re-review, approve
# GitHub shows: all checks passed, approved

# Maintainer: Merge PR
git checkout main
git pull
git merge origin/feature/auth
git push
# Or: Use GitHub "Merge" button

# Clean up
git branch -d feature/auth
git push origin --delete feature/auth
```

### Example 2: Cherry-Pick for Selective Integration
```bash
git log --oneline
# main:     A -- B -- D -- E
# hotfix:   B -- C

git checkout main
git cherry-pick <commit-C>  # Apply only C to main, not entire hotfix

# Result: A -- B -- D -- E -- C'
```

### Example 3: Reflog for Disaster Recovery
```bash
# Accidentally reset hard; lost commits
git reflog
# Output:
# a1b2c3d HEAD@{0}: reset: moving to HEAD~3
# def4567 HEAD@{1}: commit: Add feature
# ghi8901 HEAD@{2}: commit: Fix bug

git checkout def4567        # Go back to lost commit
git branch recovered-work   # Create branch to save it
# Now commits not lost
```

### Example 4: Worktrees for Parallel Development
```bash
# Main workspace
cd ~/project
git worktree add ../feature1 -b feature/auth
# New worktree in ../feature1 with branch feature/auth

cd ../feature1
# Work on feature/auth independently
git add .; git commit -m "Add auth"

cd ~/project
# Still on original branch in main workspace

git worktree remove ../feature1  # Clean up worktree
```

### Example 5: Automating with Git Hooks
```bash
# .git/hooks/pre-commit (run before commit)
#!/bin/bash
# Check code style
flake8 *.py
if [ $? -ne 0 ]; then
  echo "Flake8 check failed"
  exit 1  # Prevent commit
fi

chmod +x .git/hooks/pre-commit
# Now: before each commit, run flake8 automatically
```

---

## 8. How Interviewers Think

Interviewers assess your Git proficiency through workflow questions, conflict resolution, and understanding of distributed VCS concepts. They want developers who collaborate effectively, understand branching strategies, and can recover from mistakes.

### Red Flags
- Not knowing what a commit hash represents.
- Confusing merge and rebase; using wrong strategy.
- Force-pushing to shared branches (destroys others' work).
- Committing large binaries or credentials to repo.
- Not understanding pull requests or code review.
- Using `git reset --hard` carelessly.

### Green Flags
- Explaining branching strategy (GitFlow, trunk-based development).
- Discussing when to rebase vs merge (squash for PRs, preserve history on main).
- Understanding interactive rebase for clean history.
- Knowing how to resolve merge conflicts.
- Demonstrating awareness of distributed concepts (eventual consistency, offline work).
- Describing how to recover lost commits with reflog.

### Answer Matrix
| Level | Question: "Walk me through a PR workflow" |
|-------|------|
| **Rejected** | "I commit to main and push." |
| **Shortlisted** | "I create a branch, make changes, push, and open a PR." |
| **Selected** | "I create a feature branch from main. Push to GitHub, open PR, request review. Respond to review comments, make fixes, push updates. Reviewer approves. Maintainer merges (squash or rebase for clean history). I delete the remote branch, sync main locally. I advocate for meaningful commit messages and clean history." |

---

## 9. Frequently Asked Interview Questions (60 Questions)

### Conceptual (1-15)

**1. What is Git? Why distributed?**
Version control tracking code changes over time. Distributed means every developer has full repo copy, enabling offline work, decentralized collaboration, and disaster recovery. Contrast with centralized VCS (SVN) requiring server for every operation.

**2. What is a commit?**
Snapshot of code state with hash (SHA-1), author, date, message, parent link. Hash is deterministic: same code → same hash. Uniquely identifies version.

**3. Difference between fetch, pull, merge.**
- **Fetch**: Download commits from remote without merging.
- **Pull**: Fetch + merge (or rebase).
- **Merge**: Combine two branches, creates merge commit (unless fast-forward).

**4. What is a merge conflict?**
When both branches modify same lines differently, Git can't auto-merge. Developer resolves manually, choosing which version to keep or combining both.

**5. Rebase vs merge.**
**Merge**: Preserves history, non-linear. **Rebase**: Linear history, rewrites history (risky for shared branches). Use rebase for feature branches before merging to main; merge on main for transparency.

**6. What is HEAD?**
Pointer to current commit/branch. `HEAD~1` = parent commit. `git checkout HEAD~2` detaches HEAD (useful for inspecting old code).

**7. What is a remote?**
Server copy of repo (GitHub, GitLab). `origin` is default. `origin/main` is remote tracking branch.

**8. How does git push work?**
Uploads local commits to remote. Updates remote branch to match local. Requires network access to server.

**9. What is a tag?**
Named pointer to commit, typically for releases (v1.0.0). Lightweight or annotated (with message). Doesn't move like branches.

**10. What is `.gitignore`?**
File listing patterns for files Git should ignore (not track). Common: `*.log`, `node_modules/`, `.env` (credentials). Prevents accidental commits of sensitive/build files.

**11. What is a pull request?**
GitHub feature: propose merging feature branch into main. Enables code review, discussion, and CI/CD checks before merge. Central to collaborative workflow.

**12. Difference between `git reset` and `git revert`.**
- **Reset**: Move HEAD pointer, modifies history (dangerous). `--soft` (keep changes), `--mixed` (unstage), `--hard` (discard).
- **Revert**: Creates new commit undoing changes (safe, preserves history).

**13. What is `git stash`?**
Temporarily save uncommitted changes without committing. Useful for context switching. `git stash pop` restores.

**14. What is cherry-pick?**
Apply specific commit to current branch without merging entire branch. Useful for hotfixes or selective backports.

**15. How do you undo a commit?**
- **Not pushed**: `git reset --soft HEAD~1` (keep changes), `git reset --hard HEAD~1` (discard).
- **Already pushed**: `git revert <hash>` (create new commit undoing changes).

### Scenario-Based (16-30)

**16. Handle merge conflict.**
```bash
git merge feature
# Conflict marker in file:
# <<<<<<< HEAD (main)
# print("Hello")
# =======
# print("Hi")
# >>>>>>> feature

# Edit file, choose version or combine
git add file.py
git commit -m "Resolve conflict"
```

**17. You committed to wrong branch.**
```bash
# Committed to main instead of feature
git reset HEAD~1                    # Undo commit, keep changes
git checkout -b feature/correct     # Create correct branch
git add .; git commit -m "..."       # Commit to correct branch
```

**18. You force-pushed and destroyed others' work.**
```bash
git reflog                          # Find lost commit
git checkout <hash>                 # Go to lost commit
git branch recovered                # Save it
git push origin recovered           # Push for others to restore
```

**19. You need to revert a commit on production.**
```bash
git log --oneline
git revert <commit-hash>            # Creates new commit undoing it
git push                            # Safe; preserves history
```

**20. Large file committed to Git; need to remove.**
```bash
git rm --cached large_file.bin      # Stop tracking
git commit -m "Remove large file"
git push

# To remove from history (destructive):
git filter-branch --tree-filter 'rm -f large_file.bin' HEAD
git push origin --force
```

**21. You want interactive rebase to squash commits.**
```bash
git rebase -i HEAD~3
# In editor:
# pick a1b2c3d Commit 1
# squash def4567 Commit 2
# squash ghi8901 Commit 3
# Result: Single commit with combined message
```

**22. You accidentally deleted a local branch.**
```bash
git reflog                          # Shows branch deletions
git checkout <hash>                 # Restore deleted commits
git branch recovered                # Save as new branch
```

**23. Sync fork with upstream.**
```bash
git remote add upstream https://github.com/original/repo
git fetch upstream
git checkout main
git merge upstream/main             # Or: git rebase upstream/main
git push origin main                # Push synced version to your fork
```

**24. Bisect to find bug-introducing commit.**
```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git checks out middle commit; test it
git bisect good (or bad)
# Repeat until found
git bisect reset
```

**25. Tag release version.**
```bash
git tag -a v1.2.3 -m "Release 1.2.3"
git push origin v1.2.3
```

**26. Rebase feature branch before merging.**
```bash
git checkout feature
git rebase main                     # Replays feature on top of main
git checkout main
git merge feature                   # Fast-forward (no merge commit)
```

**27. Cherry-pick critical fix to multiple branches.**
```bash
git checkout main
git cherry-pick <fix-hash>
git push

git checkout release-v2.0
git cherry-pick <fix-hash>
git push

# Fix applied to both main and release branch
```

**28. Partial staging: commit only some changes.**
```bash
git add -p                          # Interactive staging
# Prompt: stage this hunk? (y/n/s/e)
git commit -m "Stage 1"

git add -p                          # Stage remaining
git commit -m "Stage 2"
```

**29. Rename branch.**
```bash
git branch -m old_name new_name     # Local
git push origin -u new_name         # Push to GitHub
git push origin --delete old_name   # Delete old
```

**30. View blame to find bug.**
```bash
git blame buggy_file.py
# Output: shows author + commit hash for each line
# Find suspicious line, check commit: git show <hash>
```

### Debugging (31-45)

**31. Commit message typo; fix it.**
```bash
git commit --amend -m "Correct message"
```

**32. Forgot to add a file to commit.**
```bash
git add forgotten_file
git commit --amend
# Amends previous commit (if not pushed)
```

**33. Multiple commits should be one.**
```bash
git rebase -i HEAD~3
# Mark commits 2-3 as 'squash'
# Result: combined into first commit
```

**34. Accidentally committed credentials.**
```bash
git rm --cached .env
git commit --amend --no-edit
git push origin --force-with-lease

# Better: rotate credentials immediately; prevent wasn't enough
```

**35. Wrong remote URL.**
```bash
git remote set-url origin https://github.com/correct/repo
git push  # Now pushes to correct remote
```

**36. History has commits from wrong author.**
```bash
# Fix global config
git config --global user.name "Correct Name"
git config --global user.email "correct@email.com"

# Amend recent commits
git commit --amend --author="New Name <email>"
```

**37. Detached HEAD state; made commits.**
```bash
git reflog                          # See commit hashes
git branch recovery <hash>          # Save commits to branch
git checkout main                   # Leave detached state
```

**38. Push rejected: remote has newer commits.**
```bash
git pull origin main --rebase       # Rebase local on remote
# Or: git pull (merge)
git push
```

**39. Accidentally committed and pushed to main.**
```bash
git revert <commit-hash>            # Safe; new commit undoes it
git push

# If not pushed yet: git reset --hard HEAD~1
```

**40. Merge commit with unresolved conflict.**
```bash
git merge --abort                   # Cancel merge
# Fix issues
git merge feature                   # Retry
```

### System Design (41-55)

**41. Typical feature branch structure.**
Feature branches isolate work. Convention: `feature/`, `bugfix/`, `hotfix/` prefixes. Example: `feature/user-auth`, `bugfix/login-crash`, `hotfix/sql-injection`.

**42. Commit message best practices.**
First line: 50 chars, imperative mood ("Add feature", not "Added"). Blank line. Body: explain why, not what. Example:
```
Add user authentication

Implement JWT-based auth for API endpoints.
Validates tokens on protected routes. Refreshes
on expiry. Addresses security audit findings.
```

**43. .gitignore for Python project.**
```
__pycache__/
*.pyc
.venv/
.env
.DS_Store
*.log
node_modules/
dist/
build/
```

**44. Branching strategy: GitFlow vs Trunk-Based.**
- **GitFlow**: Separate develop/main; feature branches from develop. Structured but slower releases.
- **Trunk-Based**: All work on main/develop; short-lived branches. Fast releases; requires strong CI/CD.

**45. Enforcing code review before merge.**
GitHub: branch protection rules. Require PR reviews, passing CI checks before merge. Prevents main branch degradation.

### Advanced (46-60)

**46. Submodules: include external repo.**
```bash
git submodule add https://github.com/other/lib lib/
git commit -m "Add submodule"
# lib/ contains external repo; separately versioned
```

**47. Git hooks: automated checks.**
```bash
# .git/hooks/pre-commit
#!/bin/bash
npm run lint
npm run test
# Fails if tests fail; prevents commit
```

**48. Shallow clone for large repos.**
```bash
git clone --depth=1 https://github.com/large/repo
# Downloads only recent commits; faster for CI
```

**49. Signed commits for verification.**
```bash
git commit -S -m "Important change"
# Cryptographically signs commit; proves authorship
```

**50. Sparse checkout: download subset of large repo.**
```bash
git sparse-checkout set src/ tests/
# Only these directories downloaded
```

**51. Git LFS for large files.**
```bash
git lfs install
git lfs track "*.bin"
git add large_file.bin
# Pointer stored in Git; actual file in Git LFS server
```

**52. Bisect with script (automate).**
```bash
git bisect start HEAD v1.0
git bisect run npm test
# Automatically runs script on each bisect candidate
```

**53. Rebase with interactive and autosquash.**
```bash
git commit -m "fixup! Add feature"  # Auto-squashed into target
git rebase -i --autosquash HEAD~5
```

**54. Multiple remotes (mirror, upstream).**
```bash
git remote add upstream https://github.com/original/repo
git remote add mirror https://github.com/mirror/repo
git fetch upstream
git push mirror main:main
```

**55. Clean up local branches after PR merge.**
```bash
git fetch origin --prune          # Remove remote tracking branches
git branch -vv                    # Show tracking status
git branch -d merged_feature      # Delete local merged branches
```

**56. Merge strategies: recursive, ours, theirs.**
Default (recursive) tries 3-way merge. `--strategy=ours` prefers current branch changes (dangerous).

**57. Rerere: reuse recorded resolutions.**
```bash
git config rerere.enabled true
# Git remembers merge conflict resolutions; auto-applies on similar conflicts
```

**58. Export commits to patch files.**
```bash
git format-patch origin/main -o patches/
# Creates .patch files; can email or apply to other repo
git am patches/*.patch             # Apply patches
```

**59. Amend without changing timestamp.**
```bash
GIT_COMMITTER_DATE="$(git log -1 --format=%cD)" \
  git commit --amend --no-edit --date=format:"$(git log -1 --format=%aD)"
```

**60. Recovery: find lost commits across all branches.**
```bash
git reflog
git fsck --lost-found              # Finds dangling objects
git show <sha>
# Reconstruct lost work from dangling objects
```

---

## 10. Common Mistakes

- **Force-push to shared branches**: Destroys others' commits. Communicate first.
- **Committing credentials**: Use `.env`, rotate immediately.
- **Large binaries**: Bloats repo. Use Git LFS.
- **Merging without testing**: Test locally before merge.
- **Unclear commit messages**: Makes history hard to understand.
- **Rebasing shared branches**: Rewrite public history carefully.
- **Not pulling before push**: Causes rejection. Always sync first.
- **Ignoring .gitignore**: Commits build artifacts, dependencies.
- **Merge commits on PR**: Use squash for clean history.
- **Detached HEAD surprises**: Understand HEAD state.

---

## 11. Comparison: Git vs Other VCS

| Feature | Git | SVN | Mercurial |
|---------|-----|-----|-----------|
| **Type** | Distributed | Centralized | Distributed |
| **Speed** | Fast (local) | Slow (server calls) | Fast (local) |
| **Offline** | Full functionality | Limited | Full functionality |
| **Learning** | Steep | Gentle | Moderate |
| **Industry** | Dominant (GitHub) | Legacy | Niche |
| **Branching** | Lightweight | Expensive | Lightweight |
| **History** | Rewritable | Immutable | Rewritable |

---

## 12. Practical Projects

- **Beginner**: Local repo, push to GitHub, create README.
- **Intermediate**: Collaborative repo with PRs, code review, CI/CD integration.
- **Advanced**: Open-source contribution (fork, feature, PR); manage release workflow.

---

## 13. Internship Preparation

- **Resume**: Highlight collaborative projects, meaningful commit messages.
- **Expectations**: Clean branching strategy, responsive to code review.
- **Interview focus**: Merge conflicts, branching strategy, collaborative workflows.
- **Coding rounds**: Demonstrate Git understanding through clean commits.

---

## 14. Cheat Sheet

| Command | Purpose |
|---------|---------|
| `git init` | Create repo |
| `git clone <url>` | Copy remote repo |
| `git add <file>` | Stage changes |
| `git commit -m "msg"` | Create commit |
| `git push` | Upload to remote |
| `git pull` | Download + merge |
| `git branch` | List/create branches |
| `git checkout <branch>` | Switch branch |
| `git merge <branch>` | Merge branch |
| `git rebase <branch>` | Replay commits |
| `git status` | View state |
| `git log` | View history |
| `git stash` | Save changes |
| `git reset` | Undo commits |
| `git revert` | Undo safely |

---

## 15. One-Day Revision Checklist

- [ ] Explain Git's distributed model.
- [ ] Describe commit, branch, merge.
- [ ] Walk through PR workflow.
- [ ] Resolve merge conflict (< 5 min).
- [ ] Explain rebase vs merge use cases.
- [ ] Recover lost commits with reflog.
- [ ] Design branching strategy (feature/main/develop).
- [ ] Understand HEAD states (attached vs detached).
- [ ] Use `git stash` for context switching.
- [ ] Explain when to use cherry-pick.
- [ ] List best practices for commit messages.
- [ ] Solve two Git interview problems.
