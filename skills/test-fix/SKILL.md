---
name: test-fix
description: Diagnose failing tests from their error output before changing implementation code.
---

# Test Fix

Use this skill when tests fail or the user asks to fix a failing suite.

Workflow:
- read the exact failure and traceback
- identify the smallest failing behavior
- add or adjust a focused regression test when useful
- change the implementation only after the failure is understood
- rerun the targeted test, then the broader suite
