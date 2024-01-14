from nb_to_py.converter import NotebookConverter
from nb_to_py.notebook import NotebookBuilder, FilterMarkdownType

if __name__ == "__main__":
    builder = NotebookBuilder()
    notebook = builder.build_notebook(
        filepath="tests/unit/sample.ipynb",
        filter_code_cells_by_marker=False,
        filter_markdown_cells_type=FilterMarkdownType.KeepLast,
    )
    with open("provaaa.py", "w") as f:
        NotebookConverter.convert(notebook,f)
