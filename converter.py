import pandas as pd
import markdownify 

def convert_html_to_markdown(filename, column_name):
    # Load the data from the CSV file
    df = pd.read_csv(filename)
    
    # Ensure the column is treated as a string and handle NaN values
    df[column_name] = df[column_name].fillna('').astype(str)
    
    # Convert HTML content to Markdown for each row
    for index, row in df.iterrows():
        html_content = row[column_name]
        markdown_content = markdownify.markdownify(html_content)
        df.at[index, column_name] = markdown_content
    
    # Save the updated DataFrame back to the CSV file
    df.to_csv(filename, index=False)

# Example usage:
convert_html_to_markdown('./data/complaints.csv', 'Complaint Description')
convert_html_to_markdown('./data/complaints.csv', 'CheckList')
convert_html_to_markdown('./data/complaints.csv', 'RequiredQuestions')
convert_html_to_markdown('./data/complaints.csv', 'ImportantPoints')
convert_html_to_markdown('./data/complaints.csv', 'FAQs')
convert_html_to_markdown('./data/complaints.csv', 'Scenario1')
convert_html_to_markdown('./data/complaints.csv', 'Scenario2')
convert_html_to_markdown('./data/complaints.csv', 'Scenario3')
convert_html_to_markdown('./data/complaints.csv', 'Scenario4')
convert_html_to_markdown('./data/complaints.csv', 'Scenario5')
