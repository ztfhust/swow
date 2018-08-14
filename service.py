from flask import Flask
import tushare as ts

app = Flask(__name__)

@app.route('/')
def showcase():
    all_codes = get_all_stocks_code()
    for k in all_codes.keys():
        dd_buy(all_codes[k], 2)   

def get_all_data():
    return ts.get_today_all()

def get_all_stocks_code():
    return get_all_data()['code'].to_dict()

# big deals happen for specified days
def dd_buy(code, day):
    dd = ts.get_sina_dd(code, date = '2018-8-10')
    buy_vol = dd[dd.type=='买盘']['volume'].to_dict()
    sel_vol = dd[dd.type=='卖盘']['volume'].to_dict()

    total_buy = 0
    total_sel = 0
    for k in buy_vol.keys():
        total_buy += buy_vol[k]
    
    for k in sel_vol.keys():
        total_sel += sel_vol[k]

    if total_buy - total_sel > 0 :
        return True

    print (total_buy)
    print (total_sel )   

# if this stock drops for specified days
def drop_for_days(code, day):
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 80,debug = True)