# Joker

## Overview

The Joker project is a solution for interacting with the BlockJoker API, utilizing both Python and Rust for efficient performance. The Python environment handles API interactions, while the Rust environment is used to compile a high-performance hashing function.

## Setup

### 1. Python Environment

To set up the Python environment, follow these steps:

1. **Create a Python virtual environment:**

```sh
python3 -m venv .venv
source .venv/bin/activate
```

2.**Install the required dependencies:**
```sh
pip install -r requirements.txt
```

### 2. Rust Environment (Optional)
If you want to compile the Rust hashing function yourself, follow these steps:

1. **Install Rust and necessary dependencies:**
```sh
sudo apt update &&
sudo apt install -y curl tmux git libssl-dev pkg-config &&
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y &&
source $HOME/.cargo/env
```

2. **Build the Rust project:**
```sh
cd find_hash
cargo build --release
cp ./target/release/find_hash ../find
```

### 3.Initialize Account

1. **Create a .env file:**
```sh
cp .env.example .env
```

2. **Set up your environment variables:**

- Modify CAPSOLVER_API_KEY in the .env file to your own key.

3. **Retrieve and set the BlockJoker access token:**

- Log in to BlockJoker.
- Open the browser console and enter:

```js
console.log(localStorage.BLOCK_JOKER_ACCESS_TOKEN)
```
- Copy the token (without quotes) and save it in an `auth.txt` file in the same directory, with one token per line.

## Usage

### Running the Python Script

Run the Python script to interact with the BlockJoker API:

```sh
python main.py
```

### Running the Rust Hasher

If using the Rust hasher, ensure the compiled find_hash binary is in the same directory as main.py. Use the following command to run it:

```sh
./find <mission_id> <require> <cores>
```

## Contribution

Feel free to contribute to this project by submitting issues or pull requests. Your contributions are welcome!

```csharp
You can copy and paste this into your `README.md` file directly.
```
