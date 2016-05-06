
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
        # The raw, unfiltered dataframe. 
        self._raw_dataset = pandas.DataFrame()
        # a list of Column objects
        columns_needed = []


    def get_dataframe(self, columns,query):
        """
        Returns the desired dataframe.

        columns : list of strings
            List of columns that are needed. Must be frugal. All columns that
            are used in the query must be listed here.
        query : string
            A string to pass to the pandas.DataFrame.query method.
        """
        for column in columns:
            self.columns_needed.append(Column(column, Dataset_manager.max_priority))
        _purge_columns_needed(self.columns_needed)

        # If we run in memory troubles, we could here
        # remove columns form the raw_dataset which are not longer needed

        columns_to_load = [ x.name for x in self.columns_needed if x.name not in self._raw_dataset.columns.values ]
        loaded = root_pandas.read_root(self.filename, self.treename, columns=columns_to_load)
        assert( len(loaded.index) == len(self._raw_dataset.index) )
        self._raw_dataset = pandas.concat(self._raw_dataset, loaded, axis=1)

        # reduce column priority
        for column in self.columns_needed:
            column.priority -= 1

        return _raw_dataset.query(query)

    def get_all_columns():
        return read_root(self.filename, self.treename, flatten=True).columns.values


    def _prune_columns_needed():
        """
            Prevents the list of needed columns from growing to big.

            Can be more aggressive if needed.
        """

        columns_needed.sort(lambda x : x.priority)
        # double iteration should not be a big problem due to shortness of list
        pruned = []
        for index in range(0,len(columns_needed)):
            # if there is no later entry with the same name (and higher priority)
            if columns_needed[index].name not in [x.name for x in columns_needed[index+1:] ]:
                pruned.append(name)
        columns_needed = pruned

        # we could now drop columns with very low priority
        # but we must be careful to keep the columns with the highest priority


class Column:
    def __init__(self,name, priority):
        self.name = name
        self.priority = priority



class DataFrameManager:
    """
        Use this class to get the dataframe you need.

        This is an sub implementation to define the public interface.

    """
    def __init__(self, filename):
        #stub
        pass

    def get_dataframe(self, columns,query):
        #stub
        pass
    def get_all_columns():
        #stub
        pass