"""PY-09: slicing, immutability, methods. Run: python examples/py09_strings.py"""
s = "PYTHON"
print(s[0], s[-1], s[1:5:2], s[::-1], s[2:100])
try:
    s[0] = "J"
except TypeError as exc:
    print("TypeError:", exc)
print("a,,b".split(","), "a  b".split(), "key=a=b".partition("="))
print(ord("A"), chr(97), len("café"), len("café".encode("utf-8")))
print("Zebra" < "apple", "Zebra".casefold() < "apple".casefold())
parts = [str(i) for i in range(5)]
print("-".join(parts))
