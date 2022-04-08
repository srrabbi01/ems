def calcAmountFunc(cost,prct):
    if cost and prct:
        return (cost*prct)/100
    else:
        return cost