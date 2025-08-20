import re

class CoinCollector:
    _VALUES = {"p": 1, "n": 5, "d": 10, "q": 25, "h": 50, "w": 100}

    # NOTE: remove spaces from the character class
    _TOKEN = re.compile(r"\s*([0-9]+)\s*([pndqhwPNDQHW])\s*")

    @staticmethod
    def parseChange(changeString: str) -> int:
        if not changeString:
            return 0

        total = 0
        s = changeString.replace(",", " ").replace(";", " ")
        i = 0
        while i < len(s):
            m = CoinCollector._TOKEN.match(s, i)
            if not m:
                i += 1
                continue
            qty = int(m.group(1))
            code = m.group(2).lower().strip()
            if code in CoinCollector._VALUES:
                total += qty * CoinCollector._VALUES[code]
            i = m.end()
        return total
