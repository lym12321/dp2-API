# dp2-API

Encapsulated API for [dp2-Library](http://dp2003.cn/dp2portal/view.aspx)


### 函数定义

- `login(username, password)` 登入系统

- `logout()` 登出系统

- `getReaderInfo(barcode, retType)` 获取读者信息
  - `barcode`: 读者证条码号
  - `retType`: 返回信息格式（`json`/`xml`/`html`）

- `getBiblioSummary(barcode)` 获取书籍摘要
  - `barcode`: 册条码号

- `getBiblioInfo(recPath, retType)` 获取书籍详细信息
  - `recPath`: 书籍目录（可以由 `getBiblioSummary` 函数获取）
  - `retType`: 返回信息格式（`xml`/`html`/`text`）

- `Borrow(reader, barcode, cont = False)` 借阅/续借操作
  - `reader`: 读者证条码号
  - `barcode`: 册条码号
  - `cont`: 是否为续借操作（`True`/`False`）

- `Return(barcode)` 还书操作
  - `barcode`: 册条码号

- `searchReader(keyword, matchStyle = 'middle', matchFrom = '<all>', resultSetName = 'default')` 检索读者库，保存到指定结果集
  - `keyword`: 检索关键词
  - `matchStyle`: 匹配方式（`left`/`middle`/`right`/`exact`）
  - `matchFrom`: 检索途径（`<all>`/`证条码号`/`姓名`/...）
  - `resultSetName`: 结果集名称
  - `@return`: 命中条数

- `searchBiblio(keyword, matchStyle = 'middle', matchFrom = '<all>', resultSetName = 'default')` 检索书库，保存到指定结果集
  - `keyword`: 检索关键词
  - `matchStyle`: 匹配方式（`left`/`middle`/`right`/`exact`）
  - `matchFrom`: 检索途径（`<all>`/`ISBN`/`题名`/...） 
  - `resultSetName`: 结果集名称
  - `@return`: 命中条数

- `getSearchResult(start, count, resultSetName = 'default')` 从指定结果集中查询检索结果
  - `start`: 查询起点
  - `count`: 查询数量（当 `count = -1` 时，返回尽量多的结果）
  - `resultSetName`: 结果集名称

- `getEntities(recPath, start, count)` 获得同一书目记录下的若干册记录信息
  - `recPath`: 书目路径
  - `start`: 查询起点
  - `count`: 查询数量（当 `count = -1` 时，返回尽量多的结果）
  
- `getItemInfo(barcode, retType)` 获得实体记录信息
  - `barcode`: 实体条码
  - `retType`: 返回信息格式
