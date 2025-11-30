import socket

passwords_wordlist = "/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt"
endpoints_wordlist = "/home/cccitron/Downloads/API_wordlist"
#hostname = input("Hostname (IP or hostname): ")
#port = int(input("Port: "))

hostname = "10.80.166.57"
port = 8000


def fuzz_endpoints():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hostname, port))

    with open(endpoints_wordlist, 'rb') as f:
        endpoints = f.read()

    for endpoint in endpoints.decode().splitlines():
        client_socket.sendall(endpoint.encode(errors="ignore"))
        response = client_socket.recv(1024).decode(errors="ignore")
        if not f"name '{endpoint}' is not defined" in response:
            print(f"Endpoint: '{endpoint}' worked! Response: {response}")
            endponit = "" # !!! Change this once you find correct endpoint!
            user_choice = input(f"Brute force password with endpoint: '{endpoint}' (y/n): ")
            if user_choice.lower() == "y":
                print(type(user_choice))
                brute_force(endpoint)
            elif user_choice.lower() == 'n':
                print("Bye!")
            else:
                print("Wrong input")

def brute_force(endpoint):
    print(endpoint)
        
def main():
    fuzz_endpoints()

if __name__ == "__main__":
    main()