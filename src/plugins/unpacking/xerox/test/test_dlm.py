import os

from common_helper_files import get_binary_from_file

from helperFunctions.hash import get_sha256
from objects.file import FileObject
from test.unit.unpacker.test_unpacker import TestUnpackerBase
from ..code.dlm import XeroxDLM

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


class TestXeroxDLM(TestUnpackerBase):
    def setUp(self):
        super().setUp()

        self.test_file = FileObject(file_path=os.path.join(TEST_DATA_DIR, 'DLM-First_1MB.DLM'))
        self.test_firmware = self.test_file.file_path
        self.firmware_container = XeroxDLM(self.test_firmware)

    def tearDown(self):
        self.ds_tmp_dir.cleanup()
        self.tmp_dir.cleanup()
        super().tearDown()

    def test_unpacker_selection(self):
        self.check_unpacker_selection('firmware/xerox-dlm', 'XeroxDLM')

    def test_get_header_end_offset(self):
        expected_offset = 0x243
        self.assertEqual(expected_offset, self.firmware_container.get_header_end_offset())

    def test_get_signature(self):
        expected_signature = '90ec11f7b52468378362987a4ed9e56855070915887e6afe567e1c47875b29f9'
        self.assertEqual(expected_signature, self.firmware_container.get_signature())

    def test_get_dlm_version(self):
        expected = 'NO_DLM_VERSION_CHECK'
        self.assertEqual(expected, self.firmware_container.get_dlm_version())

    def test_get_dlm_name(self):
        expected = '080415_08142013'
        self.assertEqual(expected, self.firmware_container.get_dlm_name())

    def test_header_and_binary(self):
        files, meta_data = self.unpacker.extract_files_from_file(self.test_file.file_path, self.tmp_dir.name)
        files = set(files)
        self.assertEqual(len(files), 2, 'file number incorrect')
        header_bin = get_binary_from_file(os.path.join(self.tmp_dir.name, 'dlm_header.bin'))
        self.assertEqual(get_sha256(header_bin), '96abde0032f3600549bac865964cd9d6e6c3e391f5e009be8b86b012cddc90c0')
        data_bin = get_binary_from_file(os.path.join(self.tmp_dir.name, 'dlm_data.bin'))
        self.assertEqual(get_sha256(data_bin), '701962b0d11f50d9129d5a1655ee054865e90cd1b547d40d590ea96f7dfb64eb')
        self.assertEqual(meta_data['dlm_version'], 'NO_DLM_VERSION_CHECK', 'meta: dlm_version not correct')
        self.assertEqual(meta_data['dlm_signature'], '90ec11f7b52468378362987a4ed9e56855070915887e6afe567e1c47875b29f9', 'meta: dlm_signature not correct')
        self.assertEqual(meta_data['dlm_name'], '080415_08142013', 'meta: dlm_name not correct')
        self.assertEqual(meta_data['dlm_extraction_criteria'], 'upgradeExtract.sh /tmp/080415_08142013.dnld', 'meta: dlm_criteria not correct')
