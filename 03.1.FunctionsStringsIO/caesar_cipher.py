def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """
    ans = ""
    for i in message:
        k = ord(i)
        if (k >= 65 and k <= 90) or (k >= 97 and k <= 122):
            if k >= 65 and k <= 90:
                k += n % 26
                if k > 90:
                    k -= 26
            else:
                k += n % 26
                if k > 122:
                    k -= 26
        ans += chr(k)
    return ans
