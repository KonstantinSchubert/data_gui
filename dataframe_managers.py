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
        self.columns_priority = {}
        self.columns_available = None


    def _prune_columns_needed(self):
        """
            Prevents the list of needed columns from growing to big.

            Can be more aggressive if needed.
        """

        # we could now drop columns with very low priority
        # but we must be careful to keep the columns with the highest priority
        pass



    def get_DataFrame(self, columns, query=None):
        """
        Returns the desired DataFrame.

        columns : list of strings
            List of columns that are needed. Must be frugal. All columns that
            are used in the query must be listed here.
        query : string
            A string to pass to the pandas.DataFrame.query method.
        """
        # decrease priority for existing columns
        for column in self.columns_needed:
            self.columns_priority[column] -= 1;
        # join the new columns into the set
        self.columns_needed = list(set(list(self.columns_needed) + columns))
        # set the priority of the new columns to max
        for column in columns:
            self.columns_priority[column] = DataFrameManagerROOT.max_priority

        self._prune_columns_needed()

        columns_to_load = [ x for x in self.columns_needed if x not in self._raw_dataset.columns.values ]
        if columns_to_load:
            loaded = root_pandas.read_root(self.filename, self.treename, columns=columns_to_load)
            assert( len(loaded.index) == len(self._raw_dataset.index) or len(self._raw_dataset.index) == 0 )
            self._raw_dataset = pandas.concat([self._raw_dataset, loaded] , axis=1)


        if query is None:
            return self._raw_dataset
        else:
            return self._raw_dataset.query(query)


    def get_all_columns(self):
        if self.columns_available is None:
            df = root_pandas.read_root(self.filename, self.treename, chunksize=1).next()
            self.columns_available = df.columns.values
        return self.columns_available


