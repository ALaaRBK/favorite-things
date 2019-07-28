from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABdMvJ0u4GqRPgyQclNTqdHvGciYCCPx51k6UkLUOPBtmfde_tYYRu-UNxyKnHtMAov72havwFuVUzyga3vlMJMOPBWaBJvurZokyT0ShupLgJ0_Grpotk897Iy6wS7EAqlr9ypFAQr8UcqVjagmfofEJ9Q5HkYp2zPINnuPIJ75a89MfI='

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()