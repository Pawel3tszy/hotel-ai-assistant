from pathlib import Path


def load_documents(data_path):
    data_path = Path(data_path)

    documents = []

    for file_path in data_path.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        document = {
            "source": file_path.name,
            "content": content
        }

        documents.append(document)

    return documents