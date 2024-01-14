from enum import Enum
from typing import List, Optional
from nb_to_py.cell import Cell, CellType, CellBuilder
import json


class FilterMarkdownType(Enum):
    KeepLast = "keep_last"
    ExcludeAll = "exclude_all"


class Notebook:
    def __init__(self, filepath: str, cells: List[Cell]):
        self.filepath = filepath
        self.cells = cells


class NotebookBuilder:
    def _read_json(self, filepath: str) -> dict:
        with open(filepath, "r") as f:
            nb = json.load(f)
        return nb

    def _filter_code_cells_by_marker(self, cells: List[Cell]) -> List[Cell]:
        return [
            cell
            for cell in cells
            if cell.cell_type != CellType.Code
            or (cell.cell_type == CellType.Code and cell.is_marked)
        ]

    def _exclude_all_mardown_cells(self, cells: List[Cell]) -> List[Cell]:
        return [cell for cell in cells if cell.cell_type != CellType.Markdown]

    def _keep_last_markdown_cell(self, cells: List[Cell]) -> List[Cell]:
        new_cells = []
        previous_cell = None
        for cell in cells:
            if (
                previous_cell is not None
                and previous_cell.cell_type == CellType.Markdown
                and cell.cell_type == CellType.Code
            ):
                new_cells.append(previous_cell)
            if cell.cell_type != CellType.Markdown:
                new_cells.append(cell)

            previous_cell = cell
        return new_cells

    def _filter_markdown_cells(
        self, cells: List[Cell], filter_markdown_cells_type: FilterMarkdownType
    ) -> List[Cell]:
        if filter_markdown_cells_type == FilterMarkdownType.KeepLast:
            cells = self._keep_last_markdown_cell(cells)
        elif filter_markdown_cells_type == FilterMarkdownType.ExcludeAll:
            cells = self._exclude_all_mardown_cells(cells)
        return cells

    def _build_cells(self, builder: CellBuilder, nb_cells: List[dict]) -> List[Cell]:
        return [builder.build_cell(cell) for cell in nb_cells]

    def build_notebook(
        self,
        filepath: str,
        filter_code_cells_by_marker: bool = False,
        filter_markdown_cells_type: Optional[FilterMarkdownType] = None,
    ):
        nb = self._read_json(filepath)
        builder = CellBuilder()
        cells = self._build_cells(builder, nb.get("cells"))
        if filter_code_cells_by_marker:
            cells = self._filter_code_cells_by_marker(cells)
        if filter_markdown_cells_type:
            cells = self._filter_markdown_cells(cells, filter_markdown_cells_type)
        return Notebook(filepath, cells)
