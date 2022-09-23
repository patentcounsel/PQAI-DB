"""
Unit test for custom wrapper around S3 storage
"""

import unittest
import sys
from pathlib import Path

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.parent

import testutil
testutil.load_test_environment()

sys.path.append(str(BASE_DIR.resolve()))
from core.s3wrapper import S3Bucket

class TestS3BucketOperations(unittest.TestCase):

    """Test object uploading, downloading, and listing operations of an
        S3 bucket
    """

    def setUp(self):
        self._bucket_name = testutil.TestS3BucketCreator().create()
        self.test_bucket = S3Bucket(self._bucket_name)

    def test_operations(self):
        filename = 'US7654321B2.json'
        key = f'patents/{filename}'

        self.assertObjectCount(key, 1)

        file = str((TEST_DIR / filename).resolve())
        with open(file, 'rb') as fp:
            data = fp.read()
        downloaded = self.test_bucket.get(key)
        self.assertEqual(data, downloaded)

        self.test_bucket.delete(key)
        self.assertObjectCount(key, 0)

        self.test_bucket.put(key, downloaded)
        self.assertObjectCount(key, 1)

    def assertObjectCount(self, key, n):
        keys = self.test_bucket.list(key)
        self.assertEqual(n, len(keys))


if __name__ == '__main__':
    unittest.main()
