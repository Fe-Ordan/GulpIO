#!/usr/bin/env python

"""Create a binary file including all video frames with RecordIO convention.

Usage:
    create_binary [--videos_per_chunk <videos_per_chunk>]
                  [--num_workers <num_workers>]
                  [--image_size <image_size>]
                  <input_json> <videos_directory> <output_directory>
    create_binary (-h | --help)
    create_binary --version

Arguments:
    input_json:                             Input JSON file
    videos_directory                        Base directory for video files
    output_directory                        Output directory for GulpIO files

Options:
    -h --help                               Show this screen.
    --version                               Show version.
    --videos_per_chunk=<videos_per_chunk>   Number of videos in one chunk [default: 100]
    --num_workers=<num_workers>             Number of parallel processes [default: 4]
    --image_size=<image_size>               Size of smaller edge of resized frames [default: -1]
"""

from docopt import docopt
from tqdm import tqdm
from joblib import Parallel, delayed

from gulpio.adapters import Custom20BNJsonAdapter
from gulpio.convert_binary import GulpIngestor

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)

    input_json = arguments['<input_json>']
    videos_path = arguments['<videos_directory>']
    output_folder = arguments['<output_directory>']
    videos_per_chunk = int(arguments['--videos_per_chunk'])
    num_workers = int(arguments['--num_workers'])
    img_size = int(arguments['--image_size'])

    adapter = Custom20BNJsonAdapter(input_json, videos_path,
                                    frame_size=img_size)
    ingestor = GulpIngestor(adapter, output_folder, videos_per_chunk)
    ingestor.ingest()
#    results = Parallel(n_jobs=num_workers)(delayed(chunk_writer.write_chunk)(
#        i,
#        img_size,
#        output_folder,
#        shm_dir_path
#        )
#                                            for i in chunks)
#    clear_temp_dir(shm_dir_path)
