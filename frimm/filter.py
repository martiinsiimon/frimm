"""
"""

class Filter(object):

    """
    Filter object. Contains filter name (displayed), filter language (needed?), filter source file (for execution) and filter description (to show details, if provided)
    TODO:
        add setters
        add getters
        dump()
        testSetters() -- tests
        testGetters() -- tests
        testDump() -- tests
    """
    def __init__(self):
        self.name = ''
        self.lang = ''
        self.source = ''
        self.description = ''


class Filters(object):

    """
    Container for filter objects. Provides function to automatically load filters from predefined location, create list of them, provide information of specific filter and execute code of specific filter.
    TODO:
        refresh() # the list of filters
        addFilter()
        delFilter()
        clearFilters()
        getFilter()
        executeFilter()
        dumpFilters()
        testRefresh() -- tests
        testAdd() -- tests
        testDel() -- tests
        testClear() -- tests
        testGetFilter() -- tests
        testDump() -- tests
        testExecution() -- tests
    """
    def __init__(self):
        self.filters = dict()
