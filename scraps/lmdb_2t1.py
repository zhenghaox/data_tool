# coding=utf-8
# filename: merge_lmdb.py

import lmdb

# 将两个lmdb文件合并成一个新的lmdb
def merge_lmdb(lmdb1, lmdb2, result_lmdb):

    print 'Merge start!'

    # env代表Environment, txn代表Transaction

    # 打开lmdb文件，读模式
    env_1 = lmdb.open(lmdb1)
    env_2 = lmdb.open(lmdb2)

    # 创建事务
    txn_1 = env_1.begin()
    txn_2 = env_2.begin()

    # 打开数据库
    database_1 = txn_1.cursor()
    database_2 = txn_2.cursor()

    # 打开lmdb文件，写模式，
    env_3 = lmdb.open(result_lmdb, map_size=int(1e12))
    txn_3 = env_3.begin(write=True)

    count = 0
    # 遍历数据库
    for (key, value) in database_1:
        # 将数据放到结果数据库事务中
        txn_3.put(key, value)
        count=count+1
        if(count % 1000 == 0):
            # 将数据写入数据库，必须的，否则数据不会写入到数据库中
            txn_3.commit()
            count = 0
            txn_3 = env_3.begin(write=True)

    if(count % 1000 != 0):
        txn_3.commit()
        count = 0
        txn_3 = env_3.begin(write=True)

    for (key, value) in database_2:
        txn_3.put(key, value)
        if(count % 1000 == 0):
            txn_3.commit()
            count = 0
            txn_3 = env_3.begin(write=True)

    if(count % 1000 != 0):
        txn_3.commit()
        count = 0
        txn_3 = env_3.begin(write=True)

    # 关闭lmdb
    env_1.close()
    env_2.close()
    env_3.close()

    print 'Merge success!'

    # 输出结果lmdb的状态信息，可以看到数据是否合并成功
    print env_3.stat()

def main():
    #fr = open('lmdb.txt')
    # lmdb1的目录
    #lmdb1 = fr.readline().strip()
    # lmdb2的目录
    #lmdb2 = fr.readline().strip()
    # result lmdb的目录
    #result_lmdb = fr.readline().strip()
    #fr.close()
    lmdb2='/media/e/weizhang/data/XC/done/all/lmdb0925_2_320/traffictrain_train_lmdb0925_2_320'
    lmdb1='/media/e/weizhang/data/BDdone/all2/lmdb0911_2_320/traffictrain_train_lmdb0911_2_320'
    result_lmdb='/media/e/weizhang/data/XC/done/XC+BD/XC+BD_0925'
    merge_lmdb(lmdb1, lmdb2, result_lmdb)

if __name__ == '__main__':
    main()