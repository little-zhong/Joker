import hashlib
import random
import time
import string
from logger import logger


def generate_hash(input_string):
    """
    Generate hash value of input string

    Args:
        input_string (_type_): _description_

    Returns:
        _type_: _description_
    """
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode("utf-8"))
    return sha256.hexdigest()


def generate_random_string(length):
    """
    Generate a random string of fixed length

    Args:
        length (_type_): _description_

    Returns:
        _type_: _description_
    """
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def generate(payload, require="00000"):
    """
    generate nonce and hash

    Args:
        payload (_type_): _description_
        require (str, optional): _description_. Defaults to "00000".

    Returns:
        _type_: _description_
    """
    count = 0  # Initialize count inside the function to reset it each time

    start_time = time.time()

    while True:
        random_str = generate_random_string(48)
        combined = payload + random_str
        hash_value = generate_hash(combined)

        count += 1
        if count % 10000 == 0:
            ...

        if hash_value.startswith(require):
            # print(f"Hash found: {hash_value}")
            logger.info(f"Hash found: {hash_value}, count: {count}, time: {time.time() - start_time}")  # fmt: skip
            return random_str, hash_value


if __name__ == "__main__":
    payload = "xxxxx"
    require = "00000"

    random_str, hash_value = generate(payload, require)
    print(f"Random String: {random_str}, Hash: {hash_value}")
