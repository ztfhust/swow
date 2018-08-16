from flask import Flask
import tushare as ts

app = Flask(__name__)

@app.route('/')
def showcase():
    days = 2
    trade_days_dict = getPastTradeDays(days)
    all_codes = get_all_stocks_code()
    print ('\nbig deal and price dropped for ' + str(days) + ' days as below:')
    
    for k in all_codes.keys():
        #print ('process:'+ all_codes[k])
        result = dd_buy(all_codes[k], trade_days_dict)
        result2 = drop_for_days(all_codes[k], days)
        if result == True and result2 == True:
            print ('--->result code:' + all_codes[k])
           

def get_all_data():
    return ts.get_today_all()

def get_all_stocks_code():
    return get_all_data()['code'].to_dict()

def getPastTradeDays(days):
    sh_hist_data = ts.get_hist_data('sh')['close']    
    return sh_hist_data[0:days].to_dict()

# big deals happen for specified days
def dd_buy(code, trade_days_dict):
    result = True
    
    for day in trade_days_dict.keys():    
        dd = ts.get_sina_dd(code, date = day, vol= 500)

        if dd is None:
            result = False
            break
        
        buy_vol = dd[dd.type=='买盘']['volume'].to_dict()
        sel_vol = dd[dd.type=='卖盘']['volume'].to_dict()

        total_buy = 0
        total_sel = 0
        for k in buy_vol.keys():
            total_buy += buy_vol[k]
        
        for k in sel_vol.keys():
            total_sel += sel_vol[k]

        if total_buy - total_sel < 0 :
            result = False
            break
        
    return result
ts.get_hist_data('600848')

# if this stock drops for specified days
def drop_for_days(code, days):     
    price_dict = ts.get_hist_data(code)[0:days]['p_change'].to_dict()
    if price_dict is None:
        return True

    result = True
    for k in price_dict.keys():
        if price_dict[k] > 0:
            result = False
            break

    return result        


if __name__ == '__main__':
    #app.run(host='0.0.0.0',port = 80,debug = True)
    showcase()
