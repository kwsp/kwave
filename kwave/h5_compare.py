import h5py
import numpy as np


def compare_hdf5_files(fname1, fname2) -> bool:
    try:
        with h5py.File(fname1, "r") as f1, h5py.File(fname2, "r") as f2:
            # Compare the keys in both files
            keys1 = set(f1.keys())
            keys2 = set(f2.keys())

            if keys1 != keys2:
                print("Keys in the two files are not the same.")
                print(f"{keys1=}")
                print(f"{keys2=}")
                print(f"{keys1.difference(keys2)=}")
                print(f"{keys2.difference(keys1)=}")
                return False

            # Iterate through the keys and compare the datasets
            for key in keys1:
                dataset1 = f1[key]
                dataset2 = f2[key]

                if dataset1.shape != dataset2.shape or not np.allclose(
                    dataset1, dataset2
                ):
                    print(
                        f"Data in dataset '{key}' is different between the two files."
                    )
                    return False

                attrs_keys1 = set(dataset1.attrs.keys())
                attrs_keys2 = set(dataset2.attrs.keys())
                if attrs_keys1 != attrs_keys2:
                    print(
                        f"Attrs in dataset '{key}' is different between the two files."
                    )
                    return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

    return True
