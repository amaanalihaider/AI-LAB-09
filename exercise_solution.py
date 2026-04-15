"""
EXERCISE SOLUTION: Student Support Office Automation
Case Study: Automate checking of student records from CSV file

Requirements:
1. Identify students with marks less than 12
2. Validate email addresses using regex
3. Generate a report.txt file with results
4. Display output in terminal

Author: [Your Name]
Date: [Current Date]
"""

import csv
import re

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

def analyze_student_records(csv_filename):
    """
    Read and analyze student records from CSV file.
    
    Args:
        csv_filename (str): Path to CSV file
    
    Returns:
        tuple: (underperforming_students, invalid_emails, all_students)
    """
    underperforming_students = []
    invalid_emails = []
    all_students = []
    
    try:
        with open(csv_filename, "r") as file:
            csv_reader = csv.DictReader(file)
            
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
        
        return underperforming_students, invalid_emails, all_students
    
    except FileNotFoundError:
        print(f"Error: File '{csv_filename}' not found!")
        return [], [], []
    except Exception as e:
        print(f"Error reading file: {e}")
        return [], [], []

def generate_report(underperforming, invalid_emails, all_students, report_filename):
    """
    Generate a detailed report file with analysis results.
    
    Args:
        underperforming (list): List of underperforming students
        invalid_emails (list): List of students with invalid emails
        all_students (list): List of all students
        report_filename (str): Output report filename
    """
    with open(report_filename, "w") as report:
        report.write("=" * 80 + "\n")
        report.write("STUDENT SUPPORT OFFICE - AUTOMATED ANALYSIS REPORT\n")
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

def display_terminal_output(underperforming, invalid_emails, all_students):
    """
    Display formatted output in terminal.
    
    Args:
        underperforming (list): List of underperforming students
        invalid_emails (list): List of students with invalid emails
        all_students (list): List of all students
    """
    print("\n" + "=" * 80)
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
    Main function to execute the student record analysis.
    """
    print("\n" + "=" * 80)
    print("STUDENT SUPPORT OFFICE - AUTOMATED CHECKING SYSTEM")
    print("=" * 80)
    
    # Configuration
    csv_filename = "student_data.csv"
    report_filename = "report.txt"
    
    # Create sample data file (for demonstration)
    print("\nCreating sample student data file...")
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
    
    print(f"✓ Sample data created: {csv_filename}")
    
    # Analyze student records
    print("\nAnalyzing student records...")
    underperforming, invalid_emails, all_students = analyze_student_records(csv_filename)
    
    # Display results in terminal
    display_terminal_output(underperforming, invalid_emails, all_students)
    
    # Generate report file
    print(f"Generating report file: {report_filename}")
    generate_report(underperforming, invalid_emails, all_students, report_filename)
    print(f"✓ Report generated successfully: {report_filename}")
    
    print("\n✓ Analysis complete! Check the report file for detailed results.")
    print("=" * 80 + "\n")

# Execute the program
if __name__ == "__main__":
    main()
