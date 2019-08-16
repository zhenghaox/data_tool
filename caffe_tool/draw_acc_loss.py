import matplotlib.pyplot as plt

if __name__ == "__main__":
    iterations = []
    losses = []
    accs=[]
    logfile=open('/data_1/weizhang/train/all/classify/0815_44/log/log-2019-07-18-11-39-35.log')
    lines=logfile.readlines()
    for line in lines:
        line.strip()
        if line.find('Test net output #0: Accuracy1 =') != -1:
            words=line.split(' ')
            acc=words[-1]
            accs.append(acc)
        if line.find('Iteration') != -1:
            if line.find('loss') != -1:
                words1=line.split(' ')
                loss=words1[-1]
                losses.append(loss)
    plt.plot(losses)
    plt.show()
