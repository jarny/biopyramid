import pandas
from threading import Lock
mutex = Lock()

# --------------------------------------------------
# Mutual exclusion method decorator
# --------------------------------------------------	
def mutual_exclusion(func):
	def access_mutex(*args, **kwargs):
		mutex.acquire()
		try:	
			return func(*args, **kwargs)
		finally:
			mutex.release()
	return access_mutex
	
# --------------------------------------------------
# HDF5 File access mutual exclusion
# --------------------------------------------------		
@mutual_exclusion
def read_hdf_mutex(dataset, attr):
	return pandas.read_hdf(dataset, attr)

@mutual_exclusion
def hdf_attr_to_dict(filepath, attr):
	store = pandas.HDFStore(filepath)
	d = store[attr].to_dict()
	store.close()
	return d

@mutual_exclusion
def to_hdf_mutex(item, filepath, key):
	item.to_hdf(filepath, key)