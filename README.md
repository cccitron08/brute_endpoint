NOTE:
THIS CODE WILL LIKELY REQUIRE TWEAKING AND CHANGES BASED ON ENVIROMENT!

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
  Continuous sending of data read from a wordlist while maintaining a persistent TCP connection.

- **Limit mode**  
  Reconnect-per-attempt logic, useful for learning how repeated connections behave.

### ✔ File handling
The script loads two wordlists:

- Password list  
- Endpoint list  

Each line is read and transmitted through the socket one at a time.

### ✔ Response handling
The program prints server responses, lowercases them for comparison, and demonstrates:

- substring checks  
- `any()` matching across multiple keywords  
- error-tolerant decoding  

NOTE: 
THIS WILL MOST LIKELY REQUIRE TWEAKS!
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

Do **not** use this script against systems you do not own or administer.  
Unauthorized access or probing of remote systems is illegal and unethical.

