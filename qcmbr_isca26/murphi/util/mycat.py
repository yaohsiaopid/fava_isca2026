from pprint import pprint
import pickle
import argparse
from collections import OrderedDict

def load_pickle_file(filename):
    """
    Loads an OrderedDict from a pickle file.
    """
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            print(f"Successfully loaded data from {filename}")
            return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except pickle.UnpicklingError:
        print(f"Error: Could not unpickle the file '{filename}'. It may be corrupted or not a pickle file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    """
    Main function to parse arguments and load the pickle file.
    """
    parser = argparse.ArgumentParser(
        description="Load an OrderedDict from a .pkl file and print its contents."
    )
    parser.add_argument(
        "filename",
        help="The path to the .pkl file to load."
    )
    args = parser.parse_args()

    ordered_dict_data = load_pickle_file(args.filename)

    if ordered_dict_data is not None:
        print("\nContents of the file:")
        # Using pprint for better readability of complex OrderedDicts
        pprint(ordered_dict_data)
        print(f"\nType of loaded data: {type(ordered_dict_data)}")

if __name__ == "__main__":
    main()
