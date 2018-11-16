# fastadb-docker-cwl

Example for wrapping a simple job in a docker and adding CWL to run the docker

build docker:

```
docker build -t git.imp.fu-berlin.de:5000/bzfgonop/fastadb-docker-cwl .
```

run example job using the athrep.fasta provided

```
cwl-runner fasta-db.cwl example-fasta-db-job.yml
```

example-fasta-db-job.yml:
```
fasta:
  class: File
  path: athrep.fasta
dest: translated.fasta
```
input mapped File athrep.fasta
output: translated.fasta