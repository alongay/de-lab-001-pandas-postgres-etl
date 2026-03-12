import pandas as pd
import os
import json

class SchemaGuard:
    """
    Detects changes in table structure (columns, types) across data runs.
    """
    def __init__(self, schema_dir="data/observability/schemas"):
        self.schema_dir = schema_dir
        os.makedirs(self.schema_dir, exist_ok=True)

    def _get_schema_fingerprint(self, df):
        """
        Returns a dictionary representing the dataframe's schema.
        """
        return {col: str(dtype) for col, dtype in df.dtypes.items()}

    def check_schema(self, df, domain):
        """
        Compares current schema against the last known good (LKG) schema.
        """
        fingerprint_path = os.path.join(self.schema_dir, f"{domain}_schema.json")
        current_schema = self._get_schema_fingerprint(df)

        if not os.path.exists(fingerprint_path):
            print(f"No schema baseline for {domain}. Initializing LKG.")
            with open(fingerprint_path, 'w') as f:
                json.dump(current_schema, f)
            return {"status": "INITIALIZED", "changes": []}

        with open(fingerprint_path, 'r') as f:
            lkg_schema = json.load(f)

        changes = []
        # Check for removed columns
        for col in lkg_schema:
            if col not in current_schema:
                changes.append({"type": "COLUMN_REMOVED", "column": col})
        
        # Check for added columns or type shifts
        for col, dtype in current_schema.items():
            if col not in lkg_schema:
                changes.append({"type": "COLUMN_ADDED", "column": col})
            elif lkg_schema[col] != dtype:
                changes.append({
                    "type": "TYPE_SHIFT", 
                    "column": col, 
                    "old": lkg_schema[col], 
                    "new": dtype
                })

        if not changes:
            return {"status": "SUCCESS", "changes": []}
        else:
            print(f"Schema breach detected in {domain}: {changes}")
            return {"status": "BREACH", "changes": changes}

    def update_lkg(self, df, domain):
        """
        Updates the LKG schema after an intentional change.
        """
        fingerprint_path = os.path.join(self.schema_dir, f"{domain}_schema.json")
        current_schema = self._get_schema_fingerprint(df)
        with open(fingerprint_path, 'w') as f:
            json.dump(current_schema, f)
        print(f"Updated LKG schema for {domain}.")

if __name__ == "__main__":
    # Smoke test
    guard = SchemaGuard()
    df1 = pd.DataFrame({'a': [1], 'b': ['text']})
    
    # Initialize
    guard.check_schema(df1, "test_table")
    
    # Test change
    df2 = pd.DataFrame({'a': [1], 'c': [1.5]}) # b removed, c added
    result = guard.check_schema(df2, "test_table")
    print(f"Schema check result: {result}")
