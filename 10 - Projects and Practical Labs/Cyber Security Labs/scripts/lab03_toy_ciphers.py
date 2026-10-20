"""LAB-CS-03: toy ciphers and why they fail. Teaching code only: NEVER use these ciphers to protect data.

Run:  python lab03_toy_ciphers.py
Part E needs the 'cryptography' package (pip install cryptography); it is skipped if unavailable.
"""
import string
from collections import Counter

# Approximate English letter frequencies (percent), a commonly used reference table.
ENGLISH = {
    "a": 8.2, "b": 1.5, "c": 2.8, "d": 4.3, "e": 12.7, "f": 2.2, "g": 2.0, "h": 6.1, "i": 7.0, "j": 0.15,
    "k": 0.77, "l": 4.0, "m": 2.4, "n": 6.7, "o": 7.5, "p": 1.9, "q": 0.095, "r": 6.0, "s": 6.3, "t": 9.1,
    "u": 2.8, "v": 0.98, "w": 2.4, "x": 0.15, "y": 2.0, "z": 0.074,
}


def caesar(text: str, shift: int) -> str:
    out = []
    for ch in text:
        if ch in string.ascii_lowercase:
            out.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        elif ch in string.ascii_uppercase:
            out.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        else:
            out.append(ch)
    return "".join(out)


def chi_squared(text: str) -> float:
    letters = [c for c in text.lower() if c in ENGLISH]
    n = len(letters) or 1
    counts = Counter(letters)
    return sum((counts[c] - n * p / 100) ** 2 / (n * p / 100) for c, p in ENGLISH.items())


def break_caesar(ciphertext: str) -> tuple[int, str]:
    """Try all 26 keys; the most English-like plaintext (lowest chi-squared) wins."""
    best = min(range(26), key=lambda k: chi_squared(caesar(ciphertext, -k)))
    return best, caesar(ciphertext, -best)


def vigenere(text: str, key: str, decrypt: bool = False) -> str:
    out, i = [], 0
    for ch in text:
        if ch.lower() in string.ascii_lowercase:
            k = ord(key[i % len(key)].lower()) - 97
            out.append(caesar(ch, -k if decrypt else k))
            i += 1
        else:
            out.append(ch)
    return "".join(out)


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def main() -> None:
    msg = "Meet the examinations officer at the library at noon and bring the marked scripts"

    print("== Part A: Caesar cipher (shift 7) ==")
    ct = caesar(msg, 7)
    print("ciphertext:", ct)
    k, pt = break_caesar(ct)
    print(f"brute force + frequency score -> key {k}: {pt}")
    print("keyspace: 26 keys; a computer checks them all instantly")

    print("\n== Part B: letter frequencies leak through substitution ==")
    top = Counter(c for c in ct.lower() if c.isalpha()).most_common(3)
    print("most common ciphertext letters:", top, "(plaintext 'e' shifted by 7 is 'l')")

    print("\n== Part C: Vigenere (key 'chuo') ==")
    long_msg = (msg + ". The marked scripts must be stored in the locked cabinet in the examinations office "
                "and returned to the registry before the board of examiners meets on Friday afternoon. "
                "Students who have queries about their results should contact their head of department.")
    v = vigenere(long_msg, "chuo")
    print("ciphertext (first 60):", v[:60], "...")
    letters = "".join(c for c in v.lower() if c.isalpha())
    recovered = "".join(chr(97 + break_caesar(letters[i::4])[0]) for i in range(4))
    print(f"split into 4 columns, break each as Caesar -> key {recovered!r}")
    print("decrypt with recovered key:", vigenere(v, recovered, decrypt=True)[:60], "...")
    short_guess = "".join(chr(97 + break_caesar("".join(c for c in vigenere(msg, "chuo").lower() if c.isalpha())[i::4])[0])
                          for i in range(4))
    print(f"same attack on the short message alone -> {short_guess!r} (too little text for statistics)")

    print("\n== Part D: reusing a one-time pad / stream key ==")
    key = bytes([0x5A, 0x13, 0xC7, 0x88, 0x21, 0x9E, 0x40, 0x07, 0xBB, 0x6D, 0x31, 0xF2, 0x0C, 0x99, 0x57, 0xE4])
    p1, p2 = b"PAY JUMA 50000 T", b"PAY NEEMA 900 TZ"
    c1, c2 = xor_bytes(p1, key), xor_bytes(p2, key)
    print("c1 xor c2 == p1 xor p2 ?", xor_bytes(c1, c2) == xor_bytes(p1, p2))
    print("attacker who knows (or guesses) p1 recovers p2:", xor_bytes(xor_bytes(c1, c2), p1))

    print("\n== Part E: the real thing (AES-256-GCM, authenticated) ==")
    try:
        import os

        from cryptography.exceptions import InvalidTag
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        print("cryptography not installed; skipping")
        return
    aes = AESGCM(AESGCM.generate_key(bit_length=256))
    nonce = os.urandom(12)
    sealed = aes.encrypt(nonce, msg.encode(), b"lab03")
    print("ciphertext+tag length:", len(sealed), "bytes (message", len(msg), "+ 16-byte tag)")
    tampered = bytes([sealed[0] ^ 1]) + sealed[1:]
    try:
        aes.decrypt(nonce, tampered, b"lab03")
    except InvalidTag:
        print("one flipped bit -> InvalidTag: tampering detected")
    print("decrypts correctly:", aes.decrypt(nonce, sealed, b"lab03").decode() == msg)


if __name__ == "__main__":
    main()
