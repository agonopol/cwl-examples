#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: hmmsearch
hints:
  DockerRequirement:
    dockerPull: git.imp.fu-berlin.de:5000/bzfgonop/hmm-docker-cwl/hmm-search
inputs:
  output:
    type: string
    inputBinding:
      position: 0      
      prefix: --domtblout
  hmm:
    type: File
    inputBinding:
      position: 1
  fasta:
    type: File
    inputBinding:
      position: 2 
outputs:
  domtblout:
    type: File    
    outputBinding:
      glob:  $(inputs.output)
