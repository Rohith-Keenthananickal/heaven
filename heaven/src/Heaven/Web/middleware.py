from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import os
import re  # Import the re module for regular expressions

class RangeFileWrapper(FileWrapper):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.offset = offset
        self.length = length
        self.filelike.seek(offset, os.SEEK_SET)
        super().__init__(filelike, blksize)

    def __iter__(self):
        remaining = self.length
        while remaining > 0:
            chunk_size = min(self.blksize, remaining)
            data = self.filelike.read(chunk_size)
            if not data:
                break
            remaining -= len(data)
            yield data

def range_request_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        
        if 'HTTP_RANGE' in request.META and isinstance(response, StreamingHttpResponse):
            range_header = request.META['HTTP_RANGE']
            range_match = re.match(r'bytes=(\d+)-(\d+)?', range_header)
            if range_match:
                first_byte, last_byte = range_match.groups()
                first_byte = int(first_byte)
                last_byte = int(last_byte) if last_byte else None
                file_size = os.path.getsize(response.file_to_stream.name)
                if last_byte is None:
                    last_byte = file_size - 1
                length = last_byte - first_byte + 1
                response = StreamingHttpResponse(
                    RangeFileWrapper(response.file_to_stream, offset=first_byte, length=length),
                    status=206,
                    content_type=response['Content-Type'],
                )
                response['Content-Length'] = str(length)
                response['Content-Range'] = f'bytes {first_byte}-{last_byte}/{file_size}'
        return response

    return middleware
