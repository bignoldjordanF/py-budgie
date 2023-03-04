import pbreader
import pybudgie


def main():
    contents = pbreader.read_pb_file('resources/poland_warszawa_2019_ursynow.pb')
    metadata, projects, voters = contents.metadata, contents.projects, contents.voters

    instance = pybudgie.PBInstance(
        description = metadata['description'],
        budget = metadata['budget'],
        vote_type = pbreader.PBVoteType.from_string(metadata['vote_type']),
        country = metadata['country'],
        region = metadata['unit'],
        district = metadata['district'],
        category = metadata['subunit'],
    )

    print(instance)


if __name__ == '__main__':
    main()
