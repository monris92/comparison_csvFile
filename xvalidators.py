import csv

def compare_csv(downloaded_csv, local_csv_file, validations):
    # Open the local CSV file and read it into memory
    with open(local_csv_file, newline='', encoding='utf-8') as file:
        local_csv_reader = csv.reader(file)
        local_csv = list(local_csv_reader)

    # Perform validations
    for (row_index, col_index), expected_value in validations.items():
        # Adjust indices if your CSV has headers
        if local_csv[row_index][col_index] != expected_value:
            print(f"Validation failed at row {row_index + 1}, column {col_index + 1}. "
                  f"Expected: {expected_value}, Found: {local_csv[row_index][col_index]}")
            return False
    print("All validations passed.")
    return True