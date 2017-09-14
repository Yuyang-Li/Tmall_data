import datetime
import os

index = 'H:/CPPdata/JDDeep_2017-05/JDData'

def change_type(y1,m1,d1,y2,m2,d2):
    begin = datetime.date(
        y1,m1,d1)
    end = datetime.date(y2,m2,d2)
    for i in range((end-begin).days+1):
        date = begin + datetime.timedelta(days=i)
        fold = '{}_{}'.format(index,str(date))
        files = os.listdir(fold)
        for f in files:
            sort = f[-5:-4]
            if sort == '0':
                pass
            else:
                name = os.path.join(fold,f)
                os.remove(name)




def main():
    change_type(2017,5,20,2017,5,31)

if __name__ == '__main__':
    main()
