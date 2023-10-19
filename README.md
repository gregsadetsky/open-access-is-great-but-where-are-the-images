## TLDR

Museums are sharing data on their artworks as part of "[Open Access](https://en.wikipedia.org/wiki/Open_access)" programs. Unfortunately, most museums don't make it easy to access the URLs of artwork images.

This project makes it easy to access the image URLs (see below), and provides (TODO!) SQLite databases containing all of the artwork data published through Open Access.

## Where are the images?

- [Met - Images CSV](1.data/met-images.csv)
- [Chicago - Images CSV](1.data/chicago-images.csv)

## Where is the data

Artwork data / meta information has been collected in these SQLite database files:
- `2.sqlify/open-access-is-great-but-where-are-the-images.db`

## Reasons to do this (/rant/soapbox)

- the Met doesn't make image URLs part of its [frequently updated CSV dataset file](https://github.com/metmuseum/openaccess/) -- "Images are not included and are not part of the dataset"

- the Art Institute of Chicago does not make image URLs easily available either -- warning of this in the exact same language as the Met: "Images are not included and are not part of the dataset" from its otherwise well thought out [API documentation](https://github.com/art-institute-of-chicago/api-data)

- does giving access to the image URLs feel reductive of the richness of this data? why are institutions putting in so much effort to publish Open Access datasets and keep them updated, but specifically hide the image URLs? what's going on? am I crazy?

- in the case of the Met, getting all the image URLs requires downloading a 300 Mb CSV file (as of Feb 2021) and making 600k API calls which take multiple hours to complete

- although CSV and JSON files are text-based and thus easy to consume on all platforms (the Met provides CSV, the Art Institute of Chicago JSON), past a certain file size or number of files, these become difficult to work with (does Excel allow importing a 300Mb CSV file?) For this reason, I will also be publishing (TODO) SQLite database files containing Open Access data for all museums.

The SQLite format can be used / queried on a large number of platforms. You can use [DB Browser](https://sqlitebrowser.org/) on macOS, Windows and Linux to browse the files using a graphical interface. Bindings for most programming languages exist as well.
