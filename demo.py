import pbreader
import pybudgie


def main():
    contents = pbreader.read_pb_file('resources/poland_warszawa_2019_ursynow.pb')
    metadata = contents.metadata

    instance = pybudgie.PBInstance(
        description = metadata['description'],
        country = metadata['country'],
        region = metadata['unit'],
        district = metadata['district'],
        category = metadata['subunit'],
        budget = metadata['budget']
    )
    
    print(instance)


if __name__ == '__main__':
    main()
