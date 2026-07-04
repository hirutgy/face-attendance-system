from load_dataset import load_lfw, count_identities, filter_valid_identities
from build_dataset import build_dataset

def main():
    ds = load_lfw()
    print("LFW dataset loaded.")

    print("Dataset tensors:", list(ds.tensors))

    counts = count_identities(ds)
    print("Identity counts computed.")

    valid_ids = filter_valid_identities(counts, min_images=5)
    print(f"Valid identities: {len(valid_ids)}")

    build_dataset(ds, valid_ids)
    print("Dataset folders created successfully.")

if __name__ == "__main__":
    main()
