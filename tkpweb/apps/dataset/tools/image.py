import os
from tkp.database import DataBase
from tkp.utility.accessors import DataAccessor
from tkp.utility.accessors import FITSImage
from tkp.utility.accessors import CASAImage

from tkpweb.settings import MONGODB
if MONGODB["enabled"]:
    from .mongo import fetch_hdu_from_mongo

def open_image(url, database=None):
    def get_file_by_url(url):
        image = None
        try:
            if os.path.isdir(url):
                # Likely a CASA image
                image = CASAImage(url)
            elif os.path.exists(url):
                image = FITSImage(url)
            elif MONGODB["enabled"]:
                hdu = fetch_hdu_from_mongo(url)
                image = FITSImage(hdu)
            else:
                raise Exception("FITS file not available")
        except Exception, e:
            # Unable to access file
            print e
        return image

    image = None
    if isinstance(url, DataAccessor):
        image = url
    elif isinstance(url, basestring):
        image = get_file_by_url(url)
    elif isinstance(url, (int, long)):
        db = database if database else DataBase()
        url = Image(id=url, database=database).url
        image = get_file_by_url(url)
    else:
        raise ValueError("unable to fetch url")
    return image
