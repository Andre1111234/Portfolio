import sys

def call_center(clients, recipients):
    """Клиенты, которые не получали письмо"""
    return list(set(clients) - set(recipients))

def potential_clients(clients, participants):
    """Участники, которые не клиенты"""
    return list(set(participants) - set(clients))

def loyalty_program(clients, participants):
    """Клиенты, которые не участвовали в ивенте"""
    return list(set(clients) - set(participants))

def main():
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com', 
               'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com', 
               'elon@paypal.com', 'jessica@gmail.com']
    
    participants = ['walter@heisenberg.com', 'vasily@mail.ru', 
                   'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com', 
                   'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']
    
    if len(sys.argv) != 2:
        return
    
    task = sys.argv[1]
    
    if task == 'call_center':
        result = call_center(clients, recipients)
    elif task == 'potential_clients':
        result = potential_clients(clients, participants)
    elif task == 'loyalty_program':
        result = loyalty_program(clients, participants)
    else:
        raise ValueError("Invalid task name")
    
    for email in result:
        print(email)

if __name__ == '__main__':
    main()