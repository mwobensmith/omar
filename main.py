# import the necessary packages
from imutils import paths
import time
import sys
import cv2
import os

def dhash(image, hashSize=8):
	# resize the input image, adding a single column (width) so we
	# can compute the horizontal gradient
	resized = cv2.resize(image, (hashSize + 1, hashSize))
	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]
	# convert the difference image to a hash
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

# grab the paths to both the haystack and needle images
print("[INFO] computing hashes for haystack...")
haystackPaths = list(paths.list_images("all_images"))
needlePaths = list(paths.list_images("needle_images"))
# remove the `\` character from any filenames containing a space
# (assuming you're executing the code on a Unix machine)
if sys.platform != "win32":
	haystackPaths = [p.replace("\\", "") for p in haystackPaths]
	needlePaths = [p.replace("\\", "") for p in needlePaths]

# grab the base subdirectories for the needle paths, initialize the
# dictionary that will map the image hash to corresponding image,
# hashes, then start the timer
BASE_PATHS = set([p.split(os.path.sep)[-2] for p in needlePaths])
haystack = {}
start = time.time()

# loop over the haystack paths
for p in haystackPaths:
	# load the image from disk
	image = cv2.imread(p)
	# if the image is None then we could not load it from disk (so
	# skip it)
	if image is None:
		continue
	# convert the image to grayscale and compute the hash
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imageHash = dhash(image)
	# update the haystack dictionary
	l = haystack.get(imageHash, [])
	l.append(p)
	haystack[imageHash] = l

# show timing for hashing haystack images, then start computing the
# hashes for needle images
print("[INFO] processed {} images in {:.2f} seconds".format(
	len(haystack), time.time() - start))
print("[INFO] computing hashes for needles...")

all_matches = []
# loop over the needle paths
for p in needlePaths:
	# load the image from disk
	image = cv2.imread(p)

	# if the image is None then we could not load it from disk (so
	# skip it)
	if image is None:
		continue

	# convert the image to grayscale and compute the hash
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imageHash = dhash(image)
	print(p)
	print(imageHash)

	# grab all image paths that match the hash
	matchedPaths = haystack.get(imageHash, [])
	# loop over all matched paths
	for matchedPath in matchedPaths:
		#print("Needle match: %s" % p)
		#print("Haystack match: %s" % matchedPaths)
		all_matches.append(matchedPath)
		# extract the subdirectory from the image path
		b = p.split(os.path.sep)[-2]

		# if the subdirectory exists in the base path for the needle
		# images, remove it
		if b in BASE_PATHS:
			BASE_PATHS.remove(b)

# display directories to check
print("[INFO] check the following directories...")

# loop over each subdirectory and display it
for b in BASE_PATHS:
	print("[INFO] {}".format(b))

for match in all_matches:
	print(match)


"""
Notes:
* This script requires exact hash matching. It could be modified to allow for a range of matches.
* If the needle is just a slightly cropped version of the haystack, it fails. It might be interesting to search for an image inside the haystack instead.
* To examine the 9x8 compare images, we could write them to a folder for inspection. 
"""