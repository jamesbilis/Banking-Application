class Account:
    def __init__(self):
        # Required attributes (see spec)
        self._accountNumber = None          # int, 8 digits (set later via setter)
        self._ownerFirstName = ""           # str
        self._ownerLastName = ""            # str
        self._ownerSSN = ""                 # str, 9 digits
        self._pin = ""                      # str, 4 digits, may start with 0
        self._balanceInCents = 0            # int, store money in cents

    # -------- Getters --------
    def getAccountNumber(self): return self._accountNumber
    def getOwnerFirstName(self): return self._ownerFirstName
    def getOwnerLastName(self): return self._ownerLastName
    def getOwnerSSN(self): return self._ownerSSN
    def getPIN(self): return self._pin
    def getBalanceInCents(self): return self._balanceInCents

    # -------- Setters --------
    # Keep validation light; generation/validation logic happens in BankManager/BankUtility per spec.
    def setAccountNumber(self, num: int):
        self._accountNumber = int(num)

    def setOwnerFirstName(self, name: str):
        self._ownerFirstName = str(name)

    def setOwnerLastName(self, name: str):
        self._ownerLastName = str(name)

    def setOwnerSSN(self, ssn: str):
        # Store as 9-digit string; masking happens in __repr__
        self._ownerSSN = str(ssn)

    def setPIN(self, pin: str):
        # Store as 4-char string; can start with '0'
        self._pin = str(pin)

    def setBalanceInCents(self, cents: int):
        self._balanceInCents = int(cents)

    # -------- Banking actions --------
    def deposit(self, amountInCents: int) -> int:
        """
        Add amountInCents (int) to balance and return new balance (int).
        Spec: deposit/withdraw take and return cents.  :contentReference[oaicite:2]{index=2}
        """
        self._balanceInCents += int(amountInCents)
        return self._balanceInCents

    def withdraw(self, amountInCents: int) -> int:
        """
        Subtract amountInCents (int) from balance and return new balance (int).
        NOTE: Caller (BankManager) should enforce 'insufficient funds' before calling,
        per project’s error-handling examples.  :contentReference[oaicite:3]{index=3}
        """
        self._balanceInCents -= int(amountInCents)
        return self._balanceInCents

    def isValidPIN(self, pin: str) -> bool:
        """
        Return True if the provided PIN matches the account PIN.  :contentReference[oaicite:4]{index=4}
        """
        return str(pin) == self._pin

    # -------- Helpers --------
    def _masked_ssn(self) -> str:
        """
        Format SSN like XXX-XX-#### as shown in the sample outputs.  :contentReference[oaicite:5]{index=5}
        """
        s = self._ownerSSN
        last4 = s[-4:] if len(s) >= 4 else s
        return f"XXX-XX-{last4}"

    def _formatted_balance(self) -> str:
        dollars = self._balanceInCents // 100
        cents = self._balanceInCents % 100
        return f"${dollars:,}.{cents:02d}"

    # Provide formatted string like the sample printout in the PDF.  :contentReference[oaicite:6]{index=6}
    def __repr__(self):
        lines = [
            "============================================================",
            f"Account Number: {self._accountNumber if self._accountNumber is not None else ''}",
            f"Owner First Name: {self._ownerFirstName}",
            f"Owner Last Name: {self._ownerLastName}",
            f"Owner SSN: {self._masked_ssn()}",
            f"PIN: {self._pin}",
            f"Balance: {self._formatted_balance()}",
            "============================================================",
        ]
        return "\n\n".join(lines)
