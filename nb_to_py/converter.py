import json
from typing import List, Optional, TextIO
from enum import Enum


class FilterMarkdownType(Enum):
    KeepLast = "keep_last"
    ExcludeAll = "exclude_all"


class Notebook:
    KEEP_MARKERS = ["# KEEP"]

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.json = json.load(open(filepath))
        self.cells = self._read_cells_from_json()

    def _read_cells_from_json(self) -> Optional[List]:
        return self.json.get("cells", None)

    def filter_code_cells_by_marker(self):
        cells = []
        for cell in self.cells:
            if cell.get("cell_type") != "code":
                cells.append(cell)
            elif (
                cell.get("cell_type") == "code"
                and any(
                    marker in cell.get("source", [""])[0]
                    for marker in self.KEEP_MARKERS
                )
                and len(cell.get("source")) > 1
            ):
                cell["source"] = cell.get("source")[1:]
                cells.append(cell)

        self.cells = cells

    def filter_markdown_cells(
        self, filter_comments: FilterMarkdownType = FilterMarkdownType.KeepLast
    ):
        cells = None
        if filter_comments == FilterMarkdownType.KeepLast:
            cells = self._keep_last_markdown_cell()
        elif filter_comments == FilterMarkdownType.ExcludeAll:
            cells = self._exclude_all_mardown_cells()

        self.cells = cells

    def _exclude_all_mardown_cells(self) -> List:
        return [cell for cell in self.cells if cell.get("cell_type") != "markdown"]

    def _keep_last_markdown_cell(self) -> List:
        cells = []
        previous_cell = None
        for cell in self.cells:
            if (
                previous_cell is not None
                and previous_cell.get("cell_type") == "markdown"
                and cell.get("cell_type") == "code"
            ):
                cells.append(previous_cell)
            if cell.get("cell_type") != "markdown":
                cells.append(cell)

            previous_cell = cell
        return cells


class NotebookConverter:
    def convert(
        self,
        notebook: Notebook,
        output_file: TextIO,
        filter_markdown_cells: FilterMarkdownType = None,
        filter_code_cells_by_marker: bool = False,
    ):
        if filter_code_cells_by_marker:
            notebook.filter_code_cells_by_marker()
        if filter_markdown_cells is not None:
            notebook.filter_markdown_cells(filter_markdown_cells)

        output_file.write(
            "\n\n".join(["".join(cell.get("source")) for cell in notebook.cells])
        )
