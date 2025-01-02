# Finding a Subdomain Using Matching RSA Parameters in TLS Certificate

## Introduction

Finding a Subdomain Using Matching RSA Parameters in TLS Certificate
Introduction

In this challenge, we are provided with an RSA public key in PEM format (`transparency.pem`). Our task is to:

1. Extract the RSA modulus n and exponent e from the given PEM file.
2. Find the subdomain of cryptohack.org whose TLS certificate uses the same RSA parameters (n and e).
3. Visit that subdomain to obtain the flag.

This challenge involves understanding how TLS certificates are issued and how to search through Certificate Transparency Logs to find certificates matching specific cryptographic parameters. 

### Understanding the Challenge
When you connect to a website over HTTPS, the server presents a TLS certificate during the handshake. This certificate contains the server's public key, which is used to establish a secure connection.

Certificate Transparency (CT) is an open framework for monitoring and auditing TLS certificates. All publicly trusted Certificate Authorities (CAs) are required to log every certificate they issue to public CT logs. These logs can be queried to find certificates issued for specific domains.




