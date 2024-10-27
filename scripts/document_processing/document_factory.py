class DocumentFactory:
    def __init__(self):
        self.creators = {}

    def registerFormat(self, extension, creator):
        self.creators[extension] = creator

    def getDocument(self, filepath):
        extension = filepath.split(".")[-1]
        creator = self.creators.get(extension)
        if not creator:
            raise ValueError(f"No document handler for extension: {extension}")
        return creator(filepath)
