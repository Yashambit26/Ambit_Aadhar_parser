# CLAUDE.md

## Coding Principles

Write code that is **simple, efficient, clean, and maintainable**.

### 1. Keep Code Simple

* Prefer the simplest solution that correctly solves the problem.
* Do not over-engineer.
* Avoid unnecessary abstractions, classes, functions, wrappers, or design patterns.
* Do not create code "just in case" it may be needed later.
* Use straightforward and readable logic.

### 2. Avoid Unnecessary Code

* Do not add code that is not required for the current task.
* Do not create unnecessary helper functions.
* Do not duplicate logic.
* Do not add unnecessary comments or documentation.
* Do not add unnecessary configuration files or dependencies.
* Do not modify unrelated files.

### 3. Optimize for Efficiency

* Write efficient code with reasonable time and memory complexity.
* Avoid unnecessary loops, API calls, database queries, file reads/writes, and network requests.
* Reuse existing data and functions where appropriate.
* Avoid repeatedly performing expensive operations.
* For large datasets, prefer streaming, batching, pagination, or chunking where appropriate.
* Do not optimize prematurely when it makes the code significantly harder to understand.

### 4. Reuse Existing Code

Before creating something new:

* Check whether the project already has a function, utility, class, or module that solves the problem.
* Reuse existing project patterns and utilities when appropriate.
* Do not create duplicate implementations of existing functionality.

### 5. Minimal Changes

When modifying existing code:

* Make the smallest change necessary to solve the problem.
* Preserve existing working behavior unless the task explicitly requires changing it.
* Do not refactor unrelated code.
* Do not rename variables, functions, or files unnecessarily.
* Do not rewrite an entire file when a small change is sufficient.

### 6. Dependencies

* Do not introduce a new dependency unless it provides a clear benefit.
* Prefer the standard library and existing project dependencies when possible.
* If a dependency is necessary, explain why it is needed.

### 7. Error Handling

* Handle errors that are realistically possible and important.
* Do not add excessive defensive programming.
* Avoid catching exceptions without a good reason.
* Never silently ignore errors.

### 8. Comments

* Write comments only when they explain **why** something is done.
* Do not comment obvious code.
* Do not add long explanations inside the code unless genuinely necessary.

### 9. Performance

When writing performance-sensitive code:

* Consider CPU, memory, I/O, API, database, and network costs.
* Avoid unnecessary data copying.
* Avoid loading large files or datasets entirely into memory when it is not necessary.
* Prefer batch operations over repeated individual operations when appropriate.
* Avoid unnecessary serialization/deserialization.

### 10. Code Quality

Code should be:

* Simple
* Readable
* Efficient
* Maintainable
* Testable
* Consistent with the existing project

Avoid:

* Over-engineering
* Premature optimization
* Duplicate code
* Dead code
* Unused variables/imports
* Unnecessary abstractions
* Unnecessary dependencies
* Excessive comments
* Excessive logging
* Magic values when a clear constant/configuration is appropriate

## Before Writing Code

First inspect the existing code and understand:

1. How the project is structured.
2. Existing utilities and reusable functions.
3. Existing coding patterns.
4. Existing dependencies.
5. The smallest change required to solve the task.

Do not immediately create new files or abstractions.

## Before Finishing

Verify that:

* The implementation solves the requested problem.
* No unnecessary code was added.
* No unnecessary dependencies were introduced.
* Existing functionality was not unnecessarily changed.
* There are no unused imports, variables, functions, or files.
* The implementation is reasonably efficient.
* Tests are added or updated when appropriate.

## Golden Rule

**Do the simplest thing that works.**

If a solution can be implemented with 20 lines instead of 100, prefer the 20-line solution when it remains clear and maintainable.

**Do not write code just because you can. Write only the code that is needed.**
