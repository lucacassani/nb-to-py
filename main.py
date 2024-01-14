from nb_to_py.converter import NotebookConverter
from nb_to_py.notebook import NotebookBuilder, FilterMarkdownType

if __name__ == "__main__":
    builder = NotebookBuilder()
    notebook = builder.build_notebook(
        filepath="tests/unit/sample.ipynb",
    )
    #notebook.filter_code_cells_by_marker()
    #notebook.filter_markdown_cells(FilterMarkdownType.KeepLast)
    with open("provaaa.py", "w") as f:
        NotebookConverter.convert(notebook,f)
