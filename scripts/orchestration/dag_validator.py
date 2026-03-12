import sys
from airflow.models import DagBag

def validate_dags():
    """
    Parses all DAGs in the dags folder and checks for import errors.
    """
    dagbag = DagBag(dag_folder='/opt/airflow/dags', include_examples=False)
    
    if dagbag.import_errors:
        print(f"FAILED: Found {len(dagbag.import_errors)} import errors:")
        for filename, error in dagbag.import_errors.items():
            print(f"- {filename}: {error}")
        sys.exit(1)
    
    print(f"SUCCESS: {len(dagbag.dags)} DAGs parsed successfully.")
    for dag_id in dagbag.dag_ids:
        print(f"  - {dag_id}")
    sys.exit(0)

if __name__ == "__main__":
    validate_dags()
