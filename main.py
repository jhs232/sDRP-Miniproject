from etl.extract import extract
from etl.transform import transform
from etl.load import load

def main():
    load(transform(extract()))

if __name__ == "__main__":
    main()