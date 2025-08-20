import random
from decimal import Decimal, ROUND_HALF_UP

class BankUtility:

    @staticmethod
    def promptUserForString(prompt):
        while True:
            s = input(prompt).strip()
            if s:
                return s
            print("Input cannot be empty. Try again.")

    @staticmethod
    def promptUserForPositiveNumber(prompt):
        while True:
            s = input(prompt).strip().replace("$", "")
            try:
                val = float(s)
                if val > 0:
                    return val
                print("Please enter a number greater than 0.")
            except ValueError:
                print("Invalid number. Please try again.")

    @staticmethod
    def convertFromDollarsToCents(amount):
        """
        Convert a dollar amount (float/int/str) to an int # of cents,
        rounding half-up (e.g., 19.995 -> 2000).
        """
        cents = int(Decimal(str(amount)).scaleb(2).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        return cents

    @staticmethod
    def generateRandomInteger(low, high):
        return random.randint(low, high)

    @staticmethod
    def isNumeric(numberToCheck):
        try:
            return numberToCheck.isdigit()
        except Exception:
            return False
