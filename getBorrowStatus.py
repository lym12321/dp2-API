# @Author: lym12321
# @Date: 2022-08-21
# @Note: 遍历读者库，输出在借状态

import api
import json

r = api.login('username', 'password')
if r['code'] != 0:
    print(r['msg'])
    exit()

count = api.searchReader('X202101', 'left')['msg']
print(f"共找到 {count} 条记录.")

r = api.getSearchResult(0, -1)

for item in r['msg']['results']:
    readerInfo = json.loads(api.getReaderInfo(item['Cols'][0], 'json')['msg'])
    if 'borrows' in readerInfo and 'borrow' in readerInfo['borrows']:
        if '@barcode' in readerInfo['borrows']['borrow']: count = 1
        else: count = len(readerInfo['borrows']['borrow'])
        print(f"[{item['Cols'][0]}]{item['Cols'][1]} 在借 {count} 本")
        if count == 1: print(f"\t[{readerInfo['borrows']['borrow']['@barcode']}]")
        else:
            for i in readerInfo['borrows']['borrow']:
                print(f"\t[{i['@barcode']}]")

api.logout()