generic-unspendable
====================

The generic-unspendable script generates a valid base58 encoded address string that meets the validation checks for most cryptocurrency networks but is generated in such a way that the private key can never be found. This is useful for generating a coin burn address where any coins sent to the address can never be recovered. Using this method also allows injecting a vanity keyword into the address so that the address visibly looks much less like a random address and more like the burn address it is meant to be.

USAGE:
----------------------------

Simply call the python script and pass in the cryptocurrency's address prefix and a vanity keyword that will appear directly after the prefix. For example, to generate a burn address for the Bitcoin network you can use the following:

```
$ ./unspendable.py 1 BurnAddress
Result: 1BurnAddressXXXXXXXXXXXXXXXXV7cPS6
Decimal Address Prefix: 0
```

The first argument of **1** is the address prefix for the Bitcoin network.  
The 2nd argument of **BurnAddress** is the vanity keyword to insert.

**NOTE:** Only certain alphanumeric characters are valid for the address prefix and vanity keyword. The list of valid characters are: **123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz**

The actual address is **1BurnAddressXXXXXXXXXXXXXXXXV7cPS6** and as an added check, the decimal address prefix of **0** is also displayed to eliminate guessing. The decimal address prefix must match the 2nd bit in the **PUBKEY_ADDRESS** of the coin's source code or else the address will not be valid. [Click here to view the PUBKEY_ADDRESS for Bitcoin's mainnet](https://github.com/bitcoin/bitcoin/blob/257f750cd986641afe04316ed0b22b646b56b60b/src/chainparams.cpp#L132). If you are not able to generate a valid address for your network it is most likely because the decimal address prefix doesn't match. You may have to change the vanity keyword to something that starts with a different number or letter to find one that matches your network's decimal address prefix. [Click here for more information about how the address prefixes work](https://en.bitcoin.it/wiki/List_of_address_prefixes).

