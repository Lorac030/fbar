# FBAR Calculator (Foreign Bank and Financial Accounts Report)
## Video Demo: https://www.youtube.com/watch?v=P2TYoUW8WTs

## Introduction

Foreign Bank and Financial Accounts Report (FBAR) is a report that people who reside in the US have to file if they have a cash assets on foreign financial accounts where balances together exceeds $10,000 at any time during a year. The report is filed with the Financial Crimes Enforcement Network (FinCEN), a bureau of the US Department of the Treasury.

FBAR helps the US government to detect and prevent financial crimes like money laundering, tax evasion, and more. FBAR rules apply to a wide range of financial accounts, including bank accounts, brokerage accounts, mutual funds, and trusts.

FBAR reporting requirements are complex and there are severe penalties if someone fails to follow the rules. Therefore, it's essential to accurately calculate and validate if you need to file a FBAR form.

FBAR is a command-line tool that can help you to calculate and discover if you need to file a FBAR form. In the next sections, I will explain how to it.

## The Problem

The process of reporting a FBAR can be a long and manual task. Every year, some people need to calculate their bank account balances and convert them to a specific exchange rate, which is different every year. The exchange rate can be difficult to find and because of that the process gets even more complicated.

After gathering all correct and necessary information from all balances, the person needs to manually add them and then convert it into the specific exchange rate required for that year's report. Depending on the amount you need to calculate this calculation process can be time-consuming and easy to make mistakes, so it important to take extra care when filling a FBAR form.

## My Motivation

As someone who is currently taking programming lessons, my motivation to write a program to calculate FBAR using Python is driven by a desire to apply my newfound skills to a real-world problem. The process of learning to code can be both challenging and rewarding, and I believe that one of the best ways to solidify my understanding of programming concepts is to put them into practice by building something that is both useful and relevant.

In addition to the educational benefits of writing a program to calculate FBAR, I am also motivated by the practical implications of the program. As someone who has foreign bank accounts, I understand the importance of complying with FBAR reporting requirements in order to avoid potential legal and financial consequences. By creating a program that simplifies the process of calculating FBAR balances and determining whether or not an FBAR form is required, I can help others who may be in a similar situation to mine to stay on top of their financial reporting obligations.

Finally, I am motivated by the challenge of building a program that is both accurate and user-friendly. The process of designing and coding a program involves a lot of trial and error, and requires attention to detail and problem-solving skills. By working on this project, I am not only gaining experience in programming, but also in project management and communication, as I need to clearly define the program's requirements, design the user interface, and ensure that the program is easy to use and understand.

## Installation

To use FBAR, you will need to have Python 3 installed on your computer. You can then download the `fbar.py` file and run it in your command line. Please pay attention to the file called `Pipfile`, which includes mandatory dependencies to be also installed. It is recommended to install all dependencies with `pipenv`

```
$ pipenv shell # if you have not initialized the virtual env yet
$ pipenv install
```

## Usage

FBAR runs without parameters, but will ask initially:
- Year for the tax return (i.e the year you are filing your returns for)
- Country name
- Current currency name used on that country
- Current currency symbol

After providing this initial information, the system will prompt you to enter the name of each bank and the respective balance. You need to enter one bank name and balance at a time, and press enter after each input. The balance should be entered as a number without decimals, just the rounded value to the nearest integer value.

Once you have entered all bank names and balances, the system will calculate the sum of all balances, convert the sum to US dollars using the dollar exchange rate for December 31st of the specified year, and validate it against FBAR rules.

If the total value of your foreign financial accounts in US dollars exceeds $10,000, the system will indicate that you need to file a FBAR form. Otherwise, the system will indicate that you do not need to file a FBAR form.

## Usage Example

### FBAR may be needed

```
lorac@laptop:~/code/fbar$ python app.py
-----------------------------
FBAR Calculator
-----------------------------

Tax Return Year (like 2021): 2022
Country of where your assets are (like Brazil): Brazil
Currency Name for Brazil (like Real): Real
Currency Symbol for that country (like R$): R$

Enter bank name (leave blank to finish): Itau
- Enter highest balance on 2022 in R$ for Itau: 10000
Enter bank name (leave blank to finish): Bradesco
- Enter highest balance on 2022 in R$ for Bradesco: 30000
Enter bank name (leave blank to finish): Banco do Brasil
- Enter highest balance on 2022 in R$ for Banco do Brasil: 50000
Enter bank name (leave blank to finish):

Dolar to Real Treasury reference for 2022 is R$5.286

+--------+-----------------+------------------+-------------------+
|   Year | Bank Name       |   Currency in R$ |   Currency in US$ |
+========+=================+==================+===================+
|   2022 | Itau            |         10000.00 |           1891.79 |
+--------+-----------------+------------------+-------------------+
|   2022 | Bradesco        |         30000.00 |           5675.37 |
+--------+-----------------+------------------+-------------------+
|   2022 | Banco do Brasil |         50000.00 |           9458.95 |
+--------+-----------------+------------------+-------------------+

Total balance of R$90000.00 on 2022 was equivalent to US$17026.11
As it exceeds US$10,000 you MAY NEED to file an FBAR form on April of 2023.
Please go to https://bsaefiling.fincen.treas.gov/NoRegFBARFiler.html and type all asset values there for online FBAR filing.
```

### FBAR may NOT be needed

```
lorac@laptop:~/code/fbar$ python fbar.py
-----------------------------
FBAR Calculator
-----------------------------

Tax Return Year (like 2021): 2022
Country of where your assets are (like Brazil): Brazil
Currency Name for Brazil (like Real): Real
Currency Symbol for that country (like R$): R$

Enter bank name (leave blank to finish): Itau
- Enter highest balance on 2022 in R$ for Itau: 4000
Enter bank name (leave blank to finish): Bradesco
- Enter highest balance on 2022 in R$ for Bradesco: 5000
Enter bank name (leave blank to finish): Banco do Brasil
- Enter highest balance on 2022 in R$ for Banco do Brasil: 1000
Enter bank name (leave blank to finish):

Dolar to Real Treasury reference for 2022 is R$5.286

+--------+-----------------+------------------+-------------------+
|   Year | Bank Name       |   Currency in R$ |   Currency in US$ |
+========+=================+==================+===================+
|   2022 | Itau            |          4000.00 |            756.72 |
+--------+-----------------+------------------+-------------------+
|   2022 | Bradesco        |          5000.00 |            945.89 |
+--------+-----------------+------------------+-------------------+
|   2022 | Banco do Brasil |          1000.00 |            189.18 |
+--------+-----------------+------------------+-------------------+

Total balance of R$10000.00 on 2022 was equivalent to US$1891.79
As it does not exceed US$10,000 you may not need to file a FBAR form on April of 2023.
```

## FBAR rules

The FBAR rules are intricate and can change over time, making it crucial for individuals to remain updated with the latest guidance provided by the US Department of the Treasury. Ignorance of these rules can lead to severe penalties, making it essential to adhere to the guidelines set by the government.

When it comes to filing FBAR, individuals must keep a few critical points in mind. First and foremost, it is necessary to file the FBAR electronically using Form 114 with the Financial Crimes Enforcement Network (FinCEN). Secondly, the deadline for filing the FBAR is April 15th of the following year, but individuals can request an automatic extension until October 15th if needed.

Finally, the report should include specific details, such as the maximum account value during the year, the type of account, the account number, and the name and address of the foreign financial institution. These details should be accurate and up-to-date to avoid any legal repercussions.

In conclusion, it is vital to stay updated on the latest FBAR rules and regulations to ensure that you comply with the law. By adhering to the guidelines, individuals can avoid penalties and legal issues while ensuring that their financial accounts remain in good standing with the government.

## References

### The IRS website

The Internal Revenue Service (IRS) provides detailed information about FBAR reporting requirements and instructions for completing the FBAR form. You can find this information at https://www.irs.gov/businesses/small-businesses-self-employed/report-of-foreign-bank-and-financial-accounts-fbar.

### The FinCEN website

The Financial Crimes Enforcement Network (FinCEN) is the government agency responsible for collecting and analyzing information about financial transactions in order to combat money laundering and other financial crimes. FinCEN provides information about FBAR requirements and other financial reporting requirements on their website at https://www.fincen.gov/report-foreign-bank-and-financial-accounts.

## License

FBAR is licensed under the MIT License. See `LICENSE` for more information.
