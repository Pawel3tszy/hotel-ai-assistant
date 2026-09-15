def split_documents(documents):
    chunks = []

    for document in documents:
        source = document["source"]
        content = document["content"]

        sections = content.split("\n## ")

        for index, section in enumerate(sections):
            section = section.strip()

            if not section:
                continue

            if index > 0:
                section = "## " + section

            chunk = {
                "source": source,
                "content": section
            }

            chunks.append(chunk)

    return chunks