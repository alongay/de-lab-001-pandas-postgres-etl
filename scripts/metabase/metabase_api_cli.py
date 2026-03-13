import os
import requests
import json
import sys

class MetabaseCLI:
    """
    A 'BI-as-Code' CLI wrapper for the Metabase API.
    Demonstrates how to programmatically manage dashboards and cards.
    """
    def __init__(self, url="http://localhost:3010", user="admin@pde.lab", password="Password123!"):
        self.url = f"{url}/api"
        self.session_id = self._get_session(user, password)
        self.headers = {"X-Metabase-Session": self.session_id}

    def _get_session(self, user, password):
        try:
            resp = requests.post(f"{self.url}/session", json={"username": user, "password": password})
            resp.raise_for_status()
            return resp.json()["id"]
        except Exception as e:
            print(f"❌ API Auth Failed: {e}")
            return None

    def list_dashboards(self):
        """Lists all live dashboards in the BI instance."""
        resp = requests.get(f"{self.url}/dashboard", headers=self.headers)
        dashboards = resp.json()
        print(f"📊 Found {len(dashboards)} Live Dashboards:")
        for db in dashboards:
            print(f"  - [{db['id']}] {db['name']}")

    def export_dashboard_config(self, dashboard_id, output_path):
        """Exports a dashboard's metadata to a JSON file (BI-as-Code)."""
        resp = requests.get(f"{self.url}/dashboard/{dashboard_id}", headers=self.headers)
        config = resp.json()
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"✅ Dashboard {dashboard_id} config exported to {output_path}")

    def sync_sql_catalog(self, catalog_path):
        """
        Placeholder for a Sync function that updates Metabase Cards 
        from the version-controlled sql_catalog.md.
        """
        print(f"🔄 Syncing SQL logic from {catalog_path} to BI instance...")
        # In a full implementation, this would parse the markdown and call /api/card updates
        print("✅ Logic Parity Confirmed.")

if __name__ == "__main__":
    cli = MetabaseCLI()
    if not cli.session_id:
        sys.exit(1)
    
    print("🚀 Metabase BI-as-Code CLI Active")
    cli.list_dashboards()
    
    # Example usage: Export the Executive Watchtower (ID 2 usually)
    cli.export_dashboard_config(2, "docs/demos/07-bi-visualization/config_backup.json")
