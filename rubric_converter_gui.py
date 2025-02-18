import json
import csv

def convert_rubric_to_csv(input_json_path, output_path, use_name_and_value=False):
    with open(input_json_path, 'r') as file:
        rubric_data = json.load(file)
    
    # Get scale headers
    rubric_scale_section = rubric_data['RubricScale']
    column_headers = ['Criteria']
    for scale in rubric_scale_section:
        column_headers.append(scale['name'])
    
    # Process criteria
    rubric_criterion_section = rubric_data['RubricCriterion']
    rows = []
    for criterion in rubric_criterion_section:
        if use_name_and_value:
            row = [f"{criterion['name']} ({criterion['value']})"]
        else:
            row = [criterion['description']]
        row.extend([''] * (len(column_headers) - 1))
        rows.append(row)
        
    # Map criteria to scales
    rubric_criterion_scale_section = rubric_data['RubricCriterionScale']
    criterion_id_to_row_index = {criterion['id']: index for index, criterion in enumerate(rubric_criterion_section)}
    scale_value_id_to_column_index = {scale['id']: index + 1 for index, scale in enumerate(rubric_scale_section)}
    
    for entry in rubric_criterion_scale_section:
        row_index = criterion_id_to_row_index[entry['criterion']]
        column_index = scale_value_id_to_column_index[entry['scale_value']]
        rows[row_index][column_index] = entry['description']
    
    # Write to CSV
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_headers)
        writer.writerows(rows)
    
    print(f"File has been successfully saved at: {output_path}")

if __name__ == "__main__":
    # Hardcoded paths - modify these as needed
    INPUT_PATH = "input.rbc"  # Change this to your input file path
    OUTPUT_PATH = "output.csv"  # Change this to your desired output file path
    USE_NAME_AND_VALUE = False  # Set to True if you want to use name+value instead of description
    
    convert_rubric_to_csv(INPUT_PATH, OUTPUT_PATH, USE_NAME_AND_VALUE)
