from nb_to_py.converter import NotebookConverter, Notebook, FilterMarkdownType

if __name__ == "__main__":
    nb = Notebook("tests/unit/sample.ipynb")
    converter = NotebookConverter()

    with open("sample.py", "w") as f:
        converter.convert(
            nb,
            f,
            filter_code_cells_by_marker=True,
            filter_markdown_cells=FilterMarkdownType.KeepLast,
        )
