### 使用说明

- 在右上角的搜索栏中搜索电影、影人、类型
- 搜索可以为精准搜索、部分搜索以及模糊搜索
- 在导航栏的类型选项中能选择相应的类型
- 在导航栏中的排行榜选项中可以查看点击量排行榜以及评分排行榜
- 在搜索时点击搜索结果可以进入详情界面
- 详情界面可以查看电影的详细信息以及给电影打分

### 部分实现

- 最主要的数据结构为B+树，为电影名、人名以及类型各建立了一棵B+树，精确搜索时直接使用B+树的查找取出结果
- 部分搜索是遍历所有元素暴力匹配
- 模糊搜索使用fuzzwuzzy库实现获取两个字符串相关度，在暴力比较后将结果送入最大堆，最后结果取前30名
- 点击量和评分均采用一个有序数组辅助记录，每次修改后在数组上二分寻找所在位置以及该插入的位置，从而维护点击量和评分的排行
- web框架使用flask
- 数据集来自豆瓣top250

### Instructions for use

- Search for movies, filmmakers, types in the search bar in the upper right corner

- Search can be precise search, partial search and fuzzy search

- The corresponding type can be selected in the type option of the navigation bar

- In the leaderboard option in the navigation bar, you can view the click through leaderboard and scoring leaderboard

- When searching, click the search result to enter the details interface

- In the details interface, you can view the details of the movie and score the movie

### Partial implementation

- The main data structure is the B + tree. A B + tree is established for movie name, person name and type. The search results of the B + tree are directly used in accurate search

- Partial search is to traverse all elements to match

- Fuzzy search uses the fuzzywuzzy library to obtain the correlation between two strings. After violent comparison, the results are sent to the maximum heap, and the final results are the top 30

- The hits and scores are recorded in an ordered array. After each modification, the binary score on the array is used to find the location and the inserted location, so as to maintain the ranking of hits and scores

- Web framework using flaks

- The data set is from Douban top250