#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

inputs: 
  fasta:
    type: File
  hmm:
    type: File

outputs:
  html:
    type: File
    outputSource: report/html

steps:
  translate:
    run: fasta-translate/fasta-db.cwl
    in:
      fasta: [fasta]
      dest: 
        default: "translated.fasta"
    out: [translated]
  search:
    run: hmm-search/hmm-search.cwl
    in:
      fasta: translate/translated
      hmm: [hmm]
      output: 
        default: "profile.domtblout"
    out: [ domtblout ]
  report:
    run: hmm-html-report/hmm-html-report.cwl
    in:
      fasta: translate/translated
      table: search/domtblout
      output: 
        default: "report.html"
    out: [ html ]