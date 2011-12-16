from pyon.public import IonObject
from ion.eoi.agent.data_acquisition_management_service_Placeholder import DataAcquisitionManagementServicePlaceholder
import re
import os
import inspect
from pydap.model import *
from pydap.handlers.lib import BaseHandler
from pydap.exceptions import OpenFileError
import numpy
from netCDF4 import Dataset
import yaml
from arrayterator import Arrayterator

try:
    from netCDF4 import Dataset as nc
#    extensions = re.compile(
#            r"^.*\.(nc|nc4|cdf|netcdf)$",
#            re.IGNORECASE)
    var_attrs = lambda var: dict( (a, getattr(var, a))
            for a in var.ncattrs() )
    get_value = lambda var: var.getValue()
    get_typecode = lambda var: var.dtype.char
except ImportError:
    raise ImportError("netCDF4 library missing, cannot continue")

def lineno():
    return inspect.currentframe().f_back.f_lineno

class Handler(BaseHandler):

    extensions = re.compile(r"^.*\.ionref$", re.IGNORECASE)
    damsP = None

    def __init__(self, filepath):
        self.filepath = filepath
        self.damsP = DataAcquisitionManagementServicePlaceholder()

    def parse_constraints(self, environ):
#        print ">> Start parse_constraints"

        ds_name, ds_id, ds_url, buf_size = get_dataset_info(self)
#        print "DS Info:  name=%s ds_id=%s ds_url=%s buf_size=%s" % (ds_name, ds_id, ds_url, buf_size)

        # TODO: Call the "damsP" module to retrieve a BaseDatasetHandler based on the ds_id
        dsh = self.damsP.get_data_handlers(ds_id=ds_id)

        #DSH WAY
        dataset_type = DatasetType(name=ds_name, attributes={'NC_GLOBAL': dsh.get_attributes()})
        fields, queries = environ['pydap.ce']
        fields = fields or [[(name, ())] for name in dsh.ds.variables]

#        print "CE Fields: %s" % fields
#        print "CE Queries: %s" % queries

        pdr_obj = IonObject("PydapVarDataRequest", name="p_req")
#        pdr_obj.apply_maskandscale = apply_mask

        for fvar in fields:
            target = dataset_type
            while fvar:
                name, slice_ = fvar.pop(0)
                pdr_obj.name = name
                pdr_obj.slice = slice_
                if (name in dsh.ds.dimensions or not dsh.ds.variables[name].dimensions or target is not dataset_type):
                    nm, dat, tc, di, at = dsh.acquire_data(request=pdr_obj)
                    target[name] = BaseType(name=nm, data=dat, shape=dat.shape, type=tc, dimensions=di, attributes=at)
                elif fvar:
                    attrs = dsh.get_attributes(var_name=name)
                    target.setdefault(name, StructureType(name=name, attributes=attrs))
                    target = target[name]
                else:
                    attrs = dsh.get_attributes(var_name=name)
                    grid = target[name] = GridType(name=name, attributes=attrs)
                    nm, dat, tc, di, at = dsh.acquire_data(request=pdr_obj)
                    grid[name] = BaseType(name=nm, data=dat, shape=dat.shape, type=tc, dimensions=di, attributes=at)
                    slice_ = list(slice_) + [slice(None)] * (len(grid.array.shape) - len(slice_))
                    for dim, dimslice in zip(dsh.ds.variables[name].dimensions, slice_):
                        pdr_obj.name=dim
                        pdr_obj.slice=dimslice
                        nm, dat, tc, di, at = dsh.acquire_data(request=pdr_obj)
                        grid[dim] = BaseType(name=nm, data=dat, shape=dat.shape, type=tc, dimensions=di, attributes=at)

        dataset_type._set_id()
        dataset_type.close = dsh.ds.close

#        print ">> End parse_constraints"
        return dataset_type

        # ORIGINAL WAY
#        ds = nc(ds_url)
#
#        dataset_type = DatasetType(name=name, attributes={'NC_GLOBAL': var_attrs(ds)})
#
#        fields, queries = environ['pydap.ce']
#        fields = fields or [[(name, ())] for name in ds.variables]
#        print "CE Fields: %s" % fields
#        print "CE Queries: %s" % queries
#
##        for vk in ds.variables:
#        for fvar in fields:
#            target = dataset_type
##            print fvar
#            while fvar:
#                name, slice_ = fvar.pop(0)
#                if (name in ds.dimensions or not ds.variables[name].dimensions or target is not dataset_type):
##                    print lineno()
#                    target[name] = get_var(name, ds, slice_, buf_size)
#                elif fvar:
#                    attrs = var_attrs(ds.variables[name])
#                    target.setdefault(name, StructureType(name=name, attributes=attrs))
#                    target = target[name]
#                else:
#                    attrs = var_attrs(ds.variables[name])
#                    grid = target[name] = GridType(name=name, attributes=attrs)
##                    print lineno()
#                    grid[name] = get_var(name, ds, slice_, buf_size)
#                    slice_ = list(slice_) + [slice(None)] * (len(grid.array.shape) - len(slice_))
#                    for dim, dimslice in zip(ds.variables[name].dimensions, slice_):
##                        print lineno()
#                        grid[dim] = get_var(dim, ds, dimslice, buf_size)
#
##                if name in ds.variables:
##                    var = ds.variables[name]
##
##                    dtype = str(var.dtype)
##                    if dtype == '|S1':
##                        continue
##
##                    atts={}
##                    for ak in var.ncattrs():
##                        atts[ak] = var.getncattr(ak)
##
###                    dat=var[:]
##                    dat=numpy.array(2)
##                    if isinstance(dat, numpy.ma.core.MaskedArray):
##                        dat = dat.data
##                    elif isinstance(dat, numpy.ndarray):
##                        dat = dat
##
##                    if dtype == '|S1':
##                        dat = numpy.array([''.join(row) for row in numpy.asarray(dat)])
##                        dtype = 'S'
##
###                    print dat
##
##                    dataset_type[name] = BaseType(name=name, data=dat, shape=var.shape, type=dtype, dimensions=var.dimensions, attributes=atts)
#
#        dataset_type._set_id()
#        dataset_type.close = ds.close
#
#        print ">> End parse_constraints"
#        return dataset_type

def get_var(name, fp, slice_, buf_size=10000):
    if name in fp.variables:
        var = fp.variables[name]
        if var.shape:
#            print lineno()
            data = Arrayterator(var, buf_size)[slice_]
        else:
#            print lineno()
            data = numpy.array(get_value(var))
        typecode = get_typecode(var)
        dims = var.dimensions
        attrs = var_attrs(var)
    else:
        for var in fp.variables:
            var = fp.variables[var]
            if name in var.dimensions:
                size = var.shape[
                        list(var.dimensions).index(name)]
                break
#        print lineno()
        data = numpy.arange(size)[slice_]
        typecode = data.dtype.char
        dims, attrs = (name,), {}

    # handle char vars
    if typecode == 'S1':
        typecode = 'S'
        data = numpy.array([''.join(row) for row in numpy.asarray(data)])
        dims = dims[:-1]

#    print "==> dtype: %s" % type(data)

    return BaseType(name=name, data=data, shape=data.shape,
            type=typecode, dimensions=dims,
            attributes=attrs)

def get_dataset_info(self):
    try:
        config = yaml.load(file(self.filepath))
    except:
        message = "Unable to open file '%s'." % self.filepath
        raise OpenFileError(message)

#        ds_url = environ["pydap.handlers.test.ds_url"]
    ds_obj = config["dataset"]

    if "name" in ds_obj:
        name = ds_obj["name"]
    else:
        name = os.path.split(self.filepath)[1]

    if "external_dataset_id" in ds_obj:
        ds_id = ds_obj["external_dataset_id"]
    else:
        raise OpenFileError("ExternalDataset ID not specified")

    if "buffer_size" in ds_obj:
        buf = ds_obj["buffer_size"]
    else:
        buf = 10000

    if "url" in ds_obj:
        ds_url = ds_obj["url"]
    else:
        raise OpenFileError("Dataset url not specified")

    if ds_url.startswith("&"):
        full=os.getcwd() + ds_url.replace("&","")
        ds_url = os.path.abspath(full)


    return name, ds_id, ds_url, buf



if __name__ == '__main__':
    import sys
    from paste.httpserver import serve

    application = Handler(sys.argv[1])
    serve(application, port=8001)
