
---

## Setup commands

```bash
# 1. Create the repository root
mkdir -p pes-online-evolution && cd pes-online-evolution
git init -b main

# 2. Create the Phase 1 directory skeleton
mkdir -p apps packages infra docs/adr tools .github/workflows
touch apps/.gitkeep packages/.gitkeep infra/.gitkeep

# 3. Create every file above with its exact content:
#    README.md, CHANGELOG.md, .gitignore, .editorconfig, .gitattributes,
#    .env.example, docker-compose.yml, Makefile,
#    docs/architecture.md, docs/folder-structure.md, docs/domain-model.md,
#    docs/api-surface.md, docs/phase-plan.md,
#    docs/adr/0001-mon orepo-layout.md,
#    docs/adr/0002-backend-stack.md,
#    docs/adr/0003-realtime-and-match-lifecycle.md,
#    docs/adr/0004-companion-trust-model.md,
#    tools/check_architecture.py,
#    .github/workflows/ci.yml

# 4. Make the checker executable
chmod +x tools/check_architecture.py

# 5. Prepare environment and start PostgreSQL
make env
make up

# 6. Validate everything
make verify