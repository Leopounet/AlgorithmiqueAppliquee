if [[ ! ($# -le 1) ]]; then
    python3 main.py $1 $2
    if [[ $? = 0 ]]; then
        cd ../ssl_defender_viewer
        python3 main.py ../src/$1 ../src/data.json
        cd ../src/
    fi
else
    echo "Usage: ./solve.sh <file> <solveur>"
    echo "file: chemin vers le problème à résoudre"
    echo "solveur: le solveur à utiliser greedy|random|brute"
fi