from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os
import json

class DataDriftDetector:
    """
    Detects statistical drift between a current dataset and a baseline.
    """
    def __init__(self, baseline_dir="data/observability/baselines"):
        self.baseline_dir = baseline_dir
        os.makedirs(self.baseline_dir, exist_ok=True)

    def save_baseline(self, df, domain, column_names):
        """
        Calculates and persists a baseline distribution for a list of columns.
        """
        baseline_data = {}
        for col in column_names:
            if col in df.columns:
                # Store as a list of values (or a sample if too large)
                sample = df[col].dropna().tolist()
                # Ensure native types for JSON serialization
                sample = [float(x) for x in sample]
                if len(sample) > 1000:
                    sample = np.random.choice(sample, 1000, replace=False).tolist()
                baseline_data[col] = sample
        
        baseline_path = os.path.join(self.baseline_dir, f"{domain}_baseline.json")
        with open(baseline_path, 'w') as f:
            json.dump(baseline_data, f)
        print(f"Saved baseline for {domain} to {baseline_path}")

    def detect_drift(self, df, domain, column_names, threshold=0.05):
        """
        Compares current dataframe columns against the saved baseline using KS-test.
        Returns a dictionary of results per column.
        """
        baseline_path = os.path.join(self.baseline_dir, f"{domain}_baseline.json")
        if not os.path.exists(baseline_path):
            print(f"No baseline found for {domain}. Current data will be the NEW baseline.")
            self.save_baseline(df, domain, column_names)
            return {}

        with open(baseline_path, 'r') as f:
            baseline_data = json.load(f)

        reports = []
        for col in column_names:
            if col not in df.columns or col not in baseline_data:
                continue

            current_sample = df[col].dropna().values
            baseline_sample = np.array(baseline_data[col])

            # KS-Test
            # Null hypothesis: samples come from same distribution
            # Small p-value (< threshold) means we reject the null hypothesis (Drift detected)
            stat, p_val = ks_2samp(current_sample, baseline_sample)
            
            is_drifting = p_val < threshold
            reports.append({
                "column": col,
                "statistic": float(stat),
                "p_value": float(p_val),
                "is_drifting": bool(is_drifting)
            })

        return reports

if __name__ == "__main__":
    # Smoke test
    detector = DataDriftDetector()
    
    # Create synthetic baseline
    d1 = pd.DataFrame({'val': np.random.normal(0, 1, 100)})
    detector.save_baseline(d1, "test_domain", ['val'])
    
    # Test identical distribution (No drift)
    d2 = pd.DataFrame({'val': np.random.normal(0, 1, 100)})
    reports = detector.detect_drift(d2, "test_domain", ['val'])
    print(f"Identical distribution drift report: {reports}")
    
    # Test shifted distribution (Expect drift)
    d3 = pd.DataFrame({'val': np.random.normal(5, 1, 100)})
    reports = detector.detect_drift(d3, "test_domain", ['val'])
    print(f"Shifted distribution drift report: {reports}")
