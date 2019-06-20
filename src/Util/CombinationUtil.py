class GetColCombination:
    _colNameArray = [];
    _compositeNum = 1;

    _colArraySize = 0;
    _preComposite = [];
    _currentIndex= -1 ;

    def __init__(self,_colNameArray):
        self._colNameArray = _colNameArray;

    def _initParams(self):
        self._colArraySize = self._colNameArray.__len__();
        self._preComposite = [];
        for i in range(self._compositeNum):
            self._preComposite.append(0);
        self._currentIndex = -1;

    def setCompositeNum(self,n):
        self._compositeNum = n;
        self._initParams();

    def _convertIndexArrayToColNameArray(self):
        colNameArray = [];
        for index in self._preComposite:
            colNameArray.append(self._colNameArray[index]);
        return colNameArray;

    def getNextComposite(self):
        if self._preComposite.__len__() == 0:
            self._preComposite.append(0);

        needFound = True;
        canBeFound = True;
        while (needFound and canBeFound):
            needRevert = False;
            #按照正常的顺序，尝试找到一种组合
            if(self._currentIndex < self._compositeNum-1):
                self._currentIndex += 1;
                preVal = -1;
                if  self._currentIndex != 0 :
                    preVal = self._preComposite[self._currentIndex-1];
                currentVal = preVal+1;
                if (self._colArraySize - currentVal -1) < (self._compositeNum - self._currentIndex -1):
                    #可分配的个数小于待分配的个数
                    needRevert = True;
                else:
                    self._preComposite[self._currentIndex] = currentVal;
                    if(self._currentIndex == self._compositeNum -1):
                        needFound = False;
            elif (self._currentIndex == self._compositeNum -1):
                #如果仅在当前位置上调整
                preVal = self._preComposite[self._currentIndex];
                currentVal = preVal + 1;
                if(currentVal < self._colArraySize):
                    self._preComposite[self._currentIndex] = currentVal;
                    needFound = False;
                else:
                    needRevert = True;

            if needRevert:
                while needRevert :
                    self._currentIndex -= 1;
                    if(self._currentIndex == -1):
                        canBeFound = False;
                        break;

                    currentVal = self._preComposite[self._currentIndex];
                    newVal = currentVal+1;
                    if (self._colArraySize - newVal - 1) < (self._compositeNum - self._currentIndex - 1):
                        # 可分配的个数小于待分配的个数
                        needRevert = True;
                    else:
                        self._preComposite[self._currentIndex] = newVal;
                        needRevert = False;

        if not needFound :
            return True,self._convertIndexArrayToColNameArray();
        else:
            return False,[];