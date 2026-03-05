import os, yfinance as yf, pandas as pd, ast

# 取得 GitHub 傳入的資訊
issue_title = os.getenv('ISSUE_TITLE', '').lower()
user_name = os.getenv('USER_NAME', 'Unknown')
db_path = 'stock_game_db.csv'

def get_price(symbol):
    try:
        return round(yf.Ticker(symbol).fast_info['last_price'], 2)
    except: return None

# 讀取資料
df = pd.read_csv(db_path, index_col=0) if os.path.exists(db_path) else pd.DataFrame(columns=['cash', 'portfolio'])
if user_name not in df.index: df.loc[user_name] = [100000.0, "{}"]

try:
    # 解析指令，例: "buy aapl 10"
    parts = issue_title.split()
    action, symbol, qty = parts[0], parts[1].upper(), int(parts[2])
    price = get_price(symbol)
    if price:
        cash, portfolio = float(df.loc[user_name, 'cash']), ast.literal_eval(df.loc[user_name, 'portfolio'])
        if action == 'buy' and cash >= price * qty:
            df.at[user_name, 'cash'], portfolio[symbol] = cash - price * qty, portfolio.get(symbol, 0) + qty
        elif action == 'sell' and portfolio.get(symbol, 0) >= qty:
            df.at[user_name, 'cash'], portfolio[symbol] = cash + price * qty, portfolio[symbol] - qty
            if portfolio[symbol] == 0: del portfolio[symbol]
        df.at[user_name, 'portfolio'] = str(portfolio)
        df.to_csv(db_path)
except Exception as e: print(f"Error: {e}")
