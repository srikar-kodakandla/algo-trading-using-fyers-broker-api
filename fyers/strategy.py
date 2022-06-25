import os 
try:
    os.system('rm intimate.txt')
    os.system('rm ticks.db')
except:
    print('There is an error in removing cache files ...')    
count=0
while count<60:
    count+=1
    try:
        stoploss=1 # percentage
        percent=100 # percentage of funds to be used to trade
        margin=3
        adx_limit=2
        emergency_start=False
        emergency_do_not_stop=False
        first_order=True
        try:
            read=open('stock_selection.txt','r')
        except:
            read = open('fyers/stock_selection.txt', 'r')
        stock_name=read.read().split('\n')
        read.close()
        stock_name=stock_name[0]
        #from fyers.broker_allow_stocks import allow
        #allowed_stocks=allow(stock_name)
        #stock_name=allowed_stocks[1]
        from fyers.accounts_login import login_accounts
        from common.indicator import SuperTrend
        from time import sleep
        import time
        from common import message as m
        import sys
        from fyers.order import order
        import datetime
        from fyers.script import name_to_script
        from fyers.quote import quote
        from fyers.stoploss_percentage import percentage
        from fyers.live import full_data
        import pandas as pd
        import os
        from time import sleep
        import ta
        name_script=name_to_script(stock_name)
        try:
            ddd=open('supertrend_values.txt','r').read().split('\n')
        except:
            try:
                ddd=open(f"supertrend_txt/{name_script.split(':')[1].split('-')[0]}.txt")
            except:
                ddd=open('supertrend_values_default.txt','r').read().split('\n')
        period=int(ddd[0])
        multiplier=float(ddd[1])
        accounts=login_accounts()
        m.message(f'{name_script} is selected and supertrend values {period} and {multiplier} are selected for today trading')
        intimate=open('intimate.txt','w')
        intimate.write('False')
        intimate.close()
        sleep(7)
        l=full_data(accounts[0])
        #data=l.full_data(stock_name)
        #data5=l.full_data(stock_name,resolution=5)
        fyers=accounts[0].fyers
        print(fyers.funds())
        q=quote(accounts[0])
        o=order(accounts[0])
        data = l.full_data(stock_name,days=5)
        data5=l.full_data(stock_name,resolution=5,days=5)
        wait=False 
        while not wait: 
            wait=((0 <= time.localtime().tm_wday <= 4) and (datetime.datetime.strptime( 
                    datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 09:16:00", 
                    "%d-%m-%Y %H:%M:%S") <= datetime.datetime.now())) 
            print('waiting market to open (strategy)')         
            if wait: 
                break 
            if emergency_start: 
                break 
            #print('waiting') 
            sleep(1)

        while True:
            sleep(4)
            data = l.full_data(stock_name,days=5)
            data5=l.full_data(stock_name,resolution=5,days=5)
            old_trend=SuperTrend(data,period,multiplier)[f'STX_{period}_{multiplier}'][-2]
            new_trend=SuperTrend(data,period,multiplier)[f'STX_{period}_{multiplier}'][-1]
            pl=fyers.positions()['overall']['pl_total']
            print("P and L is ",pl)
            if pl<-50:
                o.sell(stock_name)
                m.message('Loss is more , so trading stopped !!!')
                import sys 
                sys.exit()
            if pl>300:
                o.sell(stock_name)
                m.message('profit is more , so trading stopped !!!')
                import sys 
                sys.exit()

            print('supertrend value :',SuperTrend(data,period,multiplier))
            #print(data[-1])
            adx_value=ta.trend.ADXIndicator(data5['high'],data5['low'], data5['close'], 14,  False).adx()[-1]
            print(new_trend)
            try:
                current_order=o.position_symbol()[0][name_script]
            except:
                current_order=None
            if ((0 <= time.localtime().tm_wday <= 4) and (datetime.datetime.strptime(
                    datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 09:16:00",
                    "%d-%m-%Y %H:%M:%S") <= datetime.datetime.now() <= datetime.datetime.strptime(
                datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 09:17:00",
                "%d-%m-%Y %H:%M:%S"))) and first_order:
                first_order=False
                if new_trend=='up': #buy_sell=1
                    o.buy(stock_name,buy_sell=-1, qty=o.no_of_stocks(stock_name, percent, margin))
                if new_trend=='down':#buy_sell=-1
                    o.buy(stock_name, buy_sell=1, qty=o.no_of_stocks(stock_name, percent, margin))
            if (old_trend=='down' and new_trend=='up' ) or (new_trend=='up' and (current_order==1)): #change it to 1 #or current_order==None)):
                if current_order!=-1: #change to -1
                    try:
                        o.sell(stock_name)
                    except:
                        print(' No order to sell now ')
                    if adx_value>=adx_limit:
                        o.buy(stock_name,buy_sell=-1,qty=o.no_of_stocks(stock_name,percent,margin))
                        sleep(30)
            if (old_trend=='up' and new_trend=='down') or (new_trend=='down' and (current_order==-1)): #chnge it to 1 # or current_order==None)):
                if current_order!=1: #change it to -1
                    try:
                        o.sell(stock_name)
                    except:
                        print("No order to sell now ")

                    if adx_value>=adx_limit:
                        o.buy(stock_name,buy_sell=1,qty=o.no_of_stocks(stock_name,percent,margin))
                        sleep(30)
            if ((0 <= time.localtime().tm_wday <= 4) and (datetime.datetime.strptime(
                    datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 15:14:50",
                    "%d-%m-%Y %H:%M:%S") <= datetime.datetime.now() <= datetime.datetime.strptime(
                datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 15:30:00",
                "%d-%m-%Y %H:%M:%S"))) or emergency_do_not_stop:
                try:
                    for i in o.position_symbol()[1].keys():
                        o.sell(i)
                except:
                    m.message("There are no positions to sell ")
                try:
                    m.message('Today Trading stopped ! ')
                    m.message(f"Today P and L is {fyers.positions()['overall']['pl_realized']}")
                    try:
                        os.system('rm intimate.txt')
                        os.system('rm stock_selection.txt')
                        os.system,('rm ticks.db')
                        import sys
                        sys.exit()
                    except Exception as error:
                        print(error)
                    import sys 
                    sys.exit()
                except:
                    print('unable to fetch P and L ')
                    import sys
                    sys.exit()
                sys.exit()
                break
            #except Exception as error :
            #   m.message(f'There is an error in strategy , This is the error {error}')

        m.message('came outside loop , this should not happen during market hours , please check the error occured ')
    except Exception as error:
        if str(error)=="[Errno 2] No such file or directory: 'fyers/stock_selection.txt'":
            print('error stopped')
            break
        m.message(f"There is an error in trading strategy , Trying again... , The error is : {error}")
        sleep(10)

m.message("Final Call , it won't try again There is an error in trading strategy , please check or please contact srikar , Trading stopped for today .")

