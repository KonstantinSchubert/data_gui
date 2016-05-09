import pandas
import root_pandas

class DataFrameManager:
    """
        Use this class to get the DataFrame you need.

        This is an sub implementation to define the public interface.

    """
    def __init__(self, filename):
        #stub
        pass

    def get_DataFrame(self, columns,query):
        #stub
        pass
    def get_all_columns():
        #stub
        pass


class DataFrameManagerROOT(DataFrameManager):
    """
        Use this class if you are interfacing a root file.

        This class manages the loading and filtering of the data. 
        It can decides which columns it loads from the root file and 
        how much of it is being stored.
    """
    max_priority = 10
    def __init__(self, filename, treename = None):
        self.filename = filename
        self.treename = treename
        # The raw, unfiltered DataFrame. 
        self._raw_dataset = pandas.DataFrame()
        # a list of Column objects
        self.columns_needed = []
        self.columns_available = None


    def _prune_columns_needed(self, columns_needed):
        """
            Prevents the list of needed columns from growing to big.

            Can be more aggressive if needed.
        """

        columns_needed.sort(key=lambda x : x.priority)
        # double iteration should not be a big problem due to shortness of list
        pruned = []
        for index in range(0,len(columns_needed)):
            # if there is no later entry with the same name (and higher priority)
            if columns_needed[index].name not in [x.name for x in columns_needed[index+1:] ]:
                pruned.append(columns_needed[index])
        columns_needed = pruned

        # we could now drop columns with very low priority
        # but we must be careful to keep the columns with the highest priority


    def get_DataFrame(self, columns, query=None):
        """
        Returns the desired DataFrame.

        columns : list of strings
            List of columns that are needed. Must be frugal. All columns that
            are used in the query must be listed here.
        query : string
            A string to pass to the pandas.DataFrame.query method.
        """
        for column in columns:
            self.columns_needed.append(Column(column, DataFrameManagerROOT.max_priority))
        self._prune_columns_needed(self.columns_needed)

        # If we run in memory troubles, we could here
        # remove columns form the raw_dataset which are not longer needed

        columns_to_load = [ x.name for x in self.columns_needed if x.name not in self._raw_dataset.columns.values ]
        loaded = root_pandas.read_root(self.filename, self.treename, columns=columns_to_load)
        assert( len(loaded.index) == len(self._raw_dataset.index) or len(self._raw_dataset.index) == 0 )
        self._raw_dataset = pandas.concat([self._raw_dataset, loaded] , axis=1)

        # reduce column priority
        for column in self.columns_needed:
            column.priority -= 1
        if query is None:
            return self._raw_dataset
        else:
            return self._raw_dataset.query(query)


    def get_all_columns(self):
        if self.columns_available is None:
            df = root_pandas.read_root(self.filename, self.treename, chunksize=1).next()
            self.columns_available = df.columns.values
        return self.columns_available




class Column:
    def __init__(self,name, priority):
        self.name = name
        self.priority = priority


