# Handling Multiple GitHub Accounts (gh CLI)

If you use one machine for both enterprise work (e.g., `AISavantGH`) and personal studies (e.g., `alongay`), you might encounter authentication errors when trying to push or create repositories across profiles.

Example Error:
```text
GraphQL: AISavantGH cannot create a repository for alongay. (createRepository)
```

The elegant, enterprise-level solution is to use the GitHub CLI (`gh`) multi-account switching feature, rather than manually juggling SSH keys.

## Step 1: Add your second account

Run the interactive log-in command from your terminal:
```powershell
gh auth login
```

Follow the interactive prompts exactly as shown below:
```text
? Where do you use GitHub? GitHub.com
? What is your preferred protocol for Git operations on this host? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser

! First copy your one-time code: 0296-0498
Press Enter to open https://github.com/login/device in your browser... 
✓ Authentication complete.
- gh config set -h github.com git_protocol https
✓ Configured git protocol
✓ Logged in as alongay
```

## Step 2: Switch active accounts

The GitHub CLI now remembers both identities. Whenever you want to operate under your study account (`alongay`), instruct the CLI to switch contexts:

```powershell
gh auth switch -u alongay
```

Expected Output:
```text
✓ Switched active account for github.com to alongay
```

*(When you need to return to your primary application-building account, simply run `gh auth switch -u AISavantGH`)*

## Step 3: Execute repository commands

Now that you are correctly authenticated as your study profile, remote creation and push commands will succeed gracefully:

```powershell
gh repo create alongay/de-lab-001-pandas-postgres-etl --public --source=. --remote=origin --push
```
