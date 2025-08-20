from Bank import Bank
from BankUtility import BankUtility
from CoinCollector import CoinCollector
from decimal import Decimal, ROUND_HALF_UP

class BankManager:
    def __init__(self):
        self.bank = Bank()
        self.run()

    # ------------- generic prompts -------------
    def _prompt_for_ssn9(self) -> str:
        while True:
            ssn = BankUtility.promptUserForString("Enter 9-digit SSN (digits only): ")
            if ssn.isdigit() and len(ssn) == 9:
                return ssn
            print("Invalid SSN. Please enter exactly 9 digits (no dashes).")

    def _prompt_for_account_number(self) -> int:
        while True:
            s = BankUtility.promptUserForString("Enter 8-digit account number: ")
            if s.isdigit() and len(s) == 8 and s[0] != "0":
                return int(s)
            print("Invalid account number. It must be 8 digits and cannot start with 0.")

    def _prompt_for_pin(self) -> str:
        while True:
            p = BankUtility.promptUserForString("Enter 4-digit PIN: ")
            if p.isdigit() and len(p) == 4:
                return p
            print("Invalid PIN format. Please enter exactly 4 digits.")

    def _verify_account_with_pin(self):
        """Prompt for account number + PIN. Return (acct) or None."""
        acct_num = self._prompt_for_account_number()
        acct = self.bank.findAccount(acct_num)
        if not acct:
            print("No account found with that number.\n")
            return None
        for attempt in range(1, 4):
            pin = self._prompt_for_pin()
            if acct.isValidPIN(pin):
                return acct
            left = 3 - attempt
            print(f"Incorrect PIN. {left} attempt(s) remaining." if left else "Incorrect PIN. Returning to main menu.\n")
            if left == 0:
                return None
        return None

    def _format_cents(self, cents: int) -> str:
        dollars = cents // 100
        cents_only = cents % 100
        return f"${dollars:,}.{cents_only:02d}"

    # ---------- Option 1: Open account ----------
    def open_account_flow(self):
        if self.bank.isFull():
            print("Sorry—the bank is full. Cannot open more accounts.")
            return

        print("\n--- Open an Account ---")
        first = BankUtility.promptUserForString("First name: ")
        last  = BankUtility.promptUserForString("Last name: ")
        ssn9  = self._prompt_for_ssn9()

        acct = self.bank.openAccount(first, last, ssn9)

        print("\nAccount created successfully!\n")
        print(acct)
        print("\nSave this information securely:")
        print(f"  Account Number: {acct.getAccountNumber()}")
        print(f"  PIN:            {acct.getPIN()}\n")

    # ---------- Option 2: Info & balance ----------
    def info_and_balance_flow(self):
        print("\n--- Account Information & Balance ---")
        acct = self._verify_account_with_pin()
        if acct:
            print("\nAccount found:\n")
            print(acct)
            print()

    # ---------- Option 3: Change PIN ----------
    def change_pin_flow(self):
        print("\n--- Change PIN ---")
        acct = self._verify_account_with_pin()
        if not acct:
            return

        while True:
            new_pin = self._prompt_for_pin()
            if new_pin == acct.getPIN():
                print("New PIN cannot be the same as the current PIN.")
                continue
            confirm = BankUtility.promptUserForString("Re-enter new PIN to confirm: ")
            if confirm != new_pin:
                print("PINs do not match. Try again.")
                continue
            acct.setPIN(new_pin)
            print("PIN updated successfully.\n")
            return

    # ---------- Option 4: Deposit ----------
    def deposit_flow(self):
        print("\n--- Deposit Money ---")
        acct = self._verify_account_with_pin()
        if not acct:
            return
        dollars = BankUtility.promptUserForPositiveNumber("Enter amount to deposit (in dollars): $")
        cents = BankUtility.convertFromDollarsToCents(dollars)
        new_bal = acct.deposit(cents)
        print(f"Deposit successful. New balance: {self._format_cents(new_bal)}\n")

    # ---------- Option 5: Transfer between accounts ----------
    def transfer_flow(self):
        print("\n--- Transfer Money Between Accounts ---")
        print("Source account:")
        src = self._verify_account_with_pin()
        if not src:
            return

        print("Destination account:")
        dst_num = self._prompt_for_account_number()
        dst = self.bank.findAccount(dst_num)
        if not dst:
            print("No destination account found with that number.\n")
            return
        if dst.getAccountNumber() == src.getAccountNumber():
            print("Cannot transfer to the same account.\n")
            return

        dollars = BankUtility.promptUserForPositiveNumber("Enter transfer amount (in dollars): $")
        amount_cents = BankUtility.convertFromDollarsToCents(dollars)

        if src.getBalanceInCents() < amount_cents:
            print(f"Insufficient funds. Current balance: {self._format_cents(src.getBalanceInCents())}\n")
            return

        src.withdraw(amount_cents)
        dst.deposit(amount_cents)
        print(f"Transfer successful.")
        print(f"Source new balance: {self._format_cents(src.getBalanceInCents())}")
        print(f"Destination new balance: {self._format_cents(dst.getBalanceInCents())}\n")

    # ---------- Option 6: Withdraw ----------
    def withdraw_flow(self):
        print("\n--- Withdraw Money ---")
        acct = self._verify_account_with_pin()
        if not acct:
            return
        dollars = BankUtility.promptUserForPositiveNumber("Enter amount to withdraw (in dollars): $")
        amount_cents = BankUtility.convertFromDollarsToCents(dollars)

        if acct.getBalanceInCents() < amount_cents:
            print(f"Insufficient funds. Current balance: {self._format_cents(acct.getBalanceInCents())}\n")
            return

        new_bal = acct.withdraw(amount_cents)
        print(f"Withdrawal successful. New balance: {self._format_cents(new_bal)}\n")

    # ---------- Option 7: ATM withdrawal (bill breakdown) ----------
    def atm_withdrawal_flow(self):
        """
        Greedy breakdown with $50, $20, $10, $5, $1 bills.
        Adjust denominations here if your assignment specifies differently.
        """
        print("\n--- ATM Withdrawal ---")
        acct = self._verify_account_with_pin()
        if not acct:
            return

        dollars = BankUtility.promptUserForPositiveNumber("Enter cash amount to withdraw (whole dollars): $")
        # Enforce whole-dollar withdrawal
        if Decimal(str(dollars)).quantize(Decimal("1"), rounding=ROUND_HALF_UP) != Decimal(str(dollars)):
            print("ATM can only dispense whole dollars. Try again.\n")
            return

        cents = BankUtility.convertFromDollarsToCents(dollars)
        if acct.getBalanceInCents() < cents:
            print(f"Insufficient funds. Current balance: {self._format_cents(acct.getBalanceInCents())}\n")
            return

        # Bill breakdown
        remaining = int(dollars)
        breakdown = {}
        for bill in [50, 20, 10, 5, 1]:
            qty = remaining // bill
            if qty:
                breakdown[bill] = qty
                remaining -= qty * bill

        # Complete withdrawal
        acct.withdraw(cents)

        # Print breakdown
        print("Dispensed:")
        for bill in [50, 20, 10, 5, 1]:
            if bill in breakdown:
                print(f"  ${bill}: {breakdown[bill]}")
        print(f"New balance: {self._format_cents(acct.getBalanceInCents())}\n")

    # ---------- Option 8: Deposit change (coins) ----------
    def deposit_change_flow(self):
        print("\n--- Deposit Change ---")
        acct = self._verify_account_with_pin()
        if not acct:
            return
        coin_str = BankUtility.promptUserForString(
            "Enter coins (e.g., '10q 3d 7n 5p', supports p/n/d/q/h/w): "
        )
        cents = CoinCollector.parseChange(coin_str)
        if cents <= 0:
            print("No valid coins detected. Nothing deposited.\n")
            return
        new_bal = acct.deposit(cents)
        print(f"Deposited {self._format_cents(cents)} in coins. New balance: {self._format_cents(new_bal)}\n")

    # ---------- Option 9: Close an account ----------
    def close_account_flow(self):
        print("\n--- Close Account ---")
        acct = self._verify_account_with_pin()
        if not acct:
            return

        bal = acct.getBalanceInCents()
        if bal != 0:
            print(f"Account must have a zero balance to close (current: {self._format_cents(bal)}).\n")
            return

        removed = self.bank.removeAccountFromBank(acct.getAccountNumber())
        if removed:
            print("Account closed successfully.\n")
        else:
            print("Unexpected error closing account.\n")

    # ---------- Option 10: Add monthly interest to all accounts ----------
    def add_monthly_interest_flow(self):
        """
        Prompts for an ANNUAL interest rate (e.g., 3.6 for 3.6% APR),
        computes monthly rate = APR/12, applies to all accounts, rounding half-up to cents.
        """
        print("\n--- Add Monthly Interest to All Accounts ---")
        # Accept positive (can be zero if you wish)
        while True:
            s = BankUtility.promptUserForString("Enter ANNUAL interest rate as a percent (e.g., 3.6): ")
            try:
                apr = float(s)
                if apr < 0:
                    print("Rate cannot be negative.")
                    continue
                break
            except ValueError:
                print("Invalid rate. Try again.")

        monthly_rate = Decimal(str(apr)) / Decimal("1200")  # apr% / 12 months
        updated = 0
        for acct in self.bank.getAllAccounts():
            bal_cents = acct.getBalanceInCents()
            if bal_cents <= 0:
                continue
            bal = Decimal(bal_cents) / Decimal(100)
            interest = (bal * monthly_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            interest_cents = int((interest * Decimal(100)).to_integral_value(rounding=ROUND_HALF_UP))
            if interest_cents > 0:
                acct.deposit(interest_cents)
                updated += 1

        print(f"Applied monthly interest at {apr}% APR to {updated} account(s).\n")

    # ------------- main loop -------------
    def run(self):
        while True:
            print("=" * 60)
            print("What do you want to do?")
            print("1. Open an account")
            print("2. Get account information and balance")
            print("3. Change PIN")
            print("4. Deposit money in account")
            print("5. Transfer money between accounts")
            print("6. Withdraw money from account")
            print("7. ATM withdrawal")
            print("8. Deposit change")
            print("9. Close an account")
            print("10. Add monthly interest to all accounts")
            print("11. End Program")
            print("=" * 60)

            choice = input("Enter choice: ").strip()
            if choice == "11":
                print("Goodbye!")
                break
            elif choice == "1":
                self.open_account_flow()
            elif choice == "2":
                self.info_and_balance_flow()
            elif choice == "3":
                self.change_pin_flow()
            elif choice == "4":
                self.deposit_flow()
            elif choice == "5":
                self.transfer_flow()
            elif choice == "6":
                self.withdraw_flow()
            elif choice == "7":
                self.atm_withdrawal_flow()
            elif choice == "8":
                self.deposit_change_flow()
            elif choice == "9":
                self.close_account_flow()
            elif choice == "10":
                self.add_monthly_interest_flow()
            else:
                print("Invalid choice")

if __name__ == "__main__":
    BankManager()
