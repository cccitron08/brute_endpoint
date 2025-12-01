NOTE:
THIS CODE WILL LIKELY REQUIRE TWEAKING AND CHANGES BASED ON ENVIROMENT!

# Socket Interaction Tool (Educational)

This project is a Python script that demonstrates how to:

- Open and manage TCP socket connections  
- Read external files and iterate line-by-line  
- Send and receive data over a persistent socket  
- Reconnect automatically on connection errors  
- Handle user input and branching modes  
- Use functions for structured code organization  
- Decode/encode transmitted data safely  
- Work with two different operational modes  
- Manage global vs. passed-in parameters  

It is intended **strictly for learning** how Python socket communication and file-driven workflows operate.

---

## Features

### ✔ Interactive CLI workflow
The script prompts the user for:

- Wordlist file paths  
- Target IP address  
- Target port  
- Operation mode  
- Optional follow-up actions depending on received responses  

### ✔ Two operational modes
The program supports two top-level modes:

- **Limitless mode**  
  Demonstrates continuous sending of data read from a wordlist while maintaining a persistent TCP connection.

- **Limit mode**  
  Demonstrates reconnect-per-attempt logic, useful for learning how repeated connections behave.

### ✔ File handling
The script loads two wordlists:

- Password list  
- Endpoint list  

Each line is read and transmitted through the socket one at a time.

### ✔ Socket management
The code shows how to:

- Open a socket  
- Reconnect automatically after errors  
- Send bytes (`sendall()`)  
- Receive bytes (`recv()`)  
- Decode/encode with error skipping  
- Close sockets gracefully in `finally` blocks  

### ✔ Response handling
The program prints server responses, lowercases them for comparison, and demonstrates:

- substring checks  
- `any()` matching across multiple keywords  
- error-tolerant decoding  

---

## Requirements

- Python 3.8+ recommended  
- No external libraries required  

The script uses only the standard library:

- `socket`  
- `pathlib`  

---

## Running the Script


You will be prompted to provide:

1. Path to a password list  
2. Path to an endpoint list  
3. IP address  
4. Port  
5. Desired mode (limitless / limit)  

Paths must point to existing readable files.

---

## Code Structure Overview

main()
├── limitless_fuzz_endpoints()
│ └── limitless_brute_force()
├── limit_fuzz_endpoint()
│ ├── limit_send_endpoint()
│ └── limit_brute_force()
│ └── limit_send_password()


Each function focuses on a single responsibility:

- establishing connections  
- sending/receiving data  
- loading the appropriate list  
- handling errors gracefully  

---

## Safe Use Notice

This repository is intended **solely for educational exploration of Python networking**, file parsing, and interactive program flow.

Do **not** use this script against systems you do not own or administer.  
Unauthorized access or probing of remote systems is illegal and unethical.

