import sys

def main():
    if len(sys.argv) != 2:
        return
    
    target_email = sys.argv[1]
    
    try:
        with open('employees.tsv', 'r') as tsv_file:
            # Skip header line
            next(tsv_file)
            
            for line in tsv_file:
                if line.strip():
                    name, surname, email = line.strip().split('\t')
                    
                    if email == target_email:
                        # Use f-string as required
                        letter = f"Dear {name}, welcome to our team! We are sure that it will be a pleasure to work with you. That's a precondition for the professionals that our company hires."
                        print(letter)
                        return
            
        # If email not found
        return
    
    except Exception:
        # According to instructions - don't handle open() exceptions
        return

if __name__ == '__main__':
    main()