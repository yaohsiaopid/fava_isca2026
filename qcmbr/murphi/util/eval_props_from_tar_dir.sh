#!/bin/bash

# Re-evaluate unresolved properties for a target directory that contains:
# - out/    : input .m files
# - _build/ : prior .txt logs and build artifacts

time_limit=""
mem=""
tar_dir=""
JOBNUM=18

usage() {
  echo "Usage: $0 -d <tar_dir> -t <time_limit> -m <mem> [-j <jobs>]"
  echo "  -d  target directory that contains out/ and _build/"
  echo "  -t  timeout passed to timeout (for example: 75m)"
  echo "  -m  memory passed to murphi binary -m option (for example: 32768)"
  echo "  -j  parallel jobs (default: 18)"
}

while getopts "d:t:m:j:h" opt; do
  case $opt in
    d) tar_dir="$OPTARG" ;;
    t) time_limit="$OPTARG" ;;
    m) mem="$OPTARG" ;;
    j) JOBNUM="$OPTARG" ;;
    h) usage; exit 0 ;;
    \?) usage; exit 1 ;;
  esac
done

if [ -z "$tar_dir" ]; then
  echo "Error: -d <tar_dir> is required."
  usage
  exit 1
fi
if [ -z "$time_limit" ]; then
  echo "Error: -t <time_limit> is required."
  usage
  exit 1
fi
if [ -z "$mem" ]; then
  echo "Error: -m <mem> is required."
  usage
  exit 1
fi

OUT_DIR="${tar_dir}/out"
BUILD_DIR="${tar_dir}/_build"

echo "---> tar_dir: ${tar_dir}"
echo "--> out dir: ${OUT_DIR}"
echo "--> build dir: ${BUILD_DIR}"

if [ ! -d "$OUT_DIR" ]; then
  echo "Error: out directory not found: $OUT_DIR"
  exit 1
fi
if [ ! -d "$BUILD_DIR" ]; then
  echo "Error: _build directory not found: $BUILD_DIR"
  exit 1
fi

shopt -s nullglob
txt_files=("$BUILD_DIR"/*.txt)
shopt -u nullglob

if [ ${#txt_files[@]} -eq 0 ]; then
  echo "No .txt files found under $BUILD_DIR. Nothing to re-evaluate."
  exit 0
fi

declare -a TESTS_TO_RUN
while IFS= read -r txt_path; do
  base_name="$(basename "$txt_path" .txt)"
  if [ -f "${OUT_DIR}/${base_name}.m" ]; then
    TESTS_TO_RUN+=("$base_name")
  else
    echo "Skipping $base_name: missing source ${OUT_DIR}/${base_name}.m"
  fi
done < <(grep -EL "Assertion failed|Invariant.*failed|No error found" "${txt_files[@]}" || true)

echo "Unresolved tests to rerun: ${#TESTS_TO_RUN[@]}"
if [ ${#TESTS_TO_RUN[@]} -eq 0 ]; then
  echo "All listed tests are already complete (or no matching .m files)."
  exit 0
fi

run_single_test() {
  local base_name="$1"
  local output_log="${BUILD_DIR}/${base_name}.txt"
  local err_log="${BUILD_DIR}/${base_name}.err.log"
  local input="${OUT_DIR}/${base_name}.m"
  local res output_cpp output_bin

  : > "$output_log"
  mu "$input" &> "$err_log"

  res="${OUT_DIR}/${base_name}.cpp"
  if [ -f "$res" ]; then
    output_cpp="${BUILD_DIR}/${base_name}.cpp"
    mv "$res" "$output_cpp"

    output_bin="${BUILD_DIR}/${base_name}"
    g++ -g -w -I/cafe/u/yaohsiao/sandbox/murphi_playground/HeteroGen/CMurphi/include "$output_cpp" -o "$output_bin"

    ( timeout "$time_limit" /usr/bin/time -f "Time: %e seconds" "$output_bin" -m"${mem}" -tv ) &>> "$output_log"
    cp "$input" "${BUILD_DIR}/${base_name}.m"
  else
    echo "ERROR COMPILE" >> "$err_log"
  fi
}

export -f run_single_test
export OUT_DIR BUILD_DIR time_limit mem

parallel --load 80% -j "$JOBNUM" --memfree 64G --bar run_single_test ::: "${TESTS_TO_RUN[@]}"

echo "--> checking if any compilation fail"
pushd "$BUILD_DIR" >/dev/null || exit 1
find . -name "*.err.log" -exec grep -L "Code generated" {} \;
popd >/dev/null || exit 1

for t in "${TESTS_TO_RUN[@]}"; do
  if [ -f "${BUILD_DIR}/${t}.txt" ]; then
    if grep -Eq "Assertion failed|Invariant.*failed|No error found" "${BUILD_DIR}/${t}.txt"; then
      continue
    else
      echo "undetermined!!!! ${BUILD_DIR}/${t}.txt"
    fi
  else
    echo "no txt? ${BUILD_DIR}/${t}.txt"
  fi
done
