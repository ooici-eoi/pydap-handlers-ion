from ion.eoi.agent.handler.dap_external_data_handler import DapExternalDataHandler
import re
import os
from configobj import ConfigObj
from pydap.model import *
from pydap.handlers.lib import BaseHandler
from pydap.exceptions import OpenFileError
import numpy
from netCDF4 import Dataset
import yaml

class Handler(BaseHandler):

    extensions = re.compile(r"^.*\.ionref$", re.IGNORECASE)

    def __init__(self, filepath):
        self.filepath = filepath

    def parse_constraints(self, environ):
        print ">> Start parse_constraints"

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

        if "url" in ds_obj:
            ds_url = ds_obj["url"]
        else:
            raise OpenFileError("Dataset url not specified")

        if ds_url.startswith("&"):
            full=os.getcwd() + ds_url.replace("&","")
            ds_url = os.path.abspath(full)

        print "Data URL: %s" % ds_url

        ds = Dataset(ds_url)

        gbls={}
        for k in ds.ncattrs():
            gbls[k]=ds.getncattr(k)


        dataset_type = DatasetType(name=name, attributes={'NC_BLOBAL': gbls})

        fields, queries = environ['pydap.ce']
        fields = fields or [[(name, ())] for name in ds.variables]
        print fields
        print queries

#        for vk in ds.variables:
        for fvar in fields:
            while fvar:
                name, slice_ = fvar.pop(0)
                if name in ds.variables:
                    var = ds.variables[name]

                    dtype = str(var.dtype)
                    if dtype == '|S1':
                        continue

                    atts={}
                    for ak in var.ncattrs():
                        atts[ak] = var.getncattr(ak)

                    dat=var[:]
                    if isinstance(dat, numpy.ma.core.MaskedArray):
                        dat = dat.data
                    elif isinstance(dat, numpy.ndarray):
                        dat = dat

                    if dtype == '|S1':
                        dat = numpy.array([''.join(row) for row in numpy.asarray(dat)])
                        dtype = 'S'

#                    print dat

                    dataset_type[name] = BaseType(name=name, data=dat, shape=var.shape, type=dtype, dimensions=var.dimensions, attributes=atts)

        dataset_type._set_id()
        dataset_type.close = ds.close

        print ">> End parse_constraints"
        return dataset_type

if __name__ == '__main__':
    import sys
    from paste.httpserver import serve

    application = Handler(sys.argv[1])
    serve(application, port=8001)
