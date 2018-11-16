#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: /opt/app/translate.py
requirements:
  EnvVarRequirement:
    envDef:
      PYTHONPATH: /biopython
hints:
  DockerRequirement:
    dockerPull: git.imp.fu-berlin.de:5000/bzfgonop/hmm-docker-cwl/fasta-translate
inputs:
  fasta:
    type: File
    inputBinding:
      prefix: --fasta
  dest:
    type: string
    inputBinding:
      prefix: --dest
outputs:
  translated:
    type: File    
    outputBinding:
      glob:  $(inputs.dest)
stdout: stdout.txt
