import kagglehub

path = kagglehub.dataset_download(
    "ismailnasri20/driver-drowsiness-dataset-ddd"
)

print("Path to dataset files:", path)
