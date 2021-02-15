## new/better way of doing it!

- download allArtworks.jsonl -- which has a single line per artwork -- https://github.com/art-institute-of-chicago/api-data
- extract list of artwork ids
- download iiif manifest json files for all artworks
- extract image urls from manifests

---

## accessing open access data + images (worse way of doing this)

- [see here](https://github.com/art-institute-of-chicago/api-data) for a repository documenting the OA dataset
- as of Feb 2021, the OA full dataset can be downloaded at https://artic-api-data.s3.amazonaws.com/artic-api-data.tar.bz2
- accessing image URLs is super annoying. The Art Institute of Chicago's [Open Access Images page](https://www.artic.edu/open-access/open-access-images) says to use their [public image search engine](https://www.artic.edu/collection) for which no API exists. These result pages need to be iterated through (to get all of the data) and then html-parsed. Example URL:

https://www.artic.edu/collection?is_public_domain=1&page=2

however, the public search engine does not allow to iterate past the 10,000th result ("Sorry, we cannot show more than 10,000 results.") which is a problem considering that 55,206 images are supposed to be available in the public domain.

- getting the list of public domain images requires doing searches with limited date ranges (all public domain images from 1970 to 1980, all images from 1980 to 1990, etc.) and combining all of those results

## steps to do it

- use public search engine to iterate through pages of artworks by selecting small date ranges, e.g.

https://www.artic.edu/collection?date-start=1930&date-end=1940&is_public_domain=1&page=2

- based on the artwork id, download the related IIIF manifest, e.g.

https://api.artic.edu/api/v1/artworks/45382/manifest.json

## notes

- there is probably an error in the html parsing, and I did the classic error of scraping + parsing the page in one go, instead of downloading pages and then parsing them (as parsing errors can then be fixed and re-run on already downloaded pages, instead of having to re-download them every time)

the public search engine says that there 55,206 public domain artworks, but I only found 39,620 unique public domain artwork urls...

- this is an overly complicated solution to just scrape URLs that have sequential IDs... 
