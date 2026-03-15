import sys

def main():
    if len(sys.argv) != 2:
        return
    
    emails_file = sys.argv[1]
    
    try:
        with open(emails_file, 'r') as f:
            emails = [line.strip() for line in f if line.strip()]
        
        with open('employees.tsv', 'w') as tsv_file:
            # Write headers
            tsv_file.write("Name\tSurname\tEmail\n")
            
            for email in emails:
                # Parse name.surname@corp.com
                username = email.split('@')[0]
                name_parts = username.split('.')
                
                if len(name_parts) >= 2:
                    name = name_parts[0].capitalize()
                    surname = name_parts[1].capitalize()
                    
                    # Write to TSV with tab separation
                    tsv_file.write(f"{name}\t{surname}\t{email}\n")
    
    except Exception:
        # According to instructions - don't handle open() exceptions
        return

if __name__ == '__main__':
    main()