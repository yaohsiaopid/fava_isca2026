#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo $SCRIPT_DIR
FIG=$1
if [ ! -s "$FIG" ]; then
  exit 0
fi 
grep -q "WARNING" $FIG 
if [ $? -eq 0 ];
then
  echo "WARNING exists"
  grep "WARNING" $FIG
  exit 0
fi

echo "-> ${FIG}"
DOTBIN=$(which dot)
NEATOBIN=$(which neato)
if [[ $(hostname) =~ cafe-jg* ]]; then
  DOTBIN=/bin/dot
  NEATOBIN=/bin/neato
fi
echo "==> $DOTBIN"
# rm xx*
echo $FIG
if [ -f $FIG ];
then
  echo "J"
  if [ $(grep -c "digraph" $FIG) -eq 1 ]; 
  then 
      echo "=====> single digraph" 
      BASE=${FIG%.*}
      $DOTBIN -Tpng $FIG -o ${BASE}.png
      python3 "$SCRIPT_DIR/pp.py" $FIG
      ff=${BASE}.c.gv
      if which tred > /dev/null 2>&1; then
        tred ${ff} -o "${ff%.*}.trd.gv"
        sed -i "s/shape=circle/shape=circle,label=\"\"/g" "${ff%.*}.trd.gv"
        $DOTBIN -Tpng "${ff%.*}.trd.gv" -o "${ff%.*}.trd.png"
      fi
    
  else 
    BASE=${FIG%.*}
    mkdir -p "${BASE}_fig/src"
    csplit -z $FIG '/digraph.*{/' '{*}'
    for itm in $(ls xx*)
    do
          mv ${itm} ${itm}.gv
          grep -q "digraph G" ${itm}.gv
          if [ $? -eq 0 ]; then
            #grep -q "label.*Converged" ${itm}.gv
            #if [ $? -eq 0 ]; then 
              echo "--> ${itm}.gv"
              $NEATOBIN -Tpng ${itm}.gv -o ${itm}.png
              mv ${itm}.png  ${BASE}_fig
            #fi 
          fi
          mv ${itm}.gv ${BASE}_fig/src
    done
  fi
fi
