from extract import extract_all
from transform import transform_all
from load import load_all
from report import generate_quality_report

def run_pipeline():
    print("\n=======================")
    print("           SHOPPULSE ETL PIPELINE")
    print("========================")

    print("\n[1/4] Extracting data....")

    datasets = extract_all()

    print("Extraction Completed!")

    print("\n[2/4] Transforming data....")

    transformed_data,rejected_data = transform_all(datasets)

    print("Transformation Completed!")

    print("\n[3/4] Loading data....")

    load_all(transformed_data,rejected_data)

    print("Loading Completed!")

    print("\n[4/4] Generating quality report....")

    generate_quality_report()

    print("\n====================")
    print("        SHOPPULSE ETL COMPLETED!")
    print("=======================")


if __name__ == "__main__":
    run_pipeline()
