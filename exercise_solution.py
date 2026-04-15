"""
EXERCISE SOLUTION: Student Support Office Automation
Case Study: Automate checking of student records from CSV file

Requirements:
1. Identify students with marks less than 12
2. Validate email addresses using regex
3. Generate a report.txt file with results
4. Display output in terminal

This solution demonstrates BOTH methods:
- Method 1: Built-in CSV module
- Method 2: Pandas library

Author: [Your Name]
Date: [Current Date]
"""

import csv
import re

# Try to import pandas
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
    print("✓ Pandas library is available")
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠ Pandas not installed. Install with: pip install pandas")
    print("  Will use built-in CSV module only.\n")

def validate_email(email):
    """
    Validate email address using regular expression.
    
    Pattern explanation:
    - ^[a-zA-Z0-9._%+-]+ : Username part (alphanumeric and special chars)
    - @ : Required @ symbol
    - [a-zA-Z0-9.-]+ : Domain name
    - \. : Dot separator
    - [a-zA-Z]{2,}$ : Top-level domain (minimum 2 characters)
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def analyze_student_records_csv(csv_filename):
    """
    METHOD 1: Read and analyze student records using built-in CSV module.
    
    Args:
        csv_filename (str): Path to CSV file
    
    Returns:
        tuple: (underperforming_students, invalid_emails, all_students)
    """
    print("\n" + "=" * 80)
    print("METHOD 1: USING BUILT-IN CSV MODULE")
    print("=" * 80)
    
    underperforming_students = []
    invalid_emails = []
    all_students = []
    
    try:
        with open(csv_filename, "r") as file:
            csv_reader = csv.DictReader(file)
            
            print("Reading CSV file row by row...")
            for row in csv_reader:
                name = row["Name"]
                marks = int(row["Marks"])
                email = row["Email"]
                
                student_data = {
                    "name": name,
                    "marks": marks,
                    "email": email
                }
                all_students.append(student_data)
                
                # Check for underperforming students (marks < 12)
                if marks < 12:
                    underperforming_students.append(student_data)
                
                # Check for invalid email
                if not validate_email(email):
                    invalid_emails.append(student_data)
        
        print(f"✓ Successfully read {len(all_students)} student records using CSV module")
        return underperforming_students, invalid_emails, all_students
    
    except FileNotFoundError:
        print(f"Error: File '{csv_filename}' not found!")
        return [], [], []
    except Exception as e:
        print(f"Error reading file: {e}")
        return [], [], []


def analyze_student_records_pandas(csv_filename):
    """
    METHOD 2: Read and analyze student records using Pandas library.
    
    Args:
        csv_filename (str): Path to CSV file
    
    Returns:
        tuple: (underperforming_students, invalid_emails, all_students)
    """
    print("\n" + "=" * 80)
    print("METHOD 2: USING PANDAS LIBRARY")
    print("=" * 80)
    
    if not PANDAS_AVAILABLE:
        print("⚠ Pandas is not installed. Skipping this method.")
        print("  Install with: pip install pandas\n")
        return [], [], []
    
    try:
        # Read CSV file into DataFrame
        df = pd.read_csv(csv_filename)
        print("\nDataFrame Preview:")
        print(df)
        
        # Pandas-specific statistical analysis
        print("\n--- Pandas Statistical Analysis ---")
        print(f"Total students: {len(df)}")
        print(f"Average marks: {df['Marks'].mean():.2f}")
        print(f"Highest marks: {df['Marks'].max()}")
        print(f"Lowest marks: {df['Marks'].min()}")
        print(f"Standard deviation: {df['Marks'].std():.2f}")
        
        # Filter underperforming students using pandas
        print("\n--- Filtering with Pandas ---")
        underperforming_df = df[df['Marks'] < 12]
        print(f"Underperforming students (Marks < 12):")
        print(underperforming_df)
        
        # Convert DataFrame to list of dictionaries
        all_students = []
        underperforming_students = []
        invalid_emails = []
        
        for index, row in df.iterrows():
            student_data = {
                "name": row["Name"],
                "marks": int(row["Marks"]),
                "email": row["Email"]
            }
            all_students.append(student_data)
            
            # Check for underperforming students
            if row["Marks"] < 12:
                underperforming_students.append(student_data)
            
            # Check for invalid email
            if not validate_email(row["Email"]):
                invalid_emails.append(student_data)
        
        print(f"\n✓ Successfully analyzed {len(all_students)} student records using Pandas")
        return underperforming_students, invalid_emails, all_students
    
    except FileNotFoundError:
        print(f"Error: File '{csv_filename}' not found!")
        return [], [], []
    except Exception as e:
        print(f"Error reading file: {e}")
        return [], [], []

def generate_report(underperforming, invalid_emails, all_students, report_filename, method_name=""):
    """
    Generate a detailed report file with analysis results.
    
    Args:
        underperforming (list): List of underperforming students
        invalid_emails (list): List of students with invalid emails
        all_students (list): List of all students
        report_filename (str): Output report filename
        method_name (str): Name of the method used (optional)
    """
    with open(report_filename, "w") as report:
        report.write("=" * 80 + "\n")
        report.write("STUDENT SUPPORT OFFICE - AUTOMATED ANALYSIS REPORT\n")
        if method_name:
            report.write(f"Method Used: {method_name}\n")
        report.write("=" * 80 + "\n\n")
        
        # Section 1: Underperforming Students
        report.write("SECTION 1: UNDERPERFORMING STUDENTS (Marks < 12)\n")
        report.write("-" * 80 + "\n")
        
        if underperforming:
            report.write(f"Total underperforming students: {len(underperforming)}\n\n")
            for i, student in enumerate(underperforming, 1):
                report.write(f"{i}. Name: {student['name']}\n")
                report.write(f"   Marks: {student['marks']}\n")
                report.write(f"   Email: {student['email']}\n")
                report.write(f"   Status: NEEDS SUPPORT\n\n")
        else:
            report.write("No underperforming students found. All students are doing well!\n\n")
        
        # Section 2: Invalid Email Addresses
        report.write("\nSECTION 2: INVALID EMAIL ADDRESSES\n")
        report.write("-" * 80 + "\n")
        
        if invalid_emails:
            report.write(f"Total invalid emails: {len(invalid_emails)}\n\n")
            for i, student in enumerate(invalid_emails, 1):
                report.write(f"{i}. Name: {student['name']}\n")
                report.write(f"   Invalid Email: {student['email']}\n")
                report.write(f"   Action Required: Contact student to update email\n\n")
        else:
            report.write("All email addresses are valid!\n\n")
        
        # Section 3: Summary and Recommendations
        report.write("\nSECTION 3: SUMMARY AND RECOMMENDATIONS\n")
        report.write("-" * 80 + "\n")
        report.write(f"Total students processed: {len(all_students)}\n")
        report.write(f"Underperforming students: {len(underperforming)}\n")
        report.write(f"Invalid email addresses: {len(invalid_emails)}\n")
        report.write(f"Students in good standing: {len(all_students) - len(underperforming)}\n\n")
        
        report.write("RECOMMENDATIONS:\n")
        if underperforming:
            report.write("1. Schedule individual support sessions for underperforming students\n")
            report.write("2. Provide additional study materials and resources\n")
            report.write("3. Monitor progress weekly\n")
        if invalid_emails:
            report.write("4. Contact students with invalid emails to update records\n")
            report.write("5. Ensure all communication channels are functional\n")
        
        report.write("\n" + "=" * 80 + "\n")
        report.write("End of Report\n")
        report.write("=" * 80 + "\n")

def display_terminal_output(underperforming, invalid_emails, all_students, method_name=""):
    """
    Display formatted output in terminal.
    
    Args:
        underperforming (list): List of underperforming students
        invalid_emails (list): List of students with invalid emails
        all_students (list): List of all students
        method_name (str): Name of the method used (optional)
    """
    print("\n" + "=" * 80)
    if method_name:
        print(f"STUDENT RECORD ANALYSIS - {method_name}")
    else:
        print("STUDENT RECORD ANALYSIS - TERMINAL OUTPUT")
    print("=" * 80 + "\n")
    
    # Display all students
    print("ALL STUDENT RECORDS:")
    print("-" * 80)
    print(f"{'Name':<25} {'Marks':<10} {'Email':<30} {'Status':<15}")
    print("-" * 80)
    
    for student in all_students:
        status = "⚠ NEEDS HELP" if student['marks'] < 12 else "✓ OK"
        email_status = "✗ Invalid" if not validate_email(student['email']) else ""
        combined_status = f"{status} {email_status}".strip()
        
        print(f"{student['name']:<25} {student['marks']:<10} {student['email']:<30} {combined_status:<15}")
    
    print("-" * 80)
    
    # Display underperforming students
    print(f"\n⚠ UNDERPERFORMING STUDENTS (Marks < 12): {len(underperforming)}")
    if underperforming:
        for student in underperforming:
            print(f"  • {student['name']} - Marks: {student['marks']}")
    else:
        print("  None")
    
    # Display invalid emails
    print(f"\n✗ INVALID EMAIL ADDRESSES: {len(invalid_emails)}")
    if invalid_emails:
        for student in invalid_emails:
            print(f"  • {student['name']} - Email: {student['email']}")
    else:
        print("  None")
    
    print("\n" + "=" * 80)
    print(f"SUMMARY: {len(all_students)} total students | "
          f"{len(underperforming)} need support | "
          f"{len(invalid_emails)} invalid emails")
    print("=" * 80 + "\n")

def main():
    """
    Main function to execute the student record analysis using both methods.
    """
    print("\n" + "=" * 80)
    print("STUDENT SUPPORT OFFICE - AUTOMATED CHECKING SYSTEM")
    print("Demonstrating BOTH Built-in CSV and Pandas Methods")
    print("=" * 80 + "\n")
    
    # Configuration
    csv_filename = "student_data.csv"
    
    # Check if CSV file exists, if not create sample data
    import os
    if not os.path.exists(csv_filename):
        print("Creating sample student data file...")
        with open(csv_filename, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Marks", "Email"])
            writer.writerow(["Alice Johnson", "15", "alice.johnson@university.edu"])
            writer.writerow(["Bob Smith", "8", "bob.smith@invalid"])
            writer.writerow(["Charlie Brown", "18", "charlie.brown@school.com"])
            writer.writerow(["Diana Prince", "10", "diana@edu.org"])
            writer.writerow(["Eve Wilson", "5", "eve.wilson@"])
            writer.writerow(["Frank Miller", "20", "frank.miller@college.edu"])
            writer.writerow(["Grace Lee", "11", "grace.lee@university.edu"])
            writer.writerow(["Henry Davis", "14", "henry.davis@school.com"])
        print(f"✓ Sample data created: {csv_filename}\n")
    else:
        print(f"✓ Using existing file: {csv_filename}\n")
    
    # ========================================================================
    # METHOD 1: Built-in CSV Module
    # ========================================================================
    underperforming1, invalid_emails1, all_students1 = analyze_student_records_csv(csv_filename)
    
    if all_students1:
        display_terminal_output(underperforming1, invalid_emails1, all_students1, "BUILT-IN CSV METHOD")
        
        report_filename1 = "report_csv.txt"
        generate_report(underperforming1, invalid_emails1, all_students1, report_filename1, "Built-in CSV Module")
        print(f"✓ Report generated: {report_filename1}")
    
    # ========================================================================
    # METHOD 2: Pandas Library
    # ========================================================================
    if PANDAS_AVAILABLE:
        underperforming2, invalid_emails2, all_students2 = analyze_student_records_pandas(csv_filename)
        
        if all_students2:
            display_terminal_output(underperforming2, invalid_emails2, all_students2, "PANDAS METHOD")
            
            report_filename2 = "report_pandas.txt"
            generate_report(underperforming2, invalid_emails2, all_students2, report_filename2, "Pandas Library")
            print(f"✓ Report generated: {report_filename2}")
    else:
        print("\n" + "=" * 80)
        print("⚠ Pandas method skipped (not installed)")
        print("  To use pandas: pip install pandas")
        print("=" * 80)
    
    # ========================================================================
    # Comparison Summary
    # ========================================================================
    print("\n" + "=" * 80)
    print("COMPARISON: BUILT-IN CSV vs PANDAS")
    print("=" * 80)
    
    print("\n📊 Built-in CSV Module:")
    print("  ✓ No installation required")
    print("  ✓ Lightweight and fast for simple tasks")
    print("  ✓ Good for basic CSV operations")
    print("  ✗ Limited data analysis features")
    print("  ✗ More manual coding required")
    
    print("\n📊 Pandas Library:")
    if PANDAS_AVAILABLE:
        print("  ✓ Powerful data analysis capabilities")
        print("  ✓ Built-in statistical functions (mean, std, etc.)")
        print("  ✓ Easy data filtering and manipulation")
        print("  ✓ DataFrame structure for complex operations")
        print("  ✗ Requires installation (pip install pandas)")
        print("  ✗ Heavier library (more memory)")
    else:
        print("  ✗ Not installed")
        print("  → Install with: pip install pandas")
    
    print("\n" + "=" * 80)
    print("✓ Analysis complete! Check the report files for detailed results.")
    print("=" * 80 + "\n")

# Execute the program
if __name__ == "__main__":
    main()
