import axios from 'axios'

axios.defaults.headers.post['Content-Type'] = 'application/json'

function ret(code, msg){
    return {'code': code, 'msg': msg}
}

export async function login(username, password){
    let re = ret(-1, null)
    let data = {
        'strUserName': username,
        'strPassword': password,
        'strParameters': 'type=worker,client=REST|0.01'
    }
    await axios.post('./api/login', JSON.stringify(data)).then(function(r){
        if(r.data.LoginResult.ErrorCode != 0) re = ret(r.data.LoginResult.ErrorCode, r.data.LoginResult.ErrorInfo)
        else re = ret(0, r.data)
    }, function(err){
        re = ret(-1, err)
    })
    return re
}

export async function logout(){
    let re = ret(-1, null)
    await axios.post('./api/logout').then(function(r){
        if(r.data.LogoutResult.ErrorCode != 0) re = ret(r.data.LogoutResult.ErrorCode, r.data.LogoutResult.ErrorInfo)
        else re = ret(0, r.data)
    }, function(err){
        re = ret(-1, err)
    })
    return re
}

export async function getReaderInfo(barcode, retType){
    let re = ret(-1, null)
    let data = {
        'strBarcode': barcode,
        'strResultTypeList': retType
    }
    await axios.post('./api/getReaderInfo', JSON.stringify(data)).then(function(r){
        if(r.data.GetReaderInfoResult.ErrorCode != 0) re = ret(r.data.GetReaderInfoResult.ErrorCode, r.data.GetReaderInfoResult.ErrorInfo)
        else re = ret(0, r.data.results[0])
    }, function(err){
        re = ret(-1, err)
    })
    return re
}

export async function getBiblioSummary(barcode){
    let re = ret(-1, null)
    let data = {
        'strItemBarcode': barcode
    }
    await axios.post('./api/getBiblioSummary', JSON.stringify(data)).then(function(r){
        if(r.data.GetBiblioSummaryResult.ErrorCode != 0) re = ret(r.data.GetBiblioSummaryResult.ErrorCode, r.data.GetBiblioSummaryResult.ErrorInfo)
        else re = ret(0, r.data)
    }, function(err){
        re = ret(-1, err)
    })
    return re
}

export async function getBiblioInfo(recPath, retType){
    let re = ret(-1, null)
    let data = {
        'strBiblioRecPath': recPath,
        'strBiblioType': retType
    }
    await axios.post('./api/getBiblioInfo', JSON.stringify(data)).then(function(r){
        if(r.data.GetBiblioInfoResult.ErrorCode != 0) re = ret(r.data.GetBiblioInfoResult.ErrorCode, r.data.GetBiblioInfoResult.ErrorInfo)
        else re = ret(0, r.data.strBiblio)
    }, function(err){
        re = ret(-1, err)
    })
    return re
}

export async function Borrow(reader, barcode, cont = false){
    let re = ret(-1, null)
    let data = {
        'bRenew': cont,
        'strReaderBarcode': reader,
        'strItemBarcode': barcode,
        'bForce': false
    }
    await axios.post('./api/Borrow', JSON.stringify(data)).then(function(r){
        if(r.data.BorrowResult.ErrorCode != 0) re = ret(r.data.BorrowResult.ErrorCode, r.data.BorrowResult.ErrorInfo)
        else re = ret(0, r.data)
    }, function(err){
        re = ret(-1, err)
    })
    return re
}

export async function Return(barcode){
    let re = ret(-1, null)
    let data = {
        'strAction': 'return',
        'strItemBarcode': barcode
    }
    await axios.post('./api/Return', JSON.stringify(data)).then(function(r){
        if(r.data.ReturnResult.ErrorCode != 0) re = ret(r.data.ReturnResult.ErrorCode, r.data.ReturnResult.ErrorInfo)
        else re = ret(0, r.data)
    }, function(err){
        re = ret(-1, err)
    })
    return re
}

export async function searchReader(keyword, matchStyle = 'middle', matchFrom = '<all>', resultSetName = 'default'){
    let re = ret(-1, null)
    let data = {
        'strReaderDbNames': '<all>',
        'strQueryWord': keyword,
        'nPerMax': -1,
        'strFrom': matchFrom,
        'strMatchStyle': matchStyle,
        'strResultSetName': resultSetName
    }
    await axios.post('./api/searchReader', JSON.stringify(data)).then(function(r){
        if(r.data.SearchReaderResult.ErrorCode != 0) re = ret(r.data.SearchReaderResult.ErrorCode, r.data.SearchReaderResult.ErrorInfo)
        else re = ret(0, r.data.SearchReaderResult.Value)
    }, function(err){
        re = ret(-1, err)
    })
    return re
}

export async function searchBiblio(keyword, matchStyle = 'middle', matchFrom = '<all>', resultSetName = 'default'){
    let re = ret(-1, null)
    let data = {
        'strBiblioDbNames': '<all>',
        'strQueryWord': keyword,
        'nPerMax': -1,
        'strFromStyle': matchFrom,
        'strMatchStyle': matchStyle,
        'strResultSetName': resultSetName
    }
    await axios.post('./api/searchBiblio', JSON.stringify(data)).then(function(r){
        if(r.data.SearchBiblioResult.ErrorCode != 0) re = ret(r.data.SearchBiblioResult.ErrorCode, r.data.SearchBiblioResult.ErrorInfo)
        else re = ret(0, r.data.SearchBiblioResult.Value)
    }, function(err){
        re = ret(-1, err)
    })
    return re
}

export async function getSearchResult(start, count, resultSetName = 'default'){
    let re = ret(-1, null)
    let data = {
        'strResultSetName': resultSetName,
        'lStart': start,
        'lCount': count,
        'strBrowseInfoStyle': 'id,cols'
    }
    await axios.post('./api/getSearchResult', JSON.stringify(data)).then(function(r){
        if(r.data.GetSearchResultResult.ErrorCode != 0) re = ret(r.data.GetSearchResultResult.ErrorCode, r.data.GetSearchResultResult.ErrorInfo)
        else re = ret(0, {'count': r.data.GetSearchResultResult.Value, 'results': r.data.searchresults})
    }, function(err){
        re = ret(-1, err)
    })
    return re
}

export async function getEntities(recPath, start, count){
    let re = ret(-1, null)
    let data = {
        'strBiblioRecPath': recPath,
        'lStart': start,
        'lCount': count,
        'strStyle': 'onlygetpath'
    }
    await axios.post('./api/getEntities', JSON.stringify(data)).then(function(r){
        if(r.data.GetEntitiesResult.ErrorCode != 0) re = ret(r.data.GetEntitiesResult.ErrorCode, r.data.GetEntitiesResult.ErrorInfo)
        else re = ret(0, {'count': r.data.GetEntitiesResult.Value, 'results': r.data.entityinfos})
    }, function(err){
        re = ret(-1, err)
    })
    return re
}

export async function getItemInfo(barcode, retType){
    let re = ret(-1, null)
    let data = {
        'strBarcode': barcode,
        'strResultType': retType
    }
    await axios.post('./api/getItemInfo', JSON.stringify(data)).then(function(r){
        if(r.data.GetItemInfoResult.ErrorCode != 0) re = ret(r.data.GetItemInfoResult.ErrorCode, r.data.GetItemInfoResult.ErrorInfo)
        else re = ret(0, r.data.strResult)
    }, function(err){
        re = ret(-1, err)
    })
    return re
}
