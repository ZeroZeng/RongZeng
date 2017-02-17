from collections import OrderedDict
import csv
import datetime, time
import operator
from collections import defaultdict

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
        self.data = [[s.strip() for s in row] for row in self.data]

        ############# end task 2 #############

        def data_clean(self):

            for j in range(len(self[0])):
                for i in range(len(self)):
                    try:
                        self[i][j] = float(self[i][j].replace(',', ''))
                    except ValueError:
                        try:
                            self[i][j] = datetime.datetime.strptime(self[i][j], '%m/%d/%y %H:%M')
                        except:
                            pass
            return self

        self.data = [OrderedDict(zip(self.header, row)) for row in data_clean(self.data)]

    def __getitem__(self, item):
        # this is for rows only
        if isinstance(item, (int, slice)):
            return self.data[item]

        # this is for columns only
        elif isinstance(item, str):
            return Series([row[item] for row in self.data])

        # this is for rows and columns
        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):

                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [
                            [column_value for index, column_value in enumerate([value for value in row.itervalues()]) if
                             index in item[1]] for row in rowz]
                    elif all([isinstance(thing, str) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in rowz]
                    else:
                        raise TypeError('What the hell is this?')

                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rowz]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], str):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

        elif isinstance(item, list):
            if isinstance(item[0], str):

                return [[row[column_name] for column_name in item] for row in self.data]
                # else:
                #     print 'col_name is not exist.'
            elif isinstance(item[0], bool):
                list_ret = []
                result = zip(item, self.data)
                for row in result:
                    if row[0] == True:
                        list_ret.append(row[1:])
                return list_ret
            else:
                print 'Error'

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value == value]
        else:
            return [row for row in self.data if row[column_name] == value]

    ############# HW2 task 3 #############
    def col_type(self, col_name):
        try:
            test = float(self.data[0][col_name])
            result = [row[col_name] for row in self.data]
            col_type = 'Number'
            return result, col_type
        except ValueError:
            try:
                test = datetime.datetime.strptime(self.data[0][col_name], '%m/%d/%y %H:%M')
                result = [time.mktime(x.timetuple()) for x in row[col_name] for row in self.data]
                col_type = 'Date'
                return result, col_type
            except:
                result = [row[col_name] for row in self.data]
                col_type = 'Str'
                return result, col_type

    def min(self, col_name):
        result, col_type = self.col_type(col_name)
        if col_type == 'Number':
            print min(result)
        elif col_type == 'Date':
            print time.strftime('%m-%d-%y %H:%M', time.localtime(min(result)))
        else:
            print ('Cannot be calculated')

    def max(self, col_name):
        result, col_type = self.col_type(col_name)
        if col_type == 'Number':
            print max(result)
        elif col_type == 'Date':
            print time.strftime('%m-%d-%y %H:%M', time.localtime(max(result)))
        else:
            print ('Cannot be calculated')

    def median(self, col_name):
        result, col_type = self.col_type(col_name)
        nums = sorted(result)
        center = int(len(result) / 2)

        if len(result) % 2 == 0:
            even = 1
        else:
            even = 0

        if col_type == 'Number':
            if even == 0:
                print sum(result[center - 1:center + 1]) / 2.0
            else:
                print result[center]
        elif col_type == 'Date':
            if even == 0:
                print time.strftime('%m-%d-%y %H:%M', time.localtime(sum(result[center - 1:center + 1]) / 2.0))
            else:
                print time.strftime('%m-%d-%y %H:%M', time.localtime(result[center]))
        else:
            print ('Cannot be calculated')

    def mean(self, col_name):
        result, col_type = self.col_type(col_name)
        if col_type == 'Number':
            print sum(result) / len(result)
        elif col_type == 'Date':
            print time.strftime('%m-%d-%y %H:%M', time.localtime(sum(result) / len(result)))
        else:
            print ('Cannot be calculated')

    def sum(self, col_name):
        result, col_type = self.col_type(col_name)
        if col_type == 'Number':
            print sum(result)
        elif col_type == 'Date':
            print ('Date cannot sum.')
        else:
            print ('Cannot be calculated')

    def std(self, col_name):
        result, col_type = self.col_type(col_name)
        mean = sum(result) / len(result)
        if col_type == 'Number':
            print  (sum((x - mean) ** 2 / len(result) for x in result)) ** 0.5
        elif col_type == 'Date':
            print ('Date do not need std.')
        else:
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

    def add_column(self, list_of_lists, col_name):
        # type: (object, object) -> object
        if len(list_of_lists) == len(self.data):
            self.header = self.header + col_name
            new_col_dict = [OrderedDict(zip(col_name, row)) for row in list_of_lists]
            for l in range(len(self.data)):
                for rowz in self.data:
                    rowz = self.data[l].update(new_col_dict[l])
            return self
        else:
            print ('Wrong number of len')

    ############# end task 5 #############

    ############# HW3 task 1 #############
    def sort_by(self, col_name, reverse):
        if isinstance(col_name, str):
            self.data = sorted(self.data, key=operator.itemgetter(col_name), reverse=reverse)
            return self.data
        elif isinstance(col_name, list):
            if isinstance(reverse, bool):
                for i in range(len(col_name))[::-1]:
                    self.data = sorted(self.data, key=operator.itemgetter(col_name[i]), reverse=reverse)
                return self.data
            elif isinstance(reverse, list):
                for i in range(len(col_name))[::-1]:
                    self.data = sorted(self.data, key=operator.itemgetter(col_name[i]), reverse=reverse[i])
                return self.data
            else:
                print 'Number of parameter is wrong!'
        else:
            print 'TypeError'

    ############# end task 1 #############

    ############# HW3 task 3 #############

    def group_by(self, group, agg, func):
        if isinstance(group, str) & isinstance(agg, str):
            raw_data=self[[group,agg]]
            d = defaultdict(list)
            for key,value in raw_data:
                d[key].append(value)
            result=OrderedDict(d.items())
            for i,j in result.items():
                result[i]=avg(j)
            return result
        elif isinstance(group,list):
            a=group
            a.append(agg)
            raw_data=self[a]
            d = defaultdict(list)
            name = []
            value = []
            for row in raw_data:
                for i in range(1, len(row) - 1):
                    x = row[0] + ':' + row[i]
                name.append(x)
                value.append(row[-1])
            new_data = zip(name, value)
            for k, v, in new_data:
                d[k].append(v)
            result = OrderedDict(d.items())
            for i,j in result.items():
                result[i]=avg(j)
            return result
        else:
            print 'Error'



def avg(list_of_values):
    return sum(list_of_values) / float(len(list_of_values))

    ############# end task 3 #############

    ############# HW3 task 2 #############


class Series(list):
    def __init__(self, list_of_values):
        self.data = list_of_values

    def __eq__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item == other)
        return ret_list

    def __ne__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item != other)
        return ret_list

    def __lt__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item < other)
        return ret_list

    def __gt__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item > other)
        return ret_list

    def __le__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item <= other)
        return ret_list

    def __ge__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item >= other)
        return ret_list

    ############# end task 2 #############


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
df = DataFrame.from_csv('SalesJan2009.csv')
# # ============test HW2 task 3============
# x='Last_Login'
# test1 = df.min(x)
# test2 = df.max(x)
# test3 = df.median(x)
# test4 = df.sum(x)
# test5 = df.mean(x)
# test6 = df.std(x)
# # ============test HW2 task 4============
# new_row = df[1:3]
# new_rowz = df.add_rows(new_row)
# print (new_rowz)
# # ============test HW2 task 5============
# new_col = df[:,:3]
# add_col = df.add_column(new_col,new_col[0])
# print (add_col)
# # ============test HW3 task 1============
# test1=df.sort_by('Price',True)
# test1
# test2=df.sort_by(['Payment_Type','Price'],[True,True])
# test2
test3 = df[df['Price'] > 1400]
test4=df.group_by('Product','Price',avg)
test5=df.group_by(['Product','Payment_Type'],'Price',avg)
2 + 2
