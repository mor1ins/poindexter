cd poindexter
python3 Main.py &
cd ..

while true
do
        echo "hello"
        git remote update
        if git status | grep "is behind"
        then
                PID=$(ps ux | grep -m1 "Main.py" | cut -d" " -f4)
                kill $PID
                echo "Kill $PID"
                git pull
                PID=$(python3 Main.py &)
        fi
        sleep 10
done
