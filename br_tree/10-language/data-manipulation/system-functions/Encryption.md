---
title: Encryption
file: Encryption.md
source: https://brulescorp.com/brwiki2/index.php?title=Encryption
category: 10-language
subcategory: 10-language/data-manipulation/system-functions
kind: function
related: [ENCRYPT, DECRYPT, internal functions, ENCRYPT$, DECRYPT$]
---
(As of 4.30)

**Encryption** encompasses a number of different operations.  These operations can be used independently or in combination to meet different needs.  We use industry standard encryption available through OpenSSL.  Three technologies are widely used for encrypting data. BR supports the first two listed below through its `ENCRYPT` and `DECRYPT` `internal functions`. 

==Overview of Two Encryption Methods==

1. **Symmetric key ciphers** – where the same key is used to encrypt and decrypt data. You can specify a key to encrypt some data and later use the same key to decrypt the data.

2. **Hashing routines** – one way routines that take data and convert it to a hash value.  Sometimes these are thought of as checksums such as MD5 sum.  Hash values are always the same length regardless of how big the hashed data is.  A 10 gb file will have a hash result that is the same length as a 200 byte file. Hashing routines have a number of specific uses, including:
*Verify that data has not changed.
*Verifying that two files are the same.
*Validating passwords – this is based on the concept that if two values have the same hash value the values are equal.  Using this technique improves security because it allows a server to store passwords in an unrecoverable format.  Even the server software is unable to regenerate the original password.  It is only capable of checking if the hash of a password matches the stored password hash.

==Symmetric Key Ciphers==
There are two encryption functions in the BR language, `ENCRYPT$` and `DECRYPT$`.

- ENCRYPT$(Data$ [,Key$ [,Encryption-type$ [,Initialization-vector$]]])
- DECRYPT$(Data$ [,Key$ [,Encryption-type$ [,Initialization-vector$]]])

Data$ - The data to be encrypted

Key$ - The secret key to be used for encryption.  If not specified this value will come from an OPTION 66 statement.

Encryption-type$ - The type of encryption to be done.  If not specified, a common high strength encryption type will be employed.  This is described in more detail below, but is generally only useful for interfacing with other typically non-BR programs.

Initialization-vector$ - This is an arcane part of encryption standards. It exists to prevent attackers from being able to tell whether the unencrypted data has changed. This is described in more detail below, but is general only needed when interfacing with other non-BR programs.

== Interfacing With Other Programs (encryption type and initialization vector)==
There are a number of different types of encryption that BR supports through OpenSSL:  AES, BLOWFISH, DES, triple DES, RC4 and RC2.  Most symmetric key ciphers are block ciphers meaning that they encrypt one block at a time. This means if you have a bit message, it is broken up into multiple blocks and each block is encrypted. The block size can be set as (128, 192, 256) bits. Some encryption types don't support all of these values so STATUS ENCRYPTION should be checked to see what encryption types are available in BR. Besides block size, there are also various schemes for blocking data. One might expect that using 256 bit blocking would simply take every 32 bytes and call it a block.  This is not done though because there is a possibility that this would cause patterns in the encrypted data. To prevent this, there are various schemes known as codebooks which change the way data is blocked. Wikipedia explains this in more detail. If the encryption type is not specified AES:256:CBC:128 will be used. To be compatible with other programs the entire encryption type must be specified (cipher: key length: codebook: initialization vector length).

Initialization-vector – this is used to cause the same data encrypted with the same key to have a different encrypted result. This is significant because otherwise an attacker looking at data seeing the same encrypted result twice would know that the key and the unencrypted data have not changed. Regardless of whether or not you are concerned about this potential security issue, the standard encryption methods require this value so interfacing with other programs may require you to use it. It is a common practice to use a random number for this value and store the value at the beginning of (ahead of) the encrypted result. This is what BR does if this parameter is omitted.

As an example:
 ENCRYPT$(“test”,“key”) 
Produces a string containing “random number initialization vector”&”encrypted result”.

If the initialization vector is explicitly specified as in:
ENCRYPT$(“test”,“key”,“AES:256:CBC:128”,“RANDOM”) 
the result would be simply “encrypted result”.

DECRYPT$ has the same arguments as ENCRYPT$ with the exception of the first parameter which is the encrypted data. DECRYPT$ expects to be used with the same key$, encryption-type$, and initialization-vector$ as was used to encrypt the data.  As with ENCRYPT$, if key$ is not specified, the value from the OPTION statement will be used. If encryption-type$ is not specified, “AES:256:CBC:128” will be used. If the initialization vector is not specified, it will be assumed that the encrypted data starts with an initialization vector.

==Hashing Routines==
Three common forms of hashing are allowed in BR. They are MD5, SHA, and SHA-1. These are also provided through the ENCRYPT$ function specifying a null key$ value:

 ENCRYPT$(data$, “”, “MD5”) ENCRYPT$(data$, “”, “SHA”) ENCRYPT$(data$, “”, “SHA-1”)

Hashing is also referred to as Message Digests or digests. This is what the MD in MD5 means. There is no way to restore data that has been hashed. Hashing is a one way function so DECRYPT$ will yield an error.

==Asymmetric Encryption==
Asymmetric key encryption is also known as public/private key encryption.

Public/private keys are created as a pair by a key generator.  They are a pair, and it is not possible to have two public keys for the same private key or vice versa. With regard to public/private key pairs, what one key encrypts the other key can decrypt, and neither key can decrypt what it has encrypted.  When a private key is used to encrypt data, the result is called a signature because everyone who has the public key can decrypt it.

This technique is used for:

Signing (using certificates) – A private key can be used to sign data. The result of such signing can be tested/validated with the corresponding public key.

Data encryption – A public key can be used to encrypt data. This data can then only be decrypted by the corresponding private key.

Hashes and signing are different but used together.  Rather than signing a large block of data which would create a large signature, only the hash is signed to create much smaller fixed length signature data.  When verifying a large block of signed data, the data is used to create a hash value and the hash value is compared to a decrypted signature.

Asymmetric encryption is not accessible through the BR ENCRYPT$, DECRYPT$ functions. However, it is used by our SSL client server connections and HTTPS. Certificates are most commonly used by SSL and HTTPS and are less useful for other application processes. 

In the Client Server model the client knows the server’s public key and the server uses its private key to encrypt and decrypt.  BRclient.exe connects to BRListener.exe by opening an SSL socket on the server using DHE_RSA-AES256-SHA Encryption. Handshaking is performed using a private key stored on the server within BRListener. Once authenticated, the socket is then passed to BRServer.exe for actual data processing.

Encryption is invoked by Business Rules HTTP support as follows:

 CONFIG HTTPS port-number   [ LOG file-pathname ] [CERT= cert-file-basename]
 CONFIG OPTION  66   private-key-file-encryption-password
 OPEN #400: “HTTP=SERVER”, DISPLAY, OUTIN

The BRSERVER executable directory must contain two files:

 https-private.pem
 https-cert.pem

These files are made by the following commands under Linux, MAC and cygwin for Windows: openssl req -new -x509 -out httpserver.pem -days 10000

(this will prompt for the OPTION 66 password)

 mv privkey.pem   https-private.pem
 mv httpserver.pem   https-cert.pem

This port specific service can then be accessed with browsers. When the specified port is accessed through a browser, BR establishes an HTTPS connection rather than an HTTP connection.

==Signing and Certificate Processing Industry Standards==
The purpose of certificates is to verify the authenticity of unencrypted data. 

Certain companies are authorized by the government to act as a Certificate Authority (CA). These companies (e.g. Verisign) issue electronic certificates which can be used to issue second level certificates. Certificates can have expiration dates and the line of authority extends from a CA to any number of levels (but a chain is only as strong as its weakest link). Certificates contain a list of signatures (described below) that trace back to a CA as follows: 

When a company needs to obtain a certificate from a CA, it prepares its own certificate and sends it to the CA for signature. Creating a certificate requires the pre-production of a private and public key pair. The certificate text properly identifies the signing authority, the owner of the certificate, and the owner’s public key. The signing authority externally verifies the identity of the owner before signing it.  The CA provides the signature and the CA’s own public key for validating it. 

Browsers know the CA identities and their public keys. A browser can verify a CA signed cert by hashing it, decrypting the signature with the known public key and matching the decrypted signature against the hash total. 
 
Any company that is issued a (self-prepared authority signed) certificate by a CA can sign second level certificates issued to third parties. A second level cert contains the parent (CA issued) certificate, and includes the public keys of the issuer and the recipient. The signature is essentially the encrypted hash total of ‘itself plus all of its ancestors’. Additional levels each contain the chain of certificates leading from a CA issued cert to itself. By including public keys along with the identities of the owners, certificates become tools for validating the signatures of their owners. When signed data (with an encrypted hash total) is sent to clients the signatures insure that the data has not been altered along the way. 

Ostensibly, a certificate cannot be counterfeited because it requires the signature of its parent which can only be produced with its parent’s private key.  By providing both public keys ( signer and recipient ) in all certs along with signatures, a non-forgeable or alterable chain is established. 

====Example:====
CA public key – known to browser
certificate 1 (signed by CA – contains owner’s public key)
certificate 2 (signed by second level - includes certificate 1 - contains owner’s public key)
final certificate (signed by third level - includes certificate 2 - contains owner’s public key)
 
A browser would find the CA information in the certificate and check to see if it is in the browser’s internal list. If not, it fails. Then it verifies that certificate 1 (which ends up being part of the final certificate) has been signed by the CA. After that it checks certificate 2 and verifies that it has been signed by the owner of certificate 1. Finally it checks the final certificate and verifies that it has been signed by the owner of certificate 2.

To assure the line authority of any certificate, the public keys are associated with signers, not with documents. 

==**Encryption Support by Version**==

BR encryption support has evolved over time. The sections below distinguish between currently supported legacy algorithms, deprecated (removed) algorithms, and newer additions.

==Old List (Still Supported)==

The following algorithms are supported for backward compatibility and remain available in current versions:

===Symmetric Key Ciphers===
<pre>
DES (all modes)
DES-EDE / DES-EDE3 (Triple DES)
RC4 (40, 128)
RC2 (40, 64, 128)
BF (Blowfish)
CAST5
AES:128 / 192 / 256 (ECB, CBC, CFB, OFB)
IDEA
CAMELLIA:128 / 192 / 256
SEED
</pre>

===Message Digest Algorithms===
<pre>
MD5
SHA-1
MDC-2
RIPEMD-160
</pre>

==Deprecated (Removed / No Longer Available)==

The following algorithms were available in earlier versions but are no longer exposed in current builds:

<pre>
SHA   (original / alias)
DSS
DSS-1
</pre>

These were removed due to obsolescence or lack of modern security relevance.

==In Development (Newer Additions)==

===Added in Version 4.31hdg===
<pre>
SHA-256
</pre>

==STATUS ENCRYPTION==

The command:

<pre>
STATUS ENCRYPTION
</pre>

displays the encryption and digest algorithms supported by the currently running BR executable. This is the authoritative source for determining which algorithms are available.

==Notes==

* Default encryption:
  <code>AES:256:CBC:128</code>
* If no initialization vector is provided, BR prepends a random IV to the encrypted output.
* DECRYPT$ must use the same parameters as ENCRYPT$.

==Wishlist: Future Encryption Types==

The following modern algorithms are supported by OpenSSL but not currently exposed in BR:

* AES:128:GCM:96
* AES:192:GCM:96
* AES:256:GCM:96
* HMAC-SHA-256
* HMAC-SHA-512
* SHA-512
* ChaCha20-Poly1305
* PBKDF2 (password hashing)
