def load_vectors(matrix):
    vectors = []
    searching = True
    for (y, line) in enumerate(matrix):
        for (x, value) in enumerate(line):
            if searching and value == 1: # Line found, increment length now
                vectors.append({ "x": x, "y": y, "length": 1 })
                searching = False
            elif not searching and value == 1: # Increment line length
                vectors[-1]["length"] += 1
            elif not searching and value == 0: # Stop line length incrementation
                searching = True
    return vectors