
from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import Status
from git_code_debt.file_diff_stat import SpecialFile
from git_code_debt.file_diff_stat import SpecialFileType
from git_code_debt.metric import Metric
from git_code_debt.metrics.binary_file_count import BinaryFileCount


def test_binary_file_count_detects_added():
    parser = BinaryFileCount()
    input = [
        FileDiffStat(
            'foo', [], [], Status.ADDED,
            special_file=SpecialFile(SpecialFileType.BINARY, 'foo', None),
        ),
    ]

    metrics = list(parser.get_metrics_from_stat(input))
    assert metrics == [Metric('BinaryFileCount', 1)]


def test_binary_file_count_detects_deleted():
    parser = BinaryFileCount()
    input = [
        FileDiffStat(
            'foo', [], [], Status.DELETED,
            special_file=SpecialFile(SpecialFileType.BINARY, None, 'foo'),
        ),
    ]

    metrics = list(parser.get_metrics_from_stat(input))
    assert metrics == [Metric('BinaryFileCount', -1)]


def test_binary_file_count_detects_ignores_moved():
    parser = BinaryFileCount()
    input = [
        FileDiffStat(
            'foo', [], [], Status.ALREADY_EXISTING,
            special_file=SpecialFile(SpecialFileType.BINARY, 'foo', 'foo'),
        ),
    ]

    metrics = list(parser.get_metrics_from_stat(input))
    assert metrics == [Metric('BinaryFileCount', 0)]
