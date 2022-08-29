# @Author: lym12321
# @Date: 2022-08-29

from requests import session
import json

requests = session() # 这样可以存 cookie，用法与 requests 相同

baseUrl = '' # 服务器 api 地址

headers = {'Content-Type' : 'application/json'}

# 固定的接口返回格式
def ret(code, msg):
    return {'code': code, 'msg': msg}

# 登入系统
# username: 用户名
# password: 密码
def login(username, password):
    data = {
        'strUserName': username,
        'strPassword': password,
        'strParameters': 'type=worker,client=REST|0.01'
    }
    try:
        r = requests.post(f'{baseUrl}/login', data=json.dumps(data), headers=headers)
        j = json.loads(r.text)
        if j['LoginResult']['ErrorCode'] != 0:
            return ret(j['LoginResult']['ErrorCode'], j['LoginResult']['ErrorInfo'])
        return ret(0, j)
    except Exception as e:
        return ret(-1, e)

# 登出系统
def logout():    
    try:
        r = requests.post(f'{baseUrl}/logout')
        return ret(0, json.loads(r.text))
    except Exception as e:
        return ret(-1, e)

# 获取读者信息
# barcode: 读者证条码号
# retType: 返回信息格式
def getReaderInfo(barcode, retType):
    data = {
        'strBarcode': barcode,
        'strResultTypeList': retType
    }
    try:
        r = requests.post(f'{baseUrl}/getReaderInfo', data=json.dumps(data), headers=headers)
        j = json.loads(r.text)
        if j['GetReaderInfoResult']['ErrorCode'] != 0:
            return ret(j['GetReaderInfoResult']['ErrorCode'], j['GetReaderInfoResult']['ErrorInfo'])
        return ret(0, j['results'][0])
    except Exception as e:
        return ret(-1, e)

# 获取书籍摘要
def getBiblioSummary(barcode):
    data = {
        'strItemBarcode': barcode
    }
    try:
        r = requests.post(f'{baseUrl}/getBiblioSummary', data=json.dumps(data), headers=headers)
        j = json.loads(r.text)
        if j['GetBiblioSummaryResult']['ErrorCode'] != 0:
            return ret(j['GetBiblioSummaryResult']['ErrorCode'], j['GetBiblioSummaryResult']['ErrorInfo'])
        return ret(0, j)
    except Exception as e:
        return ret(-1, e)

# 获取书籍详细信息
# retType: xml/html/@price/@accessno
def getBiblioInfo(recPath, retType):
    data = {
        'strBiblioRecPath': recPath,
        'strBiblioType': retType
    }
    try:
        r = requests.post(f'{baseUrl}/getBiblioInfo', data=json.dumps(data), headers=headers)
        j = json.loads(r.text)
        if j['GetBiblioInfoResult']['ErrorCode'] != 0:
            return ret(j['GetBiblioInfoResult']['ErrorCode'], j['GetBiblioInfoResult']['ErrorInfo'])
        return ret(0, j['strBiblio'])
    except Exception as e:
        return ret(-1, e)

# 借书或续借
# reader: 读者证条码号
# barcode: 书籍册条码号
# 若 cont = True，则为续借操作
def Borrow(reader, barcode, cont = False):
    data = {
        'bRenew': cont,
        'strReaderBarcode': reader,
        'strItemBarcode': barcode,
        'bForce': False
    }
    try:
        r = requests.post(f'{baseUrl}/Borrow', data=json.dumps(data), headers=headers)
        j = json.loads(r.text)
        if j['BorrowResult']['ErrorCode'] != 0:
            return ret(j['BorrowResult']['ErrorCode'], j['BorrowResult']['ErrorInfo'])
        return ret(0, j)
    except Exception as e:
        return ret(-1, e)

# 还书
# barcode: 书籍条码号
def Return(barcode):
    data = {
        'strAction': 'return',
        'strItemBarcode': barcode
    }
    try:
        r = requests.post(f'{baseUrl}/Return', data=json.dumps(data), headers=headers)
        j = json.loads(r.text)
        if j['ReturnResult']['ErrorCode'] != 0:
            return ret(j['ReturnResult']['ErrorCode'], j['ReturnResult']['ErrorInfo'])
        return ret(0, j)
    except Exception as e:
        return ret(-1, e)

# 检索读者记录，保存到结果集（默认为 default）
# keyword: 检索词
# matchStyle: 匹配方式（left/middle/right/exact）
# matchFrom: 检索途径（<all>/证条码号/姓名/...）
# @return: 命中条数
def searchReader(keyword, matchStyle = 'middle', matchFrom = '<all>', resultSetName = 'default'):
    data = {
        'strReaderDbNames': '<all>',
        'strQueryWord': keyword,
        'nPerMax': -1,
        'strFrom': matchFrom,
        'strMatchStyle': matchStyle,
        'strResultSetName': resultSetName
    }
    try:
        r = requests.post(f'{baseUrl}/searchReader', data=json.dumps(data), headers=headers)
        j = json.loads(r.text)
        if j['SearchReaderResult']['ErrorCode'] != 0:
            return ret(j['SearchReaderResult']['ErrorCode'], j['SearchReaderResult']['ErrorInfo'])
        return ret(0, j['SearchReaderResult']['Value'])
    except Exception as e:
        return ret(-1, e)

# 检索书目
# keyword: 检索词
# matchStyle: 匹配方式（left/middle/right/exact）
# matchFrom: 检索途径（<all>/ISBN/题名/...）
# @return: 命中条数
def searchBiblio(keyword, matchStyle = 'middle', matchFrom = '<all>', resultSetName = 'default'):
    data = {
        'strBiblioDbNames': '<all>',
        'strQueryWord': keyword,
        'nPerMax': -1,
        'strFromStyle': matchFrom,
        'strMatchStyle': matchStyle,
        'strResultSetName': resultSetName
    }
    try:
        r = requests.post(f'{baseUrl}/searchBiblio', data=json.dumps(data), headers=headers)
        j = json.loads(r.text)
        if j['SearchBiblioResult']['ErrorCode'] != 0:
            return ret(j['SearchBiblioResult']['ErrorCode'], j['SearchBiblioResult']['ErrorInfo'])
        return ret(0, j['SearchBiblioResult']['Value'])
    except Exception as e:
        return ret(-1, e)

# 从结果集中指定起点获取指定数量的检索结果
# start: 记录起点，从 0 开始
# count: 记录数量，当 count = -1 时，获取尽可能多的结果
# 对于读者库来说，@return: [{'Cols': [证条码号, 姓名, 状态, 读者类别, 单位, 身份证号, 证号, 失效期]}]
# 对于书库来说，@return: [{'Cols': [路径, 题名, 作者, 出版社, 出版时间, 中图法分类号, 主题词, 关键词, ISBN]}]
def getSearchResult(start, count, resultSetName = 'default'):
    data = {
        'strResultSetName': resultSetName,
        'lStart': start,
        'lCount': count,
        'strBrowseInfoStyle': 'id,cols'
    }
    try:
        r = requests.post(f'{baseUrl}/getSearchResult', data=json.dumps(data), headers=headers)
        j = json.loads(r.text)
        if j['GetSearchResultResult']['ErrorCode'] != 0:
            return ret(j['GetSearchResultResult']['ErrorCode'], j['GetSearchResultResult']['ErrorInfo'])
        return ret(0, {'count': j['GetSearchResultResult']['Value'], 'results': j['searchresults']})
    except Exception as e:
        return ret(-1, e)

# 获得同一书目记录下的若干册记录信息
# recPath: 书目路径
# start: 查询起点，从 0 开始
# count: 查询数量，当 count = -1 时，获取尽可能多的结果
def getEntities(recPath, start, count):
    data = {
        'strBiblioRecPath': recPath,
        'lStart': start,
        'lCount': count,
        'strStyle': 'onlygetpath'
    }
    try:
        r = requests.post(f'{baseUrl}/getEntities', data=json.dumps(data), headers=headers)
        j = json.loads(r.text)
        if j['GetEntitiesResult']['ErrorCode'] != 0:
            return ret(j['GetEntitiesResult']['ErrorCode'], j['GetEntitiesResult']['ErrorInfo'])
        return ret(0, {'count': j['GetEntitiesResult']['Value'], 'results': j['entityinfos']})
    except Exception as e:
        return ret(-1, e)

# 获得实体记录信息
# barcode: 实体条码
# retType: 返回类型
def getItemInfo(barcode, retType):
    data = {
        'strBarcode': barcode,
        'strResultType': retType
    }
    try:
        r = requests.post(f'{baseUrl}/getItemInfo', data=json.dumps(data), headers=headers)
        j = json.loads(r.text)
        if j['GetItemInfoResult']['ErrorCode'] != 0:
            return ret(j['GetItemInfoResult']['ErrorCode'], j['GetItemInfoResult']['ErrorInfo'])
        # return ret(0, {'count': j['GetItemInfoResult']['Value'], 'results': j['entityinfos']})
        return ret(0, j['strResult'])
    except Exception as e:
        return ret(-1, e)
