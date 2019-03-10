#! /usr/bin/env python3

import sys
import hashlib
import binascii

dhash = lambda x: hashlib.sha256(hashlib.sha256(x).digest()).digest()
b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_check_encode(b, version):
    d = version + b
    address = d + dhash(d)[:4]

    # Convert big‐endian bytes to integer
    n = int('0x0' + binascii.hexlify(address).decode('utf8'), 16)

    # Divide that integer into base58
    res = []
    while n > 0:
        n, r = divmod (n, 58)
        res.append(b58_digits[r])
    res = ''.join(res[::-1])

    # Encode leading zeros as base58 zeros
    czero = 0
    pad = 0
    for c in d:
        if c == czero: pad += 1
        else: break
    return b58_digits[0] * pad + res


def base58_decode (s, version):
    # Convert the string to an integer
    n = 0
    for c in s:
        n *= 58
        if c not in b58_digits:
            raise Exception
        digit = b58_digits.index(c)
        n += digit

    # Convert the integer to bytes
    h = '%x' % n
    if len(h) % 2:
        h = '0' + h
    res = binascii.unhexlify(h.encode('utf8'))

    # Add padding back.
    pad = 0
    for c in s[:-1]:
        if c == b58_digits[0]: pad += 1
        else: break
    k = version * pad + res

    addrbyte, data, chk0 = k[0:1], k[1:-4], k[-4:]
    return data


def generate (prefix_string, vanity_keyword, prefix_bytes):

    # Pad and prefix.
    prefixed_name = prefix_string + vanity_keyword
    padded_prefixed_name = prefixed_name.ljust(34, 'X')

    # Decode, ignoring (bad) checksum.
    decoded_address = base58_decode(padded_prefixed_name, prefix_bytes)

    # Re-encode, calculating checksum.
    address = base58_check_encode(decoded_address, prefix_bytes)

    # Double-check.
    assert base58_decode(address, prefix_bytes) == decoded_address

    return address


if __name__ == '__main__':

    cont = True
    prefix_string = ""
    vanity_keyword = ""
    # Check the cmd line parameters
    if len(sys.argv) == 1:
      # No arguments passed in
      print("Error: No arguments found.")
      cont = False
    elif len(sys.argv) == 2:
      # Only prefix string was passed in
      prefix_string = sys.argv[1]
    elif len(sys.argv) == 3:
      # Both prefix string and vanity keyword were passed in
      prefix_string = sys.argv[1]
      vanity_keyword = sys.argv[2]
    else:
      # Too many arguments passed in
      print("Error: Too many arguments found.")
      cont = False
    if cont == True:
      # Check the length of the prefix and vanity keyword
      if len(prefix_string + vanity_keyword) > 28:
        print("Error: The address prefix and vanity keyword are too long to generate a valid address.")
        cont = False
    if cont == True:
      # Check for invalid characters in the address prefix
      for a in range(0, len(prefix_string)):
        valid = False
        for b in range(0, len(b58_digits)):
          if prefix_string[a] == b58_digits[b]:
            # This character is valid
            valid = True
            break
        if valid == False:
          # Invalid character found
          print("Error: Invalid characters detected in the address prefix. Valid characters are: " + b58_digits)
          cont = False
          break
    if cont == True:
      # Check for invalid characters in the vanity keyword
      for a in range(0, len(vanity_keyword)):
        valid = False
        for b in range(0, len(b58_digits)):
          if vanity_keyword[a] == b58_digits[b]:
            # This character is valid
            valid = True
            break
        if valid == False:
          # Invalid character found
          print("Error: Invalid characters detected in the vanity keyword. Valid characters are: " + b58_digits)
          cont = False
          break		  
    if cont == True:
      found = False
      # Loop through all possible prefix bytes to figure out the correct byte
      for i in range(0, 256):
        # Get the next address to test
        result = generate(prefix_string, vanity_keyword, (i).to_bytes(1, 'big'))
        # Check if this is the correct address
        if result[:len(prefix_string) + len(vanity_keyword)] == prefix_string + vanity_keyword:
          # 99% sure this is the correct address but do one last check to be 100%
          found = True
          xbits = result[len(prefix_string) + len(vanity_keyword):-6]
          for x in range(0, len(xbits)):
            if xbits[x] != "X":
              # This is not the correct address after all
              found = False
              break
          # Stop checking if the correct address has already been found
          if found == True:
            # Display the result
            print("Result: " + result)
            print("Decimal Address Prefix: " + str(i))
            break
      # Ensure that a result was already returned
      if found == False:
        print("Error: No results found.")
