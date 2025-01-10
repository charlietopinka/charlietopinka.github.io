import requests
from bs4 import BeautifulSoup
from Exceptions import *
import re
from Stock import *

class Finance_App:
    current_balance = 0.0

    formatted_dict = {}
    def __init__(self):
        self.previewed_balance = 0.0
        
        self.google_search = False
        self.running = False

    def confirm_submit(self):
        while True:
            input_string = input("Confirm submit? (yes/no): ").strip().lower()
            input_string = re.sub(r'[^a-z]', '', input_string)
            if input_string in ["yes", "no"]:
                return input_string
            print("Please enter 'yes' or 'no'")

    def correct_stock_searched(self, stock):
        
        
        while True:
            input_string = input("Is this the stock you are looking for? (yes/no): ").strip().lower()
            input_string = re.sub(r'[^a-z]', '', input_string)
            if input_string == "no":
                return False
            elif input_string == "yes":
                return True
            print("Please enter 'yes' or 'no'.")

    def remove_stock(self, stock):
        Finance_App.formatted_dict.pop(stock.name, None)
    def get_max_shares(self, stock):
        return int(Finance_App.current_balance // stock.price)
 
        
    def run(self):
        print("Type 'quit' at any time to stop")

        while True:
            if not self.running:
                self.running = True
                Finance_App.current_balance = self.get_valid_float_input("Enter current balance: ", "Balance cannot be negative.")
                self.previewed_balance = Finance_App.current_balance

            while True:
             
                abbr_or_name = input("Enter a stock abbreviation or name: ").strip()

                if abbr_or_name.lower() == 'exit' or abbr_or_name.lower() == 'quit':
                    print("Exiting the program. Goodbye!")
                    quit()

                if not abbr_or_name:
                    print("Invalid input. Please enter a valid stock name or abbreviation.")
                    continue

                if abbr_or_name.replace('.', '', abbr_or_name.count(".")).isdigit():
                    print("Invalid input. Please enter a valid stock name or abbreviation.")
                    continue

                try:
                    stock = self.search_stock(abbr_or_name)
                except Exception as e:
                    print(f"Error searching for stock: {e}")
                    continue

                if stock:
                    try:
                        correct = self.correct_stock_searched(stock)
                    except Exception as e:
                        print(f"Error confirming stock: {e}")
                        continue

                    if correct:
                        print(f"Stock {stock.name} ({stock.abbr}) selected")
                        break 
                    else:
                        
                        continue
                else:
                    print("Stock not found. Please try again.")
                    continue

            while True:
                max_shares = self.get_max_shares(stock)
                if max_shares > 1:
                    print(f"Maximum shares available for purchase: {max_shares} shares")
                elif max_shares == 1:
                    print(f"Maximum shares available for purchase: {max_shares} share")
                shares = self.get_valid_int_input("Enter the number of shares you want to buy: ", "Shares must be a positive integer.")
                stock.price = self.get_price_of_stock(stock.abbr)
                stock.total = shares * stock.price
                
                
                
                
                if Finance_App.current_balance >= stock.total:
                    self.preview_balance(stock)
                    if self.confirm_submit() == "yes":
                        Finance_App.current_balance -= stock.total
                        self.add_stock(stock, shares)
                        print("Transaction completed.")
                    else:
                        print("Transaction cancelled.")
                    break
                else:
                    print(f"Insufficient funds to buy {shares} shares of {stock.name}")
                    break

            self.print_stock_list()
            self.print_current_balance()

    def preview_balance(self, stock):
        preview_balance = Finance_App.current_balance - stock.total
        print(f"Preview balance after transaction: ${preview_balance:.2f}")
    def get_daily_change(self, stock):
        url = f"https://finance.yahoo.com/quote/{stock.abbr}/"
           
    
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        daily_change = soup.find('fin-streamer', {'class': 'priceChange'})
        if daily_change != None:
            percent_change_text = daily_change.text.strip()
            return percent_change_text
    def add_stock(self, stock, additional_shares):
        if not stock.name:
            print("Invalid stock name.")
            return

        if stock.name not in Finance_App.formatted_dict:
            Finance_App.formatted_dict[stock.name] = {
                "abbr": stock.abbr,
                "price": f"${stock.price:.2f}",
                "shares": additional_shares,
                "total": f"${stock.total:.2f}",
                "daily change:": f"{stock.daily_change} ({stock.percent_change:.2f}%)"
                
            }
            print(Finance_App.formatted_dict)
        else:
            stock.shares = Finance_App.formatted_dict[stock.name]['shares'] + additional_shares
            stock.total = stock.shares * stock.price
            Finance_App.formatted_dict[stock.name].update({
                "shares": additional_shares,
                "total": f"{(additional_shares * stock.price):.2f}"})
            
            print(Finance_App.formatted_dict)
            Finance_App.formatted_dict[stock.name].update({
                "shares": stock.shares,
                "total": f"${stock.total:,.2f}"
            })

    def get_valid_float_input(self, prompt, error_message):
        while True:
            user_input = input(prompt).strip()
            if user_input.lower() == "quit":
                quit()
            try:
                value = float(user_input)
                if value < 0:
                    raise ValueError(error_message)
                return value
            except ValueError:
                
                print("Must enter a positive number")
                

    def get_valid_int_input(self, prompt, error_message):
        while True:
            user_input = input(prompt).strip()
            if user_input.lower() == "quit":
                quit()
            try:
                value = int(user_input)
                if value <= 0:
                    raise ValueError(error_message)
                return value
            except ValueError:
                print(error_message)

   
    def search_stock(self, abbr_or_name):
        
        
        if not abbr_or_name:
            print("Invalid input. Please enter a valid stock name or abbreviation")
            return None
        
        if abbr_or_name.lower() == "quit":
            quit()
        try:
            
            return self.search(abbr_or_name)
        except SearchError as e:
            print(e)
            return None

    def search(self, abbr_or_name):
        print("Searching for stock...")

        if not abbr_or_name:
            print("Invalid input. Please enter a valid stock name or abbreviation.")
            return None

        if abbr_or_name.lower() == "quit":
            quit()

        try:
            stock_name = self.search_google_finance(abbr_or_name)
            if stock_name is None:
                abbr_or_name = abbr_or_name.lower().title()
                stock_abbr = self.search_bing(abbr_or_name)

                if stock_abbr is None:
                    print(f"Stock symbol or name '{abbr_or_name}' not found.")
                    return None
                else:
                    stock_name = abbr_or_name
            else:
                stock_abbr = abbr_or_name.upper()

            stock = Stock(name=stock_name, abbr=stock_abbr)
            stock.price = self.get_price_of_stock(stock.abbr)
            stock.percent_change = self.get_percent_change(stock)
            stock.daily_change = self.get_daily_change(stock)

            if stock.price == 0.0:
                print(f"Could not retrieve price for stock {stock.name} ({stock.abbr}).")
                return None

            print(f"Stock found: {stock.name} ({stock.abbr}) - ${stock.price:.2f} per share ({stock.daily_change}) ({stock.percent_change:.2f}%) ")
            return stock

        except Exception as e:
            print(f"Error during stock search: {e}")
            return None


    def search_google_finance(self, company_symbol_or_name):
        self.google_search = True
        url1 = f"https://www.google.com/finance/quote/{company_symbol_or_name}:NASDAQ"
        url2 = f"https://www.google.com/finance/quote/{company_symbol_or_name}:NYSE"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        for url in [url1, url2]:
            try:
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.content, 'html.parser')
                name_tag = soup.find('div', {'class': 'zzDege'})
                if name_tag:
                    return name_tag.text.strip()
            except:
                pass
        return None

    def search_bing(self, company_symbol_or_name):
        self.google_search = False
        url_name = company_symbol_or_name.strip().replace(" ", "%20")
        url = f"https://www.bing.com/search?q={url_name}%20stock%20symbol&FORM=ARPSEC&PC=ARPL&PTAG=30530222"
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        try:
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            symbol_tag = soup.find('div', {'class': 'enti_stxt b_demoteText'})
            if symbol_tag:
                return self.clean_symbol(symbol_tag.text.strip())
        except:
            pass
        return None

    def clean_symbol(self, symbol):
        return symbol.replace("NASDAQ: ", "").replace("NYSE: ", "").strip()

    def get_price_of_stock(self, abbr):
        url1 = f"https://www.google.com/finance/quote/{abbr}:NASDAQ"
        url2 = f"https://www.google.com/finance/quote/{abbr}:NYSE"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        for url in [url1, url2]:
            try:
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.content, 'html.parser')
                price_tag = soup.find('div', {'class': 'YMlKec fxKbKc'})
                if price_tag:
                    price = float(price_tag.text.strip().replace('$', '').replace(',', ''))
                    
                    return price
            except:
                pass
        return 0.0

    def print_stock_list(self):
        if Finance_App.formatted_dict:
            print("Your Stocks:")
            print(Finance_App.formatted_dict)
        else:
            print("Your stocks: None")

    def print_current_balance(self):
        print(f"Current Balance: ${Finance_App.current_balance:.2f}")
    

    def get_percent_change(self, stock):
        try:
            url = f"https://finance.yahoo.com/quote/{stock.abbr}/"
           
        
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            percent_change_tag = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})

            if percent_change_tag:
                percent_change = percent_change_tag.get('data-value')
                if percent_change:
                    return float(percent_change)

                print("Percent change not found.")
                return 0.0

        except Exception as e:
            print(f"Error fetching percent change: {e}")
            return 0.0



            









