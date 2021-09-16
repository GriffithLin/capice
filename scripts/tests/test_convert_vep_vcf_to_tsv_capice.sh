#!/bin/bash

# Base paths (to current dir/script).
readonly CURRENT_PATH=$(pwd)
BASE_PATH=$(realpath "$0") && readonly BASE_PATH=${BASE_PATH%/*}

main() {
  # Preparations.
  cd ${BASE_PATH}
  local -r input_vcf='../../CAPICE_example/capice_input.vcf.gz'
  local -r expected_output='../../CAPICE_example/CAPICE_input.tsv.gz'
  local -r actual_output='test_output.tsv.gz' # cleanup within each test!
  gunzip -k ${input_vcf} # keeps original gzip
  gunzip -k ${expected_output} # keeps original gzip

  # Run tests.
  testValidTextInput
  testValidGzipInput
  testEmptyInputParameter
  testNoOutputParameter
  testInvalidInputFileExtension
  testInvalidInputFilePath

  # Cleanup.
  rm ${input_vcf%.gz}
  rm ${expected_output%.gz}
}

# $1: the generated exitcode
# $2: the name of the test
validateIfFailed() {
  if [[ $1 != 1 ]]
  then
    echo "$2 failed"
  else
    echo "$2 succeeded"
  fi

  rmSilent ${actual_output}
}

# $1: the generated exitcode
# $2: the name of the test
validateOutputFile() {
  if [[ $1 != 0 ]]
  then
    echo "$2 failed"
  else
    gunzip ${actual_output}
    local checksum_expected=$(shasum -a 256 ${expected_output%.gz} | cut -d ' ' -f1)
    shasum -a 256 -c <<< "${checksum_expected%.gz}  ${actual_output%.gz}"
  fi

  rmSilent ${actual_output%.gz}
}

rmSilent() {
  rm "$1" 2> /dev/null
}

testValidTextInput() {
  bash ../convert_vep_vcf_to_tsv_capice.sh -i ${input_vcf%.gz} -o ${actual_output} &> /dev/null
  validateOutputFile $? 'testValidTextInput'
}

testValidGzipInput() {
  bash ../convert_vep_vcf_to_tsv_capice.sh -i ${input_vcf} -o ${actual_output} &> /dev/null
  validateOutputFile $? 'testValidGzipInput'
}

testEmptyInputParameter() {
  bash ../convert_vep_vcf_to_tsv_capice.sh -i "" -o ${actual_output}  &> /dev/null
  validateIfFailed "$?" 'testEmptyInputParameter'
}

testNoOutputParameter() {
  bash ../convert_vep_vcf_to_tsv_capice.sh -i ${input_vcf} &> /dev/null
  validateIfFailed "$?" 'testNoOutputParameter'
}

testInvalidInputFileExtension() {
  bash ../convert_vep_vcf_to_tsv_capice.sh -i './capice_input.vcf.zip' -o ${actual_output} &> /dev/null
  validateIfFailed "$?" 'testInvalidInputFileExtension'
}

testInvalidInputFilePath() {
  bash ../convert_vep_vcf_to_tsv_capice.sh -i './non_existing_dir/capice_input.vcf.gz' -o ${actual_output} &> /dev/null
  validateIfFailed "$?" 'testInvalidInputFileExtension'
}

main