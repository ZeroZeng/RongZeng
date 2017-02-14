from collections import OrderedDict
import csv
import datetime,time

class DataFrame(object):

    @classmethod
    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        with open(file_path, 'rU') as infile:
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)
            data = []

            for row in reader:
                data.append(row)

            return cls(list_of_lists=data)

    def __init__(self, list_of_lists, header=True):
        if header:
            self.header = list_of_lists[0]
            self.data = list_of_lists[1:]
        else:
            self.header = ['column' + str(index + 1) for index, column in enumerate(list_of_lists[0])]
            self.data = list_of_lists



        ############# HW2 task 1 #############
        if len(self.header) != len(set(self.header)):
            raise Exception('There are duplicates!!!')
        ############# end task 1 #############

        ############# HW2 task 2 #############
        self.data=[[s.strip() for s in row] for row in self.data]
        ############# end task 2 #############

        self.data = [OrderedDict(zip(self.header, row)) for row in self.data]

    def __getitem__(self, item):
        # this is for rows only
        if isinstance(item, (int, slice)):
            return self.data[item]

        # this is for columns only
        elif isinstance(item, str):
            return [row[item] for row in self.data]

        # this is for rows and columns
        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):

                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in rowz]
                    elif all([isinstance(thing,str) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in rowz]
                    else:
                        raise TypeError('What the hell is this?')

                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rowz]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1],str):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

        # only for lists of column names
        elif isinstance(item, list):
            return [[row[column_name] for column_name in item] for row in self.data]

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]

    ############# HW2 task 3 #############
    
    def min(self,col_name):
        try:
            nums = [float(row[col_name].replace(',','')) for row in self.data]
            print min(nums)
        except ValueError:
            try:
                nums=[datetime.datetime.strptime(row[col_name], '%m/%d/%y %H:%M') for row in self.data]
                nums=[time.mktime(num.timetuple()) for num in nums]
                print time.strftime('%m-%d-%y %H:%M',time.localtime(min(nums)))
            except:    
                print ('Cannot be calculated')

    def max(self,col_name):
        try:
            nums = [float(row[col_name].replace(',','')) for row in self.data]
            print max(nums)
        except ValueError:
            try:
                nums=[datetime.datetime.strptime(row[col_name], '%m/%d/%y %H:%M') for row in self.data]
                nums=[time.mktime(num.timetuple()) for num in nums]
                print time.strftime('%m-%d-%y %H:%M',time.localtime(max(nums)))
            except:    
                print ('Cannot be calculated')

    def median(self,col_name):
        try:
            nums = [float(row[col_name].replace(',','')) for row in self.data]
            nums = sorted(nums)
            center = int(len(nums) / 2)
            if len(nums) % 2 == 0:
                print sum(nums[center - 1:center + 1]) / 2.0
            else:
                print nums[center]
        except ValueError:
            try:
                nums=[datetime.datetime.strptime(row[col_name], '%m/%d/%y %H:%M') for row in self.data]
                nums=[time.mktime(num.timetuple()) for num in nums]
                nums = sorted(nums)
                center = int(len(nums) / 2)
                if len(nums) % 2 == 0:
                    print time.strftime('%m-%d-%y %H:%M',time.localtime(sum(nums[center - 1:center + 1]) / 2.0))
                else:
                    print time.strftime('%m-%d-%y %H:%M',time.localtime(nums[center]))
            except:
                print ('Cannot be calculated')


    def mean(self,col_name):
        try:
            nums = [float(row[col_name].replace(',','')) for row in self.data]
            count = len(nums)
            print sum(nums) / count
        except ValueError:
            try:
                nums=[datetime.datetime.strptime(row[col_name], '%m/%d/%y %H:%M') for row in self.data]
                nums=[time.mktime(num.timetuple()) for num in nums]
                count = len(nums)
                print time.strftime('%m-%d-%y %H:%M',time.localtime(sum(nums) / count))                
            except:
                print ('Cannot be calculated')

    def sum(self,col_name):
        try:
            nums = [float(row[col_name].replace(',','')) for row in self.data]
            print sum(nums)
        except ValueError:
            print ('Cannot be calculated')

    def std(self,col_name):
        try:
            nums = [float(row[col_name].replace(',','')) for row in self.data]
            mean = sum(nums)/len(nums)
            print  sum((x-mean)**2/len(nums) for x in nums)**0.5
        except ValueError:
            print ('Cannot be calculated')

    ############# end task 3 #############

    ############# HW2 task 4 #############
    
    def add_rows(self, list_of_lists):
        for new_list in list_of_lists:
            if len(new_list) == len(self.header):
                new_row = [OrderedDict(zip(self.header, row)) for row in list_of_lists]
                self.data = self.data + new_row
                return self
            else:
                print ('Wrong number of len')
    ############# end task 4 #############

    ############# HW2 task 5 #############
    
    def add_column(self, list_of_lists,col_name):
        # type: (object, object) -> object
        if len(list_of_lists) == len(self.data):
            self.header=self.header+col_name
            new_col_dict = [OrderedDict(zip(col_name,row)) for row in list_of_lists]
            for l in range(len(self.data)):
                for rowz in self.data:
                    rowz = self.data[l].update(new_col_dict[l]) 
            return self
        else:
            print ("Wrong number of column")
    ############# end task 5 #############



#
# infile = open('SalesJan2009.csv')
# lines = infile.readlines()
# lines = lines[0].split('\r')
# data = [l.split(',') for l in lines]
# things = lines[559].split('"')
# data[559] = things[0].split(',')[:-1] + [things[1]] + things[-1].split(',')[1:]
#
#
#
#
#
#
# # get the 5th row
# fifth = df[4]
# sliced = df[4:10]
#
# # get item definition for df [row, column]
#
# # get the third column
# tupled = df[:, 2]
# tupled_slices = df[0:5, :3]
#
# tupled_bits = df[[1, 4], [1, 4]]
#
#
# # adding header for data with no header
# df = DataFrame(list_of_lists=data[1:], header=False)
#
# # fetch columns by name
# named = df['column1']
# named_multi = df[['column1', 'column7']]
#
# #fetch rows and (columns by name)
# named_rows_and_columns = df[:5, 'column7']
# named_rows_and_multi_columns = df[:5, ['column4', 'column7']]
#
#
# #testing from_csv class method
# df = DataFrame.from_csv('SalesJan2009.csv')
# rows = df.get_rows_where_column_has_value('Payment_Type', 'Visa')
# indices = df.get_rows_where_column_has_value('Payment_Type', 'Visa', index_only=True)
#
# rows_way2 = df[indices, ['Product', 'City']]
#
#
#
# df = DataFrame.from_csv('SalesJan2009.csv')
# # ============test task 3============
# x='Last_Login'
# test1 = df.min(x)
# test2 = df.max(x)
# test3 = df.median(x)
# test4 = df.sum(x)
# test5 = df.mean(x)
# test6 = df.std(x)
# # ============test task 4============
# new_row = df[1:3]
# new_rowz = df.add_rows(new_row)
# print (new_rowz)
# # ============test task 5============
# new_col = df[:,:3]
# add_col = df.add_column(new_col,new_col[0])
# print (add_col)
