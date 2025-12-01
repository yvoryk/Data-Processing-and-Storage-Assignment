# Data Processing and Storage Assignment

An in-memory key-value database with transaction support, built in Python.

## Overview

This project implements an in-memory database that supports transactions with "all or nothing" semantics. This is important for things like banking apps where you can't have money disappear into thin air if something fails mid-transfer!

### Features

- **Key-Value Storage**: Keys are strings, values are integers
- **Transaction Support**: Begin, commit, and rollback transactions
- **Isolation**: Changes within a transaction aren't visible until committed
- **Error Handling**: Proper exceptions when operations are called incorrectly

## How to Run the Code

### Prerequisites

- Python 3.6 or higher (should already be installed on most systems)
- No external dependencies required!

### Setup & Running

1. **Clone or download this repository** to your local machine

2. **Open a terminal/command prompt** and navigate to the project folder:
   ```bash
   cd Data-Processing-and-Storage-Assignment
   ```

3. **Run the main file** to see the demo:
   ```bash
   python in_memory_db.py
   ```

That's it! The script will run through all the test cases from the assignment and show you the expected vs actual output.

### Using the Database in Your Own Code

```python
from in_memory_db import InMemoryDB

# Create a new database instance
db = InMemoryDB()

# Start a transaction before making changes
db.begin_transaction()

# Make your changes
db.put("balance", 100)
db.put("savings", 500)

# Commit to save changes (or rollback() to discard them)
db.commit()

# Now you can read the values
print(db.get("balance"))  # Output: 100
```

## Making This an Official Assignment

To formalize this homework, I'd spell out that `get()` must ignore uncommitted writes so graders can check for that isolation rule. I'd also require a few unit tests that exercise edge cases like double `begin_transaction()` calls or repeated rollbacks, and maybe add an optional `delete()` method so students wrestle with state removal. The grading rubric could then reward both passing an automated test suite and clear docstrings/readme updates, which makes evaluation consistent even in large classes. Finally, I'd remind students to include a quick complexity note or trade-off discussion so they articulate why an in-memory approach is acceptable here.