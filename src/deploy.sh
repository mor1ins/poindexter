cd poindexter
python3 Main.py &

while true
do
    echo "running..."
    git remote update
    if git status | grep "is behind"
    then
        PID=$(ps ux | grep -m1 "Main.py" | cut -d" " -f9)
        kill -9 $PID
        echo "kill -9 $PID"
        git pull
        sleep 10
        echo "Run"
        python3 Main.py &
    fi
    sleep 60
done
