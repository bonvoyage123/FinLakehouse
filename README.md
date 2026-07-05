# FinLakehouse
Build a production-style Financial Lakehouse that ingests stock market
and company financial data, processes it using a Medallion Architecture,
models business-ready datasets, orchestrates the pipeline, and exposes
analytics dashboards.

## Security and Vulnerability Checks

This project uses a comprehensive GitHub Actions workflow to automatically scan for security vulnerabilities on every pull request. This provides a robust security gate and gives clear, actionable feedback directly within pull requests.

The workflow (`.github/workflows/security.yml`) combines three powerful security tools:

*   **Trivy**: Scans the filesystem for known vulnerabilities in OS packages, application dependencies, and infrastructure-as-code configurations. The build will fail if any `CRITICAL` severity vulnerabilities are found.
*   **Bandit**: Performs static code analysis on the Python codebase to find common security issues like hardcoded secrets, SQL injection risks, and unsafe deserialization.
*   **Safety**: Checks the Python dependencies listed in `requirements.txt` against a database of known security vulnerabilities.

### Key Features of the Workflow:

*   **Unified Job**: Consolidates all security checks into a single, cohesive job named `security-scan`.
*   **Integrated Reporting**: All tools output their findings in the SARIF format. The results are then uploaded to GitHub's Security tab, providing a single, integrated view for triaging and managing vulnerabilities.
*   **Non-Blocking Review**: For Bandit and Safety, the workflow is configured with `continue-on-error: true`. This ensures that even if low or medium-severity issues are found, the results are still uploaded for review without immediately blocking the pull request.