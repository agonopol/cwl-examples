#!/usr/bin/python3.5

import os, warnings
from Bio import SeqIO
from sys import argv, stdout, exit
from Bio.Seq import Seq
from shutil import rmtree
from multiprocessing import Process, Queue, Lock, freeze_support
import argparse
import pathlib
import tempfile


# Progress bar
def progress(seq_num, in_queue, cpus):
    lock = Lock()
    lock.acquire()
    numq = seq_num - in_queue.qsize() + cpus
    stdout.write('\r'+' '*80)
    stdout.write('\rProgress: %d/%d' % (numq, seq_num))
    stdout.flush()
    lock.release()


# Translates a DNA sequence in 6 frames
def translate(in_queue, seq, seq_num, cpus, seqs, temp_path):
    for inq in iter(in_queue.get,'STOP'):
        progress(seq_num, in_queue, cpus)
        seq_id, seq = seqs[inq][0], Seq(seqs[inq][1].replace('X', 'N'))
        f = (-3,-2,-1,1,2,3)
        trans = []
        for i in f:
            if i < 0:
                trans.append(('%s_%d'%(seq_id,i), seq.reverse_complement()[-(i+1):].translate(stop_symbol='X')))
            elif i > 0:
                trans.append(('%s_+%d'%(seq_id,i), seq[i-1:].translate(stop_symbol='X')))
        with open(os.path.join(temp_path,'%d.txt'%(inq)), 'w') as out_f:
            [out_f.write('>%s\n%s\n'%(x[0],x[1])) for x in trans]


# Merges chunks
def concatenate(name, temp_path, out_path):
    dir_list = os.listdir(temp_path)
    outf = open(out_path,'w')
    for f in dir_list:
        with open(os.path.join(temp_path,f),'r') as infile:
            outf.write(infile.read())
    outf.close()

def main(): 
    warnings.filterwarnings('ignore')
    parser = argparse.ArgumentParser(description='Translate .fasta file to fasta-db.')
    parser.add_argument('--cpus', type=int, help='number of cpu\'s to use.', default=2)
    parser.add_argument('--fasta', help='input fasta file', required=True)
    parser.add_argument('--dest', help='output directory', required=False)

    args = parser.parse_args()

    temp_path = '/tmp/spill'
    pathlib.Path(temp_path).mkdir(parents=True, exist_ok=True)
 
    cpus, in_f = args.cpus, args.fasta
    plist, in_queue = [], Queue()

    # Reads genomic sequences
    print ('Reading the genome...')

    seqs = [(seq.description, str(seq.seq).upper()) for seq in SeqIO.parse(in_f,'fasta')]
    seq_num = len(seqs)
    [in_queue.put(i) for i in range(seq_num)]

    # Multiprocessing section
    print('Translating...')

    try:
        for cpu in range(cpus):
            freeze_support()
            p = Process(target=translate, args=(in_queue,'', seq_num, cpus, seqs, temp_path))
            in_queue.put('STOP')
            p.start()
            plist.append(p)
        for p in plist:
            p.join()
    except KeyboardInterrupt:
        print("Cleaning all child processess")
        for process in process_list:
            process.terminate()
            process.join()
            exit(1)

    # Concatenating
    print('\nConcatenating...')
    fname = os.path.relpath(in_f)
    concatenate(fname, temp_path, args.dest)

    # Removes the temporary folder 'temp'
    print ('Removing temporary files...')
    rmtree(temp_path)
    print ('All is done, check the "%s" folder' % (temp_path))

if __name__ == '__main__':
    main()

