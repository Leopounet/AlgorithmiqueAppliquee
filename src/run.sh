if [[ ! ($# -eq 0) ]]; then
    python3 main.py $1
    cd ../ssl_defender_viewer
    python3 main.py ../src/$1 ../src/dumps/data.json
    cd ../src/
else
    echo "Please specify a path to a problem to solve!"
fi