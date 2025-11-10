from trino.dbapi import connect
from trino.auth import OAuth2Authentication

class TrinoClient:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.auth = None

    def __enter__(self):
        print("Initializing Trino client...")
        
        print("Authenticating...")
        self.conn = connect(
            host="trino.doordash.team",
            port=443,
            user="lingfei.li@doordash.com",
            auth=OAuth2Authentication(),
            http_scheme="https",
        )
        self.cur = self.conn.cursor()
        print("Connection established")
        
        return self  # Return the instance itself to be used within the 'with' block

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection...")
        self.conn.close()
        print("Connection closed")

        # Returning False (or nothing) will propagate any exceptions
        # that occurred within the 'with' block.
        # Returning True would suppress them.
        return False

    def execute_query(self, query):
        print("Executing query:\n", query)
        self.cur.execute(query)
        
        # Get column names from cursor description
        columns = [desc[0] for desc in self.cur.description] if self.cur.description else []
        
        # Fetch all results
        rows = self.cur.fetchall()
        
        # Convert to list of dictionaries for easier handling
        results = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            results.append(row_dict)
        
        print(f"Query result: {len(results)} rows returned")
        return results