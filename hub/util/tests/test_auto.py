from hub.api.dataset import Dataset
from hub.tests.common import get_dummy_data_path
from hub.util.auto import get_most_common_extension, ingestion_summary
from io import StringIO
import sys
import hub
import pytest


def test_most_common_extension():
    path = get_dummy_data_path("tests_auto/auto_compression")
    path_file = get_dummy_data_path("test_auto/auto_comrpession/jpeg/bird.jpeg")

    compression = get_most_common_extension(path)
    file_compression = get_most_common_extension(path_file)

    assert compression == "png"
    assert file_compression == "jpeg"


def test_ingestion_summary(memory_ds: Dataset):
    clean_path = get_dummy_data_path("tests_auto/ingestion_summary/class1")
    skipped_path = get_dummy_data_path("tests_auto/ingestion_summary")

    print(skipped_path)
    ingest_summary_clean = StringIO()
    sys.stdout = ingest_summary_clean
    ingestion_summary(clean_path, [], 1)
    sys.stdout = sys.__stdout__

    if ingest_summary_clean.getvalue() in (
        "\n\nIngesiton Complete. No files were skipped.\n\n\n\n",
        "\n=============================== Ingestion Summary =============================\n\nIngesiton Complete. No files were skipped.\n\n\n\n",
    ):
        pass

    ingest_summary_skipped = StringIO()
    sys.stdout = ingest_summary_skipped
    # ingestion_summary(skipped_path, [], 1)
    hub.ingest(
        src=skipped_path,
        dest=memory_ds.path,
        images_compression="auto",
        progress_bar=True,
        summary=True,
        overwrite=False,
    )
    sys.stdout = sys.__stdout__
    output = ingest_summary_skipped.getvalue()

    if output in (
        (
            "\n\n" + "\n\n"
            "============================================================================================= "
            + "\n"
            "Ingestion Summary \n"
            + "===========================================================================================\n\n \n\n ingestion_summary/    (3/4)\n\n       [Skipped]  test.json\n\n       class0/    (1/2)\n\n             [Skipped]  test.json\n\n       class1/    (1/1)\n\n       class2/    (1/0)\n"
        ),
    ):
        pass