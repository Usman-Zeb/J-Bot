import pandas as pd
import string

def remove_unsupported(text):
    if isinstance(text, str):
        # Define a set of supported characters (ASCII printable characters)
        supported_chars = set(string.printable)
        # Return only supported characters for strings
        return ''.join(char for char in text if char in supported_chars)
    else:
        # Return the integer unchanged
        return text

def remove_unsupported_chars(input_filename, output_filename):
    # Read the CSV file
    df = pd.read_csv(input_filename)
    
    # Apply the function to each cell in the DataFrame
    df = df.applymap(remove_unsupported)
    
    # Save the cleaned DataFrame to a new CSV file
    df.to_csv(output_filename, index=False)

# Example usage:
remove_unsupported_chars('./data/complaints.csv', './data/cleaned_output.csv')
