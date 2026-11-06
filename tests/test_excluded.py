"""Kaynak alınmayacak yazarlar ve eserler (`catalog/excluded.py`, kullanıcının kararı 2026-11-06)."""

from dataclasses import replace

import pytest

from risale_mcp.catalog import WORKS, _excluded_problems
from risale_mcp.catalog.excluded import openiti_reason
from risale_mcp.sources import openiti


@pytest.mark.parametrize("path", [
    "1323MuhammadCabduh/1323MuhammadCabduh.RisalatTawhid/1323MuhammadCabduh.RisalatTawhid.Shamela0001-ara1",
    "1354RashidRida/1354RashidRida.Manar/1354RashidRida.Manar.Shamela0002-ara1",
])
def test_excluded_openiti_texts_cannot_be_fetched(path):
    assert openiti_reason(path)
    with pytest.raises(ValueError, match="kaynak alınmaz"):
        openiti.Text("1325AH", "0" * 40, path)


def test_other_texts_by_the_same_neighbours_are_allowed():
    assert openiti_reason("1354RashidRida/1354RashidRida.Khilafa/1354RashidRida.Khilafa.X-ara1") is None
    assert openiti_reason("0685NasirDinBaydawi/0685NasirDinBaydawi.AnwarTanzil/0685NasirDinBaydawi.AnwarTanzil.X") is None


def test_the_catalogue_refuses_an_excluded_author():
    assert _excluded_problems(WORKS) == []
    assert _excluded_problems([replace(WORKS[0], author="Muhammed Abduh")])
