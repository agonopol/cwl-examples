#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: /opt/app/parser.py
hints:
  DockerRequirement:
    dockerPull: git.imp.fu-berlin.de:5000/bzfgonop/hmm-docker-cwl/hmm-html-report
inputs:
  table:
    type: File
    inputBinding:
      prefix: -r
  fasta:
    type: File
    inputBinding:
      prefix: -d
  output:
    type: string
    inputBinding:
      prefix: -o
outputs:
  html:
    type: File    
    outputBinding:
      glob:  $(inputs.output)
