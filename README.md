# Ming Ke Ming (名可名) -- Account Module (Python)

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/dimchat/mkm-py/blob/master/LICENSE)
[![Version](https://img.shields.io/badge/alpha-0.7.8-red.svg)](https://github.com/dimchat/mkm-py/wiki)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/dimchat/mkm-py/pulls)
[![Platform](https://img.shields.io/badge/Platform-Python%203-brightgreen.svg)](https://github.com/dimchat/mkm-py/wiki)

This [document](https://github.com/moky/DIMP/blob/master/MingKeMing-Identity.md) introduces a common **Account Module** for decentralized user identity authentication.

Copyright &copy; 2018-2019 Albert Moky

- [Meta](#meta)
    - [Version](#meta-version)
    - [Seed](#meta-seed)
    - [Key](#meta-key)
    - [Fingerprint](#meta-fingerprint)
- [ID](#id)
    - [Type](#id-type)
    - [Name](#id-name)
    - [Address](#id-address)
    - [Terminal](#id-terminal)
    - [Number](#id-number)
- [Samples](#samples)

## <span id="meta">0. Meta</span>

The **Meta** was generated by your **private key**, it can be used to build a new ID for entity, or verify the ID/PK pair.

It consists of 4 fields:

| Field       | Description                   |
| ----------- | ----------------------------- |
| version     | Meta Algorithm Version        |
| seed        | Entity Name                   |
| key         | Public Key                    |
| fingerprint | Signature to generate address |

### <span id="meta-version">0.0. Version</span>

* ```0x01``` **Default version**
* ```0x02``` BTC version
* ```0x03``` Extended BTC version
* ```0x04``` ETH version
* ```0x05``` Extended ETH version

### <span id="meta-seed">0.1. Seed</span>

A string as same as **ID.name** for generate the fingerprint.

### <span id="meta-key">0.2. Key</span>

A **public key** (PK) was binded to an ID by the **Meta Algorithm**.

### <span id="meta-fingerprint">0.3. Fingerprint</span>

THe **fingerprint** field was generated by your **private key** and **seed**:

````python
data = seed.encode('utf-8')
fingerprint = private_key.sign(data)
````

## <span id="id">1. ID</span>
The **ID** is used to identify an **entity**(user/group). It consists of 3 fields and 2 extended properties:

| Field       | Description                   |
| ----------- | ----------------------------- |
| name        | Same with meta.seed           |
| address     | Unique Identification         |
| terminal    | Login point, it's optional.   |
| type        | Network type                  |
| number      | Search Number                 |

The ID format is ```name@address[/terminal]```.

### <span id="id-type">1.0. Type</span>

The **network type** of a person is ```8```, and group is ```16```:

```python
class NetworkID(IntEnum):
    # Person Account
    Main = 0x08         # 0000 1000 (Person)

    # Virtual Groups
    Group = 0x10        # 0001 0000 (Multi-Persons)
    Polylogue = 0x10    # 0001 0000 (Multi-Persons Chat, N < 100)
    Chatroom = 0x30     # 0011 0000 (Multi-Persons Chat, N >= 100)

    # Network
    Provider = 0x76     # 0111 0110 (Service Provider)
    Station = 0x88      # 1000 1000 (Server Node)

    # Internet of Things
    Thing = 0x80        # 1000 0000 (IoT)
    Robot = 0xC8        # 1100 1000
```

### <span id="id-name">1.1. Name</span>
The **Name** field is a username, or just a random string for group:

1. The length of name must more than 1 byte, less than 32 bytes;
2. It should be composed by a-z, A-Z, 0-9, or charactors '_', '-', '.';
3. It cannot contain key charactors('@', '/').

```python
# Name examples
user_name  = "Albert.Moky"
group_name = "Group-9527"
```

### <span id="id-address">1.2. Address</span>

The **Address** field was created with the **Fingerprint** in Meta and a **Network ID**:

```python
def check_code(data: bytes) -> bytes:
    # check code in BTC address
    return sha256(sha256(data))[:4]
    
class BTCAddress(Address):
    
    @classmethod
    def new(cls, data: bytes, network: NetworkID=0) -> Address:
        """Generate address with fingerprint and network ID
        :param data:    fingerprint (signature/key.data)
        :param network: address type
        :return:        Address object
        """
        prefix = chr(network).encode('latin1')
        digest = ripemd160(sha256(data))
        code = check_code(prefix + digest)
        address = base58_encode(prefix + digest + code)
        return BTCAddress(address)
```

When you get a meta for the entity ID from the network,
you must verify it with the consensus algorithm before accept its **public key**.

```python
    """
    Meta algorithm
        1. compare meta.seed with ID.name
        2. build address with meta, compare it with ID.address
        3. if matches, get public key from meta
    """
    def match_identifier(self, identifier: ID) -> bool:
        """ Check ID(name+address) with meta info """
        if identifier is None:
            return False
        return self.generate_identifier(identifier.address.network) == identifier

    def match_address(self, address: Address) -> bool:
        """ Check address with meta info """
        if address is None:
            return False
        return self._generate_address(network=address.network) == address

    def generate_identifier(self, network: NetworkID) -> ID:
        """ Generate ID with meta info and network ID """
        address = self._generate_address(network=network)
        return ID.new(name=self.seed, address=address)

    @abstractmethod
    def _generate_address(self, network: NetworkID) -> Address:
        """ Generate address with meta info and network ID """
        pass
```

### <span id="id-terminal">1.3. Terminal</span>

A resource identifier as **Login Point**.

### <span id="id-number">1.4. Number</span>

A **Search Number** is defined for easy remember. Its value is converted from the **check code** of the address. It's greater than **0** and smaller than **2<sup>32</sup> (4,294,967,296)**.

## <span id="samples">2. Samples</span>

### ID

```python
# ID examples
ID1 = "hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj"  # Immortal Hulk
ID2 = "moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk"  # Monkey King
```

### Meta

```javascript
/* Meta(JsON) for hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj */
{
    "version"     : 0x01,
    "key"         : {
        "algorithm" : "RSA",
        "data"      : "-----BEGIN PUBLIC KEY-----\nMIGJAoGBALB+vbUK48UU9rjlgnohQowME+3JtTb2hLPqtatVOW364/EKFq0/PSdnZVE9V2Zq+pbX7dj3nCS4pWnYf40ELH8wuDm0Tc4jQ70v4LgAcdy3JGTnWUGiCsY+0Z8kNzRkm3FJid592FL7ryzfvIzB9bjg8U2JqlyCVAyUYEnKv4lDAgMBAAE=\n-----END PUBLIC KEY-----",
        // other parameters
        "mode"      : "ECB",
        "padding"   : "PKCS1",
        "digest"    : "SHA256"
    },
    "seed"        : "hulk",
    "fingerprint" : "jIPGWpWSbR/DQH6ol3t9DSFkYroVHQDvtbJErmFztMUP2DgRrRSNWuoKY5Y26qL38wfXJQXjYiWqNWKQmQe/gK8M8NkU7lRwm+2nh9wSBYV6Q4WXsCboKbnM0+HVn9Vdfp21hMMGrxTX1pBPRbi0567ZjNQC8ffdW2WvQSoec2I="
}
```

(All data encode with **BASE64** algorithm as default, excepts the **address**)
