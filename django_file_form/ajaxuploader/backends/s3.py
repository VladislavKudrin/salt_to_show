from multiprocessing import Pool

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import boto3
from django.conf import settings

from ajaxuploader.backends.base import AbstractUploadBackend


class S3UploadBackend(AbstractUploadBackend):
    NUM_PARALLEL_PROCESSES = 4
    def upload_chunk(self, chunk, *args, **kwargs):
        self._counter += 1
        buffer = StringIO()
        buffer.write(chunk)
        self._pool.apply_async(
            self._mp.upload_part_from_file(buffer, self._counter))
        buffer.close()

    def setup(self, filename, *args, **kwargs):
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        self._bucket = boto3.resource('s3')
        self._mp = self._bucket.initiate_multipart_upload(filename)
        self._pool = Pool(processes=self.NUM_PARALLEL_PROCESSES)
        self._counter = 0

    def upload_complete(self, request, filename, *args, **kwargs):
        # Tie up loose ends, and finish the upload
        self._pool.close()
        self._pool.join()
        self._mp.complete_upload()
