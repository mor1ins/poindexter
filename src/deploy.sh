cd poindexter
PID=$(python Main.py &)

while true; do
        git remote update
        if git status | grep "is behind"
        then
                kill $PID
                echo "Kill $PID"
                git pull
                PID=$(python Main.py &)
        fi
        sleep 10
done
