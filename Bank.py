from Account import Account
from BankUtility import BankUtility

class Bank:
    MAX_ACCOUNTS = 100

    def __init__(self):
        # Use a dict for O(1) lookups by account number
        self._accounts = {}  # {int accountNumber -> Account}

    # ---------- Introspection ----------
    def countAccounts(self) -> int:
        return len(self._accounts)

    def isFull(self) -> bool:
        return self.countAccounts() >= Bank.MAX_ACCOUNTS

    def getAllAccounts(self):
        # Returns a list (copy) so external code can iterate safely
        return list(self._accounts.values())

    # ---------- Core operations ----------
    def addAccountToBank(self, account: Account) -> bool:
        """
        Add an Account object to the bank.
        Returns True if added, False if bank is full or accountNumber already exists.
        """
        if self.isFull():
            return False
        acct_num = account.getAccountNumber()
        if acct_num is None:
            raise ValueError("Account must have an account number before adding to bank.")
        if acct_num in self._accounts:
            return False
        self._accounts[acct_num] = account
        return True

    def removeAccountFromBank(self, accountNumber: int) -> bool:
        """
        Remove an account by number. Returns True if removed, False if not found.
        """
        return self._accounts.pop(int(accountNumber), None) is not None

    def findAccount(self, accountNumber: int) -> Account | None:
        """
        Find an account by number. Returns the Account or None.
        """
        return self._accounts.get(int(accountNumber))

    # ---------- Safe generators (unique within this bank) ----------
    def generateUniqueAccountNumber(self) -> int:
        """
        Generate an 8-digit account number (first digit non-zero) that is unique in the bank.
        """
        if self.isFull():
            raise RuntimeError("Bank is full; cannot generate new account number.")
        while True:
            # 8-digit, first digit non-zero
            num = BankUtility.generateRandomInteger(10000000, 99999999)
            if num not in self._accounts:
                return num

    def generateRandomPIN(self) -> str:
        """
        Generate a 4-digit PIN string (can start with 0), e.g. '0319'.
        """
        pin_int = BankUtility.generateRandomInteger(0, 9999)
        return f"{pin_int:04d}"

    # ---------- Optional helper (convenience for account creation) ----------
    def openAccount(self, first: str, last: str, ssn9: str) -> Account:
        """
        Create a new Account object with generated account number and PIN.
        NOTE: Does not take any initial deposit; caller can deposit later.
        """
        if self.isFull():
            raise RuntimeError("Bank is full; cannot open another account.")

        a = Account()
        a.setOwnerFirstName(first)
        a.setOwnerLastName(last)
        a.setOwnerSSN(ssn9)

        acct_num = self.generateUniqueAccountNumber()
        pin = self.generateRandomPIN()
        a.setAccountNumber(acct_num)
        a.setPIN(pin)
        a.setBalanceInCents(0)

        added = self.addAccountToBank(a)
        if not added:
            # Extremely unlikely due to uniqueness check, but handle gracefully
            raise RuntimeError("Failed to add newly created account to bank.")
        return a
