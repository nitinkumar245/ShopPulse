from pathlib import Path
import pandas as pd

PROJECT_ROOT=Path(__file__).resolve().parents[1]

PROCESSED_DIR=PROJECT_ROOT/"data"/"processed"
REJECTED_DIR=PROJECT_ROOT/"data"/"rejected"
REPORT_DIR=PROJECT_ROOT/"data"/"reports"

def generate_quality_report():
    REPORT_DIR.mkdir(parents=True,exist_ok=True)

    report_data=[]

    processed_files = list(PROCESSED_DIR.glob("*.csv"))

    for file in processed_files:

        dataset_name = file.stem

        processed_df = pd.read_csv(file)

        rejected_file = REJECTED_DIR/f"{dataset_name}_rejected.csv"

        if rejected_file.exists():
            rejected_df = pd.read_csv(rejected_file)
        else:
            rejected_df=pd.DataFrame()

        total_processed=len(processed_df)
        total_rejected = len(rejected_df)

        report_data.append({
            "Dataset":dataset_name,
            "Processed Records": total_processed,
            "Rejected Records":total_rejected,
            "Total Records":total_processed + total_rejected
        })      

        report_df = pd.DataFrame(report_data)

        report_path=REPORT_DIR/"data_quality_report.csv"

        report_df.to_csv(report_path,index=False)

        print("\n=========== DATA QUALITY REPORT =============")

        print(report_df.to_string(index=False))

        print("\nTotal Processed:",report_df["Processed Records"].sum())

        print("Total Rejected:",report_df["Rejected Records"].sum())

        print(f"\nReport Saved at: {report_path}")


if __name__ == "__main__":
    generate_quality_report()