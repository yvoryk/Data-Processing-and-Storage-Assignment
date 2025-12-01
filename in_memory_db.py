"""
In-Memory Key-Value Database with Transaction Support
Data Processing and Storage Assignment
"""


class InMemoryDB:
    """
    An in-memory key-value database that supports transactions.
    
    Keys are strings and values are integers.
    Transactions provide "all or nothing" updates - changes made within
    a transaction are only visible after commit(), and can be undone with rollback().
    """

    def __init__(self):
        # Main database storage - this is the "committed" state
        self._main_store = {}
        
        # Transaction storage - holds uncommitted changes
        self._transaction_store = None
        
        # Flag to track if a transaction is currently active
        self._in_transaction = False

    def get(self, key: str):
        """
        Returns the value associated with the key, or None if the key doesn't exist.
        
        This method can be called anytime, even when a transaction is not in progress.
        Note: Changes made within an ongoing transaction are NOT visible until commit().
        
        Args:
            key: The string key to look up
            
        Returns:
            The integer value associated with the key, or None if key doesn't exist
        """
        # Always read from main store - transaction changes aren't visible until commit
        return self._main_store.get(key, None)

    def put(self, key: str, val: int):
        """
        Creates a new key with the provided value if key doesn't exist,
        otherwise updates the value of an existing key.
        
        This method can ONLY be called when a transaction is in progress.
        
        Args:
            key: The string key to create/update
            val: The integer value to set
            
        Raises:
            Exception: If no transaction is currently in progress
        """
        if not self._in_transaction:
            raise Exception("No transaction in progress - cannot call put() outside of a transaction")
        
        # Store the change in our transaction store
        self._transaction_store[key] = val

    def begin_transaction(self):
        """
        Starts a new transaction.
        
        Only one transaction can exist at a time. All put() operations
        after this call will be part of this transaction until commit() or rollback().
        
        Raises:
            Exception: If a transaction is already in progress
        """
        if self._in_transaction:
            raise Exception("Transaction already in progress - only one transaction allowed at a time")
        
        self._in_transaction = True
        self._transaction_store = {}

    def commit(self):
        """
        Applies all changes made within the transaction to the main state.
        
        After commit, all changes become visible to future get() calls.
        The transaction ends after this call.
        
        Raises:
            Exception: If no transaction is currently in progress
        """
        if not self._in_transaction:
            raise Exception("No transaction in progress - cannot commit")
        
        # Apply all changes from transaction store to main store
        for key, value in self._transaction_store.items():
            self._main_store[key] = value
        
        # End the transaction
        self._in_transaction = False
        self._transaction_store = None

    def rollback(self):
        """
        Aborts all changes made within the transaction.
        
        Everything goes back to the way it was before the transaction started.
        The transaction ends after this call.
        
        Raises:
            Exception: If no transaction is currently in progress
        """
        if not self._in_transaction:
            raise Exception("No transaction in progress - cannot rollback")
        
        # Simply discard the transaction store - don't apply anything
        self._in_transaction = False
        self._transaction_store = None


def main():
    """
    Demonstrates the InMemoryDB functionality with the examples from the assignment.
    """
    print("=" * 60)
    print("In-Memory Database with Transaction Support - Demo")
    print("=" * 60)
    
    inmemoryDB = InMemoryDB()
    
    # Test 1: get() on non-existent key
    print("\n--- Test 1: Get non-existent key ---")
    result = inmemoryDB.get("A")
    print(f"inmemoryDB.get('A') = {result}")
    print("Expected: None (A doesn't exist yet)")
    
    # Test 2: put() without transaction should throw error
    print("\n--- Test 2: Put without transaction ---")
    try:
        inmemoryDB.put("A", 5)
        print("ERROR: Should have thrown an exception!")
    except Exception as e:
        print(f"Caught expected exception: {e}")
    
    # Test 3: Start transaction and make changes
    print("\n--- Test 3: Transaction with commit ---")
    inmemoryDB.begin_transaction()
    print("Started new transaction")
    
    inmemoryDB.put("A", 5)
    print("Set A = 5 (not committed yet)")
    
    result = inmemoryDB.get("A")
    print(f"inmemoryDB.get('A') = {result}")
    print("Expected: None (changes not committed yet)")
    
    inmemoryDB.put("A", 6)
    print("Updated A = 6 (still not committed)")
    
    inmemoryDB.commit()
    print("Committed transaction")
    
    result = inmemoryDB.get("A")
    print(f"inmemoryDB.get('A') = {result}")
    print("Expected: 6 (last committed value)")
    
    # Test 4: commit() without transaction should throw error
    print("\n--- Test 4: Commit without transaction ---")
    try:
        inmemoryDB.commit()
        print("ERROR: Should have thrown an exception!")
    except Exception as e:
        print(f"Caught expected exception: {e}")
    
    # Test 5: rollback() without transaction should throw error
    print("\n--- Test 5: Rollback without transaction ---")
    try:
        inmemoryDB.rollback()
        print("ERROR: Should have thrown an exception!")
    except Exception as e:
        print(f"Caught expected exception: {e}")
    
    # Test 6: get() on another non-existent key
    print("\n--- Test 6: Get another non-existent key ---")
    result = inmemoryDB.get("B")
    print(f"inmemoryDB.get('B') = {result}")
    print("Expected: None (B doesn't exist)")
    
    # Test 7: Transaction with rollback
    print("\n--- Test 7: Transaction with rollback ---")
    inmemoryDB.begin_transaction()
    print("Started new transaction")
    
    inmemoryDB.put("B", 10)
    print("Set B = 10 (not committed)")
    
    inmemoryDB.rollback()
    print("Rolled back transaction")
    
    result = inmemoryDB.get("B")
    print(f"inmemoryDB.get('B') = {result}")
    print("Expected: None (changes were rolled back)")
    
    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

