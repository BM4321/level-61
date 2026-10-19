"""PY-15: propagation, else/finally order, chaining. Run: python examples/py15_exceptions.py"""


def demo(x):
    try:
        print("  try")
        result = 10 / x
    except ZeroDivisionError:
        print("  except")
        return "error"
    else:
        print("  else")
        return result
    finally:
        print("  finally")


print("demo(2) ->", demo(2))
print("demo(0) ->", demo(0))


class ConfigError(Exception):
    pass


try:
    try:
        port = int({"port": "eighty"}["port"])
    except (KeyError, ValueError) as exc:
        raise ConfigError("invalid or missing 'port' setting") from exc
except ConfigError as err:
    print("caught:", err, "| caused by:", repr(err.__cause__))
