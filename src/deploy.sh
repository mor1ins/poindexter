cd poindexter
PID=$(python3 Main.py &)

while true do
        echo "hello"
        git remote update
        if git status | grep "is behind"
        then
                kill $PID
                echo "Kill $PID"
                git pull
                PID=$(python3 Main.py &)
        fi
        sleep 10
done
