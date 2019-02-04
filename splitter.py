import os
import getopt
from pydub import AudioSegment


def usage():
    print(f'Usage: {os.sys.argv[0]} (-i <infile> | --in=<infile>) (-o <outdir> | --out=<outdir>) [--makedir]')


def split_file(infile, outdir='.', makedir=False, seconds=60):

    if makedir and not os.path.exists(outdir):
        try:
            os.makedirs(outdir)
        except OSError as e:
            print(f'Unable to create output directory: {outdir}')
            return

    audio = AudioSegment.from_mp3(infile)
    audio_len = int(audio.duration_seconds)

    for x in range(0, audio_len * 1000, 60000):
        start_secs = (x / 1000)
        segment = None
        if float(x + 60000) < (audio.duration_seconds * 1000):
            segment = audio[x:x + 60000]
        else:
            segment = audio[x:]
        outpath = os.path.join(outdir,f'out_{start_secs}.flac')
        segment.export(outpath, format='flac')
        print(f'Wrote {outpath}')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["help", "in=", "out=", "makedir"])
    except getopt.GetoptError:
        os.sys.exit(2)

    if not opts:
        usage()
        os.sys.exit(0)

    infile = ""
    outdir = "."
    makedir = False
    for opt, arg in opts:
        if opt in ("-i", "--in"):
            infile = arg
        elif opt in ("-o", "--out"):
            outdir = arg
        elif opt in ("--makedir"):
            makedir = True
        elif opt in ("-h", "--help"):
            usage()
            os.sys.exit(0)

    if not os.path.exists(infile):
        print(f'Input file does not exist: {infile}')
        os.sys.exit(1)
    elif not makedir and not os.path.exists(outdir):
        print(f'Output directory does not exist: {outdir}')
        os.sys.exit(1)

    split_file(infile, outdir, makedir)


if __name__ == '__main__':
    main(os.sys.argv[1:])
