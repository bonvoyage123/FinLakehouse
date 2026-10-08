from src.ingestion.fmp_ingestion import ingest_fmp_data


def main():
    uploaded_keys = ingest_fmp_data()
    print(f"Uploaded {len(uploaded_keys)} raw files to S3.")


if __name__ == "__main__":
    main()
