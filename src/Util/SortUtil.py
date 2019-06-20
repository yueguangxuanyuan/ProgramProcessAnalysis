import copy

class AttriImportanceSort :

    _attriNameArray = None;
    _attriImportanceArray = None;
    _sortRule = 1; #1代表升序，否则为降序

    def __init__(self):
        pass

    def _sort_it(self,_start,_end):
        if _start >= _end :
            return ;

        _value = self._attriImportanceArray[_start];
        _name_value = self._attriNameArray[_start];

        _emptyIndex = _start;
        for _index in range(_start+1,_end):
            judgeCondition = False;
            if self._sortRule == 1:
                judgeCondition = self._attriImportanceArray[_index] < _value;
            else:
                judgeCondition = self._attriImportanceArray[_index] > _value;

            if judgeCondition:
                self._attriImportanceArray[_emptyIndex] = self._attriImportanceArray[_index];
                self._attriNameArray[_emptyIndex] = self._attriNameArray[_index];
                _emptyIndex += 1;
                self._attriImportanceArray[_index] = self._attriImportanceArray[_emptyIndex];
                self._attriNameArray[_index] = self._attriNameArray[_emptyIndex];

        self._attriImportanceArray[_emptyIndex] = _value;
        self._attriNameArray[_emptyIndex] = _name_value;

        self._sort_it(_start,_emptyIndex);
        self._sort_it(_emptyIndex+1,_end);


    def sort(self,InAttriNameArray,InAttriImportanceArray,sortRule=1):
        self._attriNameArray = copy.copy(InAttriNameArray);
        self._attriImportanceArray =copy.copy(InAttriImportanceArray);
        self._sortRule = sortRule;

        self._sort_it(0,self._attriNameArray.__len__());

        return self._attriNameArray,self._attriImportanceArray;


if __name__ == "__main__":
    sortor =AttriImportanceSort();

    x,y = sortor.sort([2,3,1],[8,7,6],0);

    print(x);
    print(y);