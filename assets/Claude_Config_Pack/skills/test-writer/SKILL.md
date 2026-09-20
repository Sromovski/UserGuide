---
name: test-writer
description: Writes tests that match this repository's existing test conventions. Use when the user asks for tests, says code is untested, asks to reproduce a bug with a test, or asks to raise coverage.
---

# Test writer

Writes tests that look like they were written by whoever wrote the existing suite.

## Steps

1. **Read the neighbours first.** Find 2-3 existing test files near the code under test.
   Copy their framework, imports, naming, setup/teardown and assertion style.
2. Identify what the code under test actually promises: inputs, outputs, side effects,
   and the errors it is documented to raise.
3. Write tests in this order: happy path, boundaries, error cases, then regressions.
4. Run them. Paste the real output.

## Coverage checklist

- [ ] The normal case with realistic data
- [ ] Empty / zero / null input
- [ ] The boundary on each numeric or length limit
- [ ] Each error branch the code can take
- [ ] Anything async: rejection and timeout
- [ ] The specific bug, if this is a regression test

## Rules

- Match the existing suite's conventions over any preference of your own.
- One behaviour per test. A test name should read as a sentence about that behaviour.
- No assertions on internal implementation detail — test the contract.
- Never mock the thing under test. Mock its collaborators only.
- If a test needs a comment to explain what it does, rename the test instead.
- If reproducing a bug: the test must FAIL first. Show that, then fix the code.
