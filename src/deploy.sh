cd poindexter
python3 Main.py &


while true
do
        echo "running..."
        git remote update
        if git status | grep "is behind"
        then
                PID=$(ps ux | grep -m1 "Main.py" | cut -d" " -f4)
                kill $PID
                echo "Kill $PID"
                git pull
                sleep 10
                echo "Run"
                python3 Main.py &
        fi
        sleep 60
done
